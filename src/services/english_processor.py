import nltk

nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

from src.utils.cleaning import (
    remove_punctuation,
    remove_numbers,
    normalize_whitespace,
)


# Load once — not inside the function
ENGLISH_STOP_WORDS = set(stopwords.words("english"))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def process_english(text: str, options: dict) -> tuple[str, list[str]]:
    """
    Process English text based on the given options.
    Returns (processed_text, list_of_applied_steps).
    """
    applied_steps = []

    # Step 1: Lowercase (part of normalize)
    if options.get("normalize", False):
        text = text.lower()
        applied_steps.append("lowercase")

    # Step 2: Remove punctuation
    if options.get("remove_punctuation", False):
        text = remove_punctuation(text)
        applied_steps.append("remove_punctuation")

    # Step 3: Remove numbers
    if options.get("remove_numbers", False):
        text = remove_numbers(text)
        applied_steps.append("remove_numbers")

    # Step 4: Tokenize for word-level operations
    tokens = word_tokenize(text)

    # Step 5: Remove stopwords
    if options.get("remove_stopwords", False):
        tokens = [t for t in tokens if t.lower() not in ENGLISH_STOP_WORDS]
        applied_steps.append("remove_stopwords")

    # Step 6: Stemming
    if options.get("stemming", False):
        tokens = [stemmer.stem(t) for t in tokens]
        applied_steps.append("stemming")

    # Step 7: Lemmatization
    if options.get("lemmatize", False):
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
        applied_steps.append("lemmatize")

    # Final: Join tokens and clean whitespace
    text = " ".join(tokens)
    text = normalize_whitespace(text)

    return text, applied_steps