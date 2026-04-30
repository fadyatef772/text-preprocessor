import nltk

nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

from src.utils.cleaning import (
    remove_punctuation,
    remove_numbers,
    normalize_whitespace,
)
from src.utils.arabic_cleaning import (
    remove_tashkeel,
    remove_tatweel,
    normalize_alef,
    normalize_ya,
    normalize_ta_marbuta,
)


ARABIC_STOP_WORDS = set(stopwords.words("arabic"))

# Negation words we want to PROTECT from removal
ARABIC_NEGATIONS = {"لا", "ليس", "ليست", "لم", "لن", "ما", "غير"}


def get_safe_stopwords() -> set:
    """Return stopwords minus negation words."""
    return ARABIC_STOP_WORDS - ARABIC_NEGATIONS


SAFE_STOP_WORDS = get_safe_stopwords()


def process_arabic(text: str, options: dict) -> tuple[str, list[str]]:
    """
    Process Arabic text based on the given options.
    Returns (processed_text, list_of_applied_steps).
    """
    applied_steps = []

    # Step 1: Normalize (Arabic-specific)
    if options.get("normalize", False):
        text = remove_tashkeel(text)
        applied_steps.append("remove_tashkeel")

        text = remove_tatweel(text)
        applied_steps.append("remove_tatweel")

        text = normalize_alef(text)
        applied_steps.append("normalize_alef")

        text = normalize_ya(text)
        applied_steps.append("normalize_ya")

    # Step 2: Remove punctuation
    if options.get("remove_punctuation", False):
        text = remove_punctuation(text)
        applied_steps.append("remove_punctuation")

    # Step 3: Remove numbers
    if options.get("remove_numbers", False):
        text = remove_numbers(text)
        applied_steps.append("remove_numbers")

    # Step 4: Tokenize and remove stopwords
    tokens = text.split()

    if options.get("remove_stopwords", False):
        tokens = [t for t in tokens if t not in SAFE_STOP_WORDS]
        applied_steps.append("remove_stopwords_safe")

    # Step 5: Stemming (basic Arabic stemming)
    if options.get("stemming", False):
        from nltk.stem.isri import ISRIStemmer
        stemmer = ISRIStemmer()
        tokens = [stemmer.stem(t) for t in tokens]
        applied_steps.append("stemming")

    # Final: Rejoin and clean
    text = " ".join(tokens)
    text = normalize_whitespace(text)

    return text, applied_steps