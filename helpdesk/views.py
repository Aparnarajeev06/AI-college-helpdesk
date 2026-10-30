
import hashlib
import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .ai import AIProviderError, AIRateLimitError, answer_question
from .data.ncerc_data import ncerc_data
from .models import ChatFeedback


logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def home(request):
    """Display the NCERC College Helpdesk homepage."""
    return render(
        request,
        "helpdesk/home.html",
        {
            "ncerc_data": ncerc_data,
            "chat_ai_enabled": settings.CHAT_AI_ENABLED,
            "chat_ai_provider": settings.CHAT_AI_PROVIDER,
        },
    )


def _chat_rate_limited(request):
    address = request.META.get("REMOTE_ADDR", "unknown")
    key = "helpdesk-chat:" + hashlib.sha256(address.encode()).hexdigest()
    if cache.add(key, 1, timeout=60):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.add(key, 1, timeout=60)
        return False
    return count > settings.CHAT_RATE_LIMIT


@require_POST
def chat_api(request):
    """Answer campus questions using retrieved facts and the configured model."""
    if len(request.body) > 4096:
        return JsonResponse(
            {"error": "Please keep your question under 1000 characters."},
            status=400,
        )

    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Please send a valid question."}, status=400)

    if not isinstance(body, dict):
        return JsonResponse({"error": "Please send a valid question."}, status=400)

    question = body.get("message")
    if not isinstance(question, str) or not question.strip():
        return JsonResponse({"error": "Please enter a question."}, status=400)

    question = question.strip()
    if len(question) > 1000:
        return JsonResponse(
            {"error": "Please keep your question under 1000 characters."},
            status=400,
        )

    if _chat_rate_limited(request):
        return JsonResponse(
            {
                "error": "The helpdesk is receiving many questions. Please try again shortly.",
                "fallback": True,
            },
            status=429,
        )

    if not settings.CHAT_AI_ENABLED:
        return JsonResponse(
            {"error": "AI chat is disabled; using local helpdesk rules.", "fallback": True},
            status=503,
        )

    try:
        result = answer_question(question)
    except AIRateLimitError as error:
        logger.warning("AI model rate limit reached: %s", error)
        return JsonResponse({"error": str(error), "fallback": True}, status=429)
    except AIProviderError as error:
        logger.warning("AI model request failed: %s", error)
        provider = getattr(settings, "CHAT_AI_PROVIDER", "ollama")
        provider_label = "local AI model" if provider == "ollama" else "AI model"
        return JsonResponse(
            {
                "error": f"The {provider_label} is unavailable; using local helpdesk rules.",
                "fallback": True,
            },
            status=503,
        )

    return JsonResponse(result)


@require_POST
def feedback_api(request):
    """Store a rating and its question to help improve local answer rules."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Please send valid feedback."},
            status=400,
        )

    if not isinstance(body, dict):
        return JsonResponse(
            {"error": "Please send valid feedback."},
            status=400,
        )

    question = body.get("question")
    is_helpful = body.get("is_helpful")

    if not isinstance(question, str) or not question.strip():
        return JsonResponse(
            {"error": "A question is required for feedback."},
            status=400,
        )

    if len(question) > 1000:
        return JsonResponse(
            {"error": "Please keep the question under 1000 characters."},
            status=400,
        )

    if not isinstance(is_helpful, bool):
        return JsonResponse(
            {"error": "Please choose whether the answer was helpful."},
            status=400,
        )

    ChatFeedback.objects.create(
        question=question.strip(),
        is_helpful=is_helpful,
    )
    return JsonResponse({"saved": True}, status=201)
