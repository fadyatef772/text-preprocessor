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


def remove_urls(text: str) -> str:
    """Remove URLs (http, https, www) from text."""
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    return text


def remove_emojis(text: str) -> str:
    """Remove emojis and special Unicode symbols."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0000FE00-\U0000FE0F"
        "\U0000200D"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def remove_hashtags(text: str) -> str:
    """Remove hashtag symbols but keep the word."""
    return text.replace('#', '')