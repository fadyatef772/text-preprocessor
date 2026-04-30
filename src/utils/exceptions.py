class PreprocessingError(Exception):
    """Base exception for preprocessing errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UnsupportedLanguageError(PreprocessingError):
    """Raised when language is not supported."""
    def __init__(self, language: str):
        super().__init__(
            message=f"Language '{language}' is not supported. Use 'ar' or 'en'.",
            status_code=400,
        )


class EmptyTextError(PreprocessingError):
    """Raised when text is empty after processing."""
    def __init__(self):
        super().__init__(
            message="Text is empty after preprocessing. Try disabling some options.",
            status_code=422,
        )


class NLPResourceError(PreprocessingError):
    """Raised when an NLP resource fails to load."""
    def __init__(self, resource: str):
        super().__init__(
            message=f"Failed to load NLP resource: {resource}. Please check installation.",
            status_code=500,
        )