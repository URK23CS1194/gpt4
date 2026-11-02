import requests, re

INTENTS = ["GENERATE_RECOMMENDATION", "REFINE_RECOMMENDATION", "SHOW_PROFILE", "EXPLAIN_RECOMMENDATION", "SAVE_RECOMMENDATION", "EXIT"]

def detect_intent(message, model="llama3.2"):
    text = message.lower()
    rules = [
        (["exit", "quit", "close", "bye"], "EXIT"),
        (["save", "download", "store"], "SAVE_RECOMMENDATION"),
        (["why", "explain", "reason"], "EXPLAIN_RECOMMENDATION"),
        (["profile", "my details", "show my"], "SHOW_PROFILE"),
        (["more", "instead", "avoid", "don't want", "do not want", "refine", "prefer"], "REFINE_RECOMMENDATION"),
        (["recommend", "suggest", "courses", "find"], "GENERATE_RECOMMENDATION"),
    ]
    for words, intent in rules:
        if any(word in text for word in words):
            return intent
    try:
        prompt = f"Classify this message into exactly one of {INTENTS}. Return only the label: {message}"
        r = requests.post("http://localhost:11434/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=30)
        r.raise_for_status()
        label = r.json().get("response", "").strip().upper()
        for intent in INTENTS:
            if intent in label:
                return intent
    except Exception:
        pass
    return "GENERATE_RECOMMENDATION"
