"""
Isolated live test — run via:
  venv\Scripts\python.exe manage.py shell < scratch\shell_test.py
"""
import json, textwrap
from django.core.cache import cache
from django.test import RequestFactory
from helpdesk.views import chat_api
from helpdesk.ai import retrieve_facts
from django.conf import settings as djsettings

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

factory = RequestFactory()

def ask(question):
    cache.clear()
    req = factory.post(
        "/api/chat/",
        data=json.dumps({"message": question}),
        content_type="application/json",
        REMOTE_ADDR="127.0.0.1",
    )
    req._dont_enforce_csrf_checks = True
    resp = chat_api(req)
    return resp.status_code, json.loads(resp.content)

print(f"\nProvider: {djsettings.CHAT_AI_PROVIDER} | Model: {djsettings.OLLAMA_MODEL}\n")

for q in QUESTIONS:
    retrieved = retrieve_facts(q)
    status, data = ask(q)

    print("=" * 72)
    print(f"Q : {q}")
    print(f"── HTTP {status}")

    if status == 429:
        print("  ⚠  RATE LIMITED (429) — NOT a retrieval failure")
        print(f"  error: {data.get('error')}")
        continue

    print(f"  mode      : {data.get('mode','—')}")
    print(f"  provider  : {data.get('provider','—')}")
    print(f"  fallback  : {data.get('fallback', False)}")
    print(f"  confidence: {data.get('confidence','—')}")
    print(f"  location  : {json.dumps(data.get('location',{}), ensure_ascii=False)}")
    print(f"  source    : {data.get('source_url','—')}")

    if data.get("answer"):
        wrapped = textwrap.fill(data["answer"], 68,
                                initial_indent="  answer   : ",
                                subsequent_indent="              ")
        print(wrapped)
    if data.get("error"):
        print(f"  error     : {data['error']}")

    print(f"  retrieved ({len(retrieved)} facts):")
    for f in retrieved:
        print(f"    [{f.get('confidence','?'):18s}] {f['title']}")
        print(f"      location : {f.get('location',{})}")
        print(f"      source   : {f.get('source_url','—')}")

print("\n" + "="*72)
print("DONE")
