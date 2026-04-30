from src.models.schemas import PreprocessRequest, PreprocessResponse
from src.services.english_processor import process_english
from src.services.arabic_processor import process_arabic
from src.utils.exceptions import UnsupportedLanguageError, EmptyTextError


def run_pipeline(request: PreprocessRequest) -> PreprocessResponse:
    """
    Route the request to the correct language processor
    and return a structured response.
    """
    options = request.options.model_dump()

    if request.language == "en":
        processed_text, applied_steps = process_english(request.text, options)
    elif request.language == "ar":
        processed_text, applied_steps = process_arabic(request.text, options)
    else:
        raise UnsupportedLanguageError(request.language)

    # Check if text became empty after processing
    if not processed_text.strip():
        raise EmptyTextError()

    return PreprocessResponse(
        original_text=request.text,
        processed_text=processed_text,
        language=request.language,
        applied_steps=applied_steps,
    )