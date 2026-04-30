import re


# Tashkeel (diacritics) Unicode range
TASHKEEL_PATTERN = re.compile(r"[\u0617-\u061A\u064B-\u0652]")

# Tatweel character
TATWEEL = "\u0640"


def remove_tashkeel(text: str) -> str:
    """Remove Arabic diacritics (fatha, damma, kasra, etc.)."""
    return TASHKEEL_PATTERN.sub("", text)


def remove_tatweel(text: str) -> str:
    """Remove Arabic tatweel (stretching character)."""
    return text.replace(TATWEEL, "")


def normalize_alef(text: str) -> str:
    """Normalize all Alef variants (أ إ آ) to bare Alef (ا)."""
    text = re.sub(r"[أإآ]", "ا", text)
    return text


def normalize_ya(text: str) -> str:
    """Normalize Alef Maqsura (ى) to Ya (ي)."""
    return text.replace("ى", "ي")


def normalize_ta_marbuta(text: str) -> str:
    """Normalize Ta Marbuta (ة) to Ha (ه). Use cautiously."""
    return text.replace("ة", "ه")