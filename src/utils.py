import re
from pathlib import Path

import emoji

def get_project_root():
    """Get the absolute path of the project root directory."""
    return Path(__file__).parent.parent.resolve()

def remove_emojis(text):
    return emoji.replace_emoji(text, replace="")

def remove_urls(text):
    return re.sub(r"https?://\S+", "", text)

def collapse_whitespace(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

MEDIA_CAPTIONS = re.compile(r"^\[?(Photo|Video|Sticker|GIF|Document|Audio|Voice message|Video message)\]?$", re.IGNORECASE)
SYSTEM_MESSAGES = re.compile(r"(joined the group|left the group|pinned a message|changed the group|added|removed)", re.IGNORECASE)

def is_valid_message(text):
    if not text:
        return False
    if MEDIA_CAPTIONS.match(text):
        return False
    if SYSTEM_MESSAGES.search(text):
        return False
    if not re.search(r"[a-zA-ZçğıöşüÇĞİÖŞÜ0-9]", text):
        return False
    words = text.split()
    if len(text) < 20 or len(words) < 5:
        return False
    if len(text) > 250 or len(words) > 50:
        return False
    return True

def clean_message(text):
    text = remove_emojis(text)
    text = remove_urls(text)
    text = collapse_whitespace(text)
    if not is_valid_message(text):
        return None
    return text

def process_messages(messages: list[str]) -> list[str]:
    cleaned = [clean_message(m) for m in messages]
    return [m for m in cleaned if m is not None]

def build_user_prompt(data:list[str]) -> str:
        user_prompt = "Analyze the following messages:\n\n"
        for msg in data:
            user_prompt += f"- {msg}\n"
        return user_prompt

def build_system_prompt() -> str:
    return """You are a visa appointment alert classifier for Turkey. You will receive a batch of recent messages from Turkish visa appointment Telegram channels.

Your job: Identify messages that suggest visa appointment slots may be available.

## What counts as an alert:
- Someone confirming open appointment slots
- Specific mentions of country + city + availability
- Someone suggesting others should check for slots ("bi bakın", "açılmış olabilir")
- Shared links to booking pages with available dates

## What to IGNORE:
- Questions without any claim of availability ("randevu var mı?")
- Pure wishful thinking about the future ("inşallah açılır", "belki yarın")
- Past tense reports about slots that already closed ("vardı ama bitti", "kaçırdım")
- Complaints, discussions, advice, or off-topic chat
- Someone sharing their personal appointment date (already booked)
- Sarcasm or frustration ("sanki açılacak", "rüyamda gördüm")

## Response format:
If NO valid alerts found, respond ONLY with:
NO

If valid alerts found, respond ONLY with:
{"alerts":[{"country":"<country>","city":"<city>","source":"<brief quote from original message>","confidence":"high|medium"}]}

Rules:
- Respond ONLY with valid JSON or NO, nothing else
- No explanations, no preamble, no markdown
- "high" = direct confirmation of available slots
- "medium" = likely or possibly available, worth checking
- Country names in English, properly capitalized"""

def format_alert(alert: dict) -> str:
    country = alert.get("country", "Unknown")
    city = alert.get("city", "Unknown")
    confidence = alert.get("confidence", "unknown")
    source = alert.get("source", "")
    return (
        f"Country: {country}\n"
        f"City: {city}\n"
        f"Confidence: {confidence}\n"
        f"Source: {source}"
    )

def format_alerts(alerts: list[dict]) -> str:
    header = f"VISA ALERT - {len(alerts)} slot(s) found!\n\n"
    body = "\n\n---\n\n".join(format_alert(a) for a in alerts)
    return header + body