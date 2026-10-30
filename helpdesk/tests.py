import json
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from django.core.cache import cache
from django.test import Client, TestCase, override_settings

from .ai import (
    AIProviderError,
    AIRateLimitError,
    _ollama_chat,
    _openai_chat,
    generate_answer,
    retrieve_facts,
)
from .data.ncerc_data import ncerc_data
from .models import ChatFeedback


class HelpdeskHomeTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_homepage_serves_room_317_information(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "IQAC Conference Room")
        self.assertContains(response, '"317": "IQAC Conference Room"')
        self.assertContains(response, 'data-question="Where is the library?"')
        self.assertContains(response, 'data-question="Show me the campus tour."')
        self.assertContains(response, 'href="https://ncerc.ac.in/360/"')
        self.assertContains(
            response,
            "https://www.google.com/maps/search/?api=1&amp;"
            "query=Nehru%20College%20of%20Engineering%20and%20Research%20Centre",
        )
        self.assertContains(response, "Your question and rating are saved")
        self.assertContains(response, "Project Abstract")
        self.assertContains(response, "does not require a paid")
        self.assertContains(response, "AI with local fallback")

    @patch("helpdesk.ai.generate_answer", return_value="The library is on the ground floor.")
    def test_chat_returns_mocked_ai_answer_with_retrieved_location(self, generate):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "Where can I find the library?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mode"], "ai")
        self.assertEqual(response.json()["answer"], "The library is on the ground floor.")
        self.assertEqual(response.json()["location"]["block"], "Brahmagupta Block")
        self.assertEqual(response.json()["location"]["floor"], "Ground Floor")
        self.assertEqual(response.json()["location"]["facility"], "NCERC Central Library")
        self.assertEqual(
            response.json()["links"][0]["href"],
            "https://ncerc.ac.in/360/",
        )
        self.assertIn("google.com/maps/search", response.json()["links"][1]["href"])
        self.assertEqual(
            response.json()["image"],
            "/static/helpdesk/images/optimized/library.jpg",
        )
        generate.assert_called_once()
        self.assertTrue(any(
            "NCERC Central Library" in fact["text"]
            for fact in generate.call_args.args[1]
        ))

    def test_retrieval_finds_typos_rooms_and_block_facilities(self):
        library = retrieve_facts("Where is the libary?")
        classroom = retrieve_facts("Where is room 318?")
        bhaskara = retrieve_facts("What facilities are in Bhaskara Block?")

        self.assertTrue(any("Central Library" in fact["text"] for fact in library))
        self.assertTrue(any("Room 318" in fact["text"] for fact in classroom))
        self.assertTrue(any("KTU Exam Cell" in fact["text"] for fact in bhaskara))

    def test_unknown_question_returns_fallback_without_calling_model(self):
        with patch("helpdesk.ai.generate_answer") as generate:
            response = self.client.post(
                "/api/chat/",
                data=json.dumps({"message": "Where is the ATM?"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["fallback"])
        generate.assert_not_called()

    def test_department_location_not_in_dataset_uses_fallback(self):
        with patch("helpdesk.ai.generate_answer") as generate:
            response = self.client.post(
                "/api/chat/",
                data=json.dumps({"message": "Where is the CSE department?"}),
                content_type="application/json",
            )

        self.assertTrue(response.json()["fallback"])
        generate.assert_not_called()

    def test_ambiguous_office_question_asks_for_clarification(self):
        with patch("helpdesk.ai.generate_answer") as generate:
            response = self.client.post(
                "/api/chat/",
                data=json.dumps({"message": "Where is the office?"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mode"], "clarification")
        self.assertIn("Which location", response.json()["answer"])
        generate.assert_not_called()

    @override_settings(CHAT_AI_ENABLED=False)
    def test_disabled_ai_returns_rule_fallback_signal(self):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "Where is the library?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 503)
        self.assertTrue(response.json()["fallback"])

    @patch("helpdesk.ai.generate_answer", side_effect=AIProviderError("connection failed"))
    def test_model_failure_returns_fallback_signal_without_details(self, _generate):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "Where is the library?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 503)
        self.assertTrue(response.json()["fallback"])
        self.assertNotIn("connection failed", response.json()["error"])

    def test_invalid_and_excessively_long_chat_input_is_rejected(self):
        invalid = self.client.post(
            "/api/chat/", data="{", content_type="application/json"
        )
        too_long = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "x" * 1001}),
            content_type="application/json",
        )

        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(too_long.status_code, 400)
        self.assertEqual(
            self.client.post(
                "/api/chat/",
                data=json.dumps({"message": "a"}) + (" " * 4096),
                content_type="application/json",
            ).status_code,
            400,
        )

    def test_chat_requires_post_and_valid_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.get("/api/chat/").status_code, 405)
        self.assertEqual(
            client.post(
                "/api/chat/",
                data=json.dumps({"message": "Where is the library?"}),
                content_type="application/json",
            ).status_code,
            403,
        )
        client.get("/")
        token = client.cookies["csrftoken"].value
        with patch("helpdesk.ai.generate_answer", return_value="The library is here."):
            response = client.post(
                "/api/chat/",
                data=json.dumps({"message": "Where is the library?"}),
                content_type="application/json",
                HTTP_X_CSRFTOKEN=token,
            )
        self.assertEqual(response.status_code, 200)

    @override_settings(CHAT_RATE_LIMIT=1)
    @patch("helpdesk.ai.generate_answer", return_value="Answer.")
    def test_chat_rate_limit_is_applied(self, _generate):
        data = json.dumps({"message": "Where is the library?"})
        first = self.client.post("/api/chat/", data=data, content_type="application/json")
        second = self.client.post("/api/chat/", data=data, content_type="application/json")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)
        self.assertTrue(second.json()["fallback"])

    @override_settings(
        CHAT_AI_PROVIDER="ollama",
        OLLAMA_BASE_URL="http://127.0.0.1:11434",
        OLLAMA_MODEL="qwen2.5:3b",
        OLLAMA_TIMEOUT=3,
    )
    @patch(
        "helpdesk.ai.urlopen",
        return_value=BytesIO(b'{"message":{"content":"Ground floor."}}'),
    )
    def test_ollama_provider_sends_separate_system_and_user_messages(self, urlopen):
        answer = _ollama_chat("Where is the library?", retrieve_facts("Where is the library?"))

        self.assertEqual(answer, "Ground floor.")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "qwen2.5:3b")
        self.assertEqual(payload["messages"][1]["role"], "user")
        self.assertIn("Retrieved campus facts", payload["messages"][0]["content"])
        self.assertIn("NCERC Central Library", payload["messages"][0]["content"])

    @override_settings(
        OLLAMA_BASE_URL="http://127.0.0.1:11434",
        OLLAMA_MODEL="qwen2.5:3b",
        OLLAMA_TIMEOUT=1,
    )
    @patch("helpdesk.ai.urlopen", side_effect=URLError("connection refused"))
    def test_ollama_connection_failure_is_reported_as_provider_error(self, _urlopen):
        with self.assertRaises(AIProviderError):
            _ollama_chat("Where is the library?", retrieve_facts("Where is the library?"))

    def test_homepage_serves_aryabhatta_first_floor_directory(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aryabhatta Block - First Floor")
        self.assertContains(response, '"205-214": "ME Faculty Cabins"')
        self.assertContains(response, "Advanced Computing Lab")
        self.assertContains(response, "confirm the assignment")

    def test_academic_office_is_listed_on_aryabhatta_first_floor(self):
        self.assertIn(
            "Academic Office",
            ncerc_data["aryabhatta_first_floor"]["facilities"],
        )
        self.assertNotIn(
            "Academic Office",
            ncerc_data["aryabhatta_second_floor"]["facilities"],
        )

    def test_chat_feedback_is_saved_for_rule_improvements(self):
        response = self.client.post(
            "/api/feedback/",
            data=json.dumps({
                "question": "Library location?",
                "is_helpful": False,
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"saved": True})
        feedback = ChatFeedback.objects.get()
        self.assertEqual(feedback.question, "Library location?")
        self.assertFalse(feedback.is_helpful)

    def test_chat_feedback_rejects_missing_or_invalid_values(self):
        missing_question = self.client.post(
            "/api/feedback/",
            data=json.dumps({"is_helpful": True}),
            content_type="application/json",
        )
        invalid_rating = self.client.post(
            "/api/feedback/",
            data=json.dumps({
                "question": "Library location?",
                "is_helpful": "yes",
            }),
            content_type="application/json",
        )

        self.assertEqual(missing_question.status_code, 400)
        self.assertEqual(invalid_rating.status_code, 400)
        self.assertEqual(ChatFeedback.objects.count(), 0)

    def test_helpdesk_script_is_not_wrapped_in_markdown(self):
        script_path = Path(__file__).resolve().parent / "static" / "helpdesk" / "script.js"
        script = script_path.read_text(encoding="utf-8")

        self.assertTrue(script.startswith('document.addEventListener("DOMContentLoaded"'))
        self.assertNotIn("```", script)

    @override_settings(
        CHAT_AI_PROVIDER="openai",
        OPENAI_API_KEY="test-mock-key",
        OPENAI_MODEL="gpt-4o-mini",
        OPENAI_TIMEOUT=5,
    )
    @patch(
        "helpdesk.ai.urlopen",
        return_value=BytesIO(
            b'{"choices":[{"message":{"content":"The library is in Brahmagupta Block."}}]}'
        ),
    )
    def test_openai_provider_sends_chat_request(self, urlopen):
        answer = _openai_chat(
            "Where is the library?",
            retrieve_facts("Where is the library?"),
        )
        self.assertEqual(answer, "The library is in Brahmagupta Block.")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "gpt-4o-mini")
        self.assertEqual(payload["messages"][1]["role"], "user")
        self.assertIn("Retrieved campus facts", payload["messages"][0]["content"])
        self.assertEqual(
            request.headers.get("Authorization"),
            "Bearer test-mock-key",
        )

    @override_settings(
        CHAT_AI_PROVIDER="openai",
        OPENAI_API_KEY="",
    )
    def test_openai_missing_api_key_raises_provider_error(self):
        with self.assertRaises(AIProviderError):
            _openai_chat(
                "Where is the library?",
                retrieve_facts("Where is the library?"),
            )

    @override_settings(
        CHAT_AI_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
    )
    @patch(
        "helpdesk.ai.urlopen",
        side_effect=HTTPError(
            "https://api.openai.com", 429, "Too Many Requests", {}, BytesIO(b"{}")
        ),
    )
    def test_openai_rate_limit_raises_ai_rate_limit_error(self, _urlopen):
        with self.assertRaises(AIRateLimitError):
            _openai_chat(
                "Where is the library?",
                retrieve_facts("Where is the library?"),
            )

    @override_settings(
        CHAT_AI_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
    )
    @patch(
        "helpdesk.ai.urlopen",
        side_effect=HTTPError(
            "https://api.openai.com", 401, "Unauthorized", {}, BytesIO(b"{}")
        ),
    )
    def test_openai_invalid_key_raises_provider_error(self, _urlopen):
        with self.assertRaises(AIProviderError):
            _openai_chat(
                "Where is the library?",
                retrieve_facts("Where is the library?"),
            )

    @override_settings(
        CHAT_AI_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
    )
    @patch("helpdesk.ai.urlopen", side_effect=URLError("connection refused"))
    def test_openai_connection_failure_raises_provider_error(self, _urlopen):
        with self.assertRaises(AIProviderError):
            _openai_chat(
                "Where is the library?",
                retrieve_facts("Where is the library?"),
            )

    @override_settings(
        CHAT_AI_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
    )
    @patch("helpdesk.ai._openai_chat", return_value="Dispatched to OpenAI.")
    def test_generate_answer_dispatches_to_openai(self, openai_mock):
        answer = generate_answer(
            "Where is the library?",
            retrieve_facts("Where is the library?"),
        )
        self.assertEqual(answer, "Dispatched to OpenAI.")
        openai_mock.assert_called_once()

    @override_settings(CHAT_AI_PROVIDER="unsupported_provider")
    def test_generate_answer_unsupported_provider_raises_error(self):
        with self.assertRaises(AIProviderError):
            generate_answer(
                "Where is the library?",
                retrieve_facts("Where is the library?"),
            )

    def test_retrieval_finds_campus_tour_and_classroom(self):
        explore = retrieve_facts("How can I explore the campus?")
        classroom = retrieve_facts("Where can I find classroom 111?")

        self.assertTrue(any("Campus Tour" in fact["title"] for fact in explore))
        self.assertTrue(any("Room 111" in fact["title"] for fact in classroom))

    def test_retrieval_finds_playground_and_basketball_court(self):
        playground = retrieve_facts("Where is the playground?")
        basketball = retrieve_facts("Where is the basketball court?")
        sports_synonym = retrieve_facts("Where is the play ground?")
        bball_synonym = retrieve_facts("Where is the basket ball court?")

        self.assertTrue(any("Playground" in fact["title"] for fact in playground))
        self.assertEqual(playground[0]["location"]["block"], "Campus Grounds")
        self.assertTrue(any("Basketball Court" in fact["title"] for fact in basketball))
        self.assertEqual(basketball[0]["location"]["block"], "Campus Grounds")
        self.assertTrue(any("Playground" in fact["title"] for fact in sports_synonym))
        self.assertTrue(any("Basketball" in fact["title"] for fact in bball_synonym))

    def test_retrieval_finds_kapila_and_varahamihira_blocks(self):
        kapila = retrieve_facts("What is inside Kapila block?")
        varahamihira = retrieve_facts("What is in Varahamihira block?")

        self.assertTrue(any("Kapila Block" in fact["title"] for fact in kapila))
        self.assertTrue(any("MBA" in fact["text"] for fact in kapila))
        self.assertTrue(any("MCA" in fact["text"] for fact in kapila))
        self.assertEqual(kapila[0]["location"]["block"], "Kapila Block")
        # Kapila Block confidence must be verified
        self.assertEqual(
            next(f for f in kapila if "Kapila Block" in f["title"])["confidence"],
            "verified",
        )

        self.assertTrue(any("Varahamihira Block" in fact["title"] for fact in varahamihira))
        self.assertTrue(any("workshop" in fact["text"].lower() for fact in varahamihira))
        self.assertEqual(varahamihira[0]["location"]["block"], "Varahamihira Block")
        # Varahamihira now correctly states 4 EE labs (was 3 in old dataset)
        self.assertTrue(any("4 Electrical" in fact["text"] for fact in varahamihira))

    def test_retrieval_finds_administrative_office_and_synonyms(self):
        admin_office = retrieve_facts("Where is the administrative office?")
        admin_synonym = retrieve_facts("Where is the admin office?")

        self.assertTrue(any("Administrative" in fact["title"] for fact in admin_office))
        self.assertEqual(admin_office[0]["location"]["block"], "Aryabhatta Block")
        self.assertEqual(admin_office[0]["location"]["floor"], "First Floor")
        self.assertTrue(any("Administrative" in fact["title"] for fact in admin_synonym))

    def test_retrieval_identifies_block_containing_library(self):
        library_block = retrieve_facts("Which block contains the library?")

        self.assertTrue(any("Central Library" in fact["title"] for fact in library_block))
        self.assertTrue(any("Brahmagupta" in fact["text"] for fact in library_block))

    def test_retrieval_finds_bhaskara_block_facilities(self):
        bhaskara = retrieve_facts("What facilities are available in Bhaskara block?")

        self.assertTrue(any("Bhaskara Block" in fact["title"] for fact in bhaskara))
        self.assertTrue(any("Gymnasium" in fact["text"] for fact in bhaskara))

    def test_retrieval_finds_360_tour(self):
        tour = retrieve_facts("Can I see the campus in 360°?")

        self.assertTrue(any("Campus Tour" in fact["title"] for fact in tour))
        self.assertIn("360", tour[0]["text"])

    def test_unverified_location_uses_fallback(self):
        with patch("helpdesk.ai.generate_answer") as generate:
            response = self.client.post(
                "/api/chat/",
                data=json.dumps({"message": "Where is the swimming pool?"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["fallback"])
        self.assertIn("verified", response.json()["error"].lower())
        generate.assert_not_called()

    @patch("helpdesk.ai.generate_answer", return_value="The playground is on campus grounds.")
    def test_chat_returns_playground_location_and_source_links(self, _generate):
        response = self.client.post(
            "/api/chat/",
            data=json.dumps({"message": "Where is the playground?"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["mode"], "ai")
        self.assertEqual(data["location"]["block"], "Campus Grounds")
        self.assertEqual(data["links"][0]["href"], "https://ncerc.ac.in/360/")
        # playground source is now ncerc.ac.in/sports
        self.assertIn("sports", data["links"][2]["href"].lower())

    def test_data_confidence_fields_are_set_correctly(self):
        """Each top-level entry must declare a confidence field with a known value."""
        from helpdesk.data.ncerc_data import ncerc_data
        allowed = {"verified", "verified-partial", "unverified"}
        top_level_entries = [
            "library", "canteen", "fitness_centre", "transportation",
            "auditorium", "sports_playground", "basketball_court",
            "kapila_block", "brahmagupta_block", "varahamihira_block",
            "bhaskara_block", "aryabhatta_block", "administrative_office", "hostels",
        ]
        for key in top_level_entries:
            entry = ncerc_data[key]
            self.assertIn(
                entry.get("confidence"), allowed,
                f"Entry '{key}' has unexpected confidence: {entry.get('confidence')!r}",
            )

    def test_library_is_verified_in_brahmagupta_ground_floor(self):
        """Library facts must be verified and in Brahmagupta Block, Ground Floor."""
        facts = retrieve_facts("Where is the library?")
        library_fact = next(
            (f for f in facts if "Central Library" in f["title"]), None
        )
        self.assertIsNotNone(library_fact, "Library fact not retrieved")
        self.assertEqual(library_fact["confidence"], "verified")
        self.assertEqual(library_fact["location"]["block"], "Brahmagupta Block")
        self.assertEqual(library_fact["location"]["floor"], "Ground Floor")

    def test_varahamihira_block_states_four_electrical_labs(self):
        """Official source says 4 EE labs; old dataset incorrectly said 3."""
        from helpdesk.data.ncerc_data import ncerc_data
        desc = ncerc_data["varahamihira_block"]["description"]
        self.assertIn("four", desc.lower(), "Varahamihira should state four EE laboratories")

    def test_basketball_court_source_is_sports_page(self):
        """Basketball court source URL must point to the sports page."""
        from helpdesk.data.ncerc_data import ncerc_data
        self.assertIn("sports", ncerc_data["basketball_court"]["source_url"])

    def test_canteen_timing_is_not_claimed_as_verified(self):
        """Canteen opening hours could not be confirmed from official page text."""
        from helpdesk.data.ncerc_data import ncerc_data
        # Confidence must NOT be fully 'verified' since timing is unconfirmed
        self.assertNotEqual(ncerc_data["canteen"].get("confidence"), "verified")


