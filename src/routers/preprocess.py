from fastapi import APIRouter, HTTPException

from src.models.schemas import PreprocessRequest, PreprocessResponse
from src.services.pipeline import run_pipeline
from src.utils.exceptions import PreprocessingError


router = APIRouter()


@router.post("/preprocess", response_model=PreprocessResponse)
async def processed_text(request: PreprocessRequest):
    """
    Preprocess text based on language and selected options.
    """
    try:
        response = run_pipeline(request)
        return response
    except PreprocessingError:
        # Let the global handler deal with our custom exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")