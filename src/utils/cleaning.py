import re
import string


def remove_punctuation(text: str) -> str:
    """Remove English and Arabic punctuation marks."""
    # Arabic punctuation characters
    arabic_punctuation = "؟،؛«»"
    all_punctuation = string.punctuation + arabic_punctuation
    return text.translate(str.maketrans("", "", all_punctuation))


def remove_numbers(text: str) -> str:
    """Remove English digits and Arabic-Indic digits."""
    # \d matches 0-9, we add Arabic-Indic numerals ٠-٩
    return re.sub(r"[\d٠-٩]+", "", text)


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces into one and strip edges."""
    return re.sub(r"\s+", " ", text).strip()


def remove_extra_newlines(text: str) -> str:
    """Replace multiple newlines with a single space."""
    return re.sub(r"\n+", " ", text)