import json
import textwrap

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.test import RequestFactory

from helpdesk.ai import retrieve_facts
from helpdesk.views import chat_api


QUESTIONS = [
    "Where is the playground?",
    "Where is the basketball court?",
    "What is inside Kapila block?",
    "Where is the administrative office?",
    "Which block contains the library?",
    "What facilities are available in Bhaskara block?",
    "Can I see the campus in 360\u00b0?",
    "Where is the swimming pool?",
]


class Command(BaseCommand):
    help = "Run isolated live tests against /api/chat/ with rate-limit cache reset per question."

    def handle(self, *args, **options):
        factory = RequestFactory()
        self.stdout.write(
            f"\nNCERC Helpdesk Live Test | provider={settings.CHAT_AI_PROVIDER} "
            f"| model={settings.OLLAMA_MODEL}\n"
        )

        for q in QUESTIONS:
            # ── Retrieve facts independently (lets us check retrieval vs model separately)
            retrieved = retrieve_facts(q)

            # ── Reset rate-limit cache so this question is never blocked by a prior one
            cache.clear()

            req = factory.post(
                "/api/chat/",
                data=json.dumps({"message": q}),
                content_type="application/json",
                REMOTE_ADDR="127.0.0.1",
            )
            req._dont_enforce_csrf_checks = True
            resp = chat_api(req)
            status = resp.status_code
            data = json.loads(resp.content)

            self.stdout.write("\n" + "=" * 72)
            self.stdout.write(f"Q : {q}")
            self.stdout.write(f"-- HTTP {status}")

            if status == 429:
                self.stdout.write("  \u26a0  RATE LIMITED (429) \u2014 NOT a retrieval failure")
                self.stdout.write(f"  error: {data.get('error')}")
                continue

            mode     = data.get("mode", "\u2014")
            provider = data.get("provider", "\u2014")
            fallback = data.get("fallback", False)
            conf     = data.get("confidence", "\u2014")
            location = data.get("location", {})
            src_url  = data.get("source_url", "\u2014")
            answer   = data.get("answer", "")
            error    = data.get("error", "")

            self.stdout.write(f"  mode      : {mode}")
            self.stdout.write(f"  provider  : {provider}")
            self.stdout.write(f"  fallback  : {fallback}")
            self.stdout.write(f"  confidence: {conf}")
            self.stdout.write(f"  location  : {json.dumps(location, ensure_ascii=False)}")
            self.stdout.write(f"  source    : {src_url}")

            if answer:
                wrapped = textwrap.fill(
                    answer, 66,
                    initial_indent="  answer   : ",
                    subsequent_indent="              ",
                )
                self.stdout.write(wrapped)
            if error:
                self.stdout.write(f"  error     : {error}")

            self.stdout.write(f"  retrieved ({len(retrieved)} facts):")
            for f in retrieved:
                conf_f = f.get("confidence", "?")
                self.stdout.write(f"    [{conf_f:18s}] {f['title']}")
                self.stdout.write(f"      location : {f.get('location', {})}")
                self.stdout.write(f"      source   : {f.get('source_url', '\u2014')}")

        self.stdout.write("\n" + "=" * 72)
        self.stdout.write("DONE\n")
