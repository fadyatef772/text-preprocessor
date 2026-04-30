from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from src.routers.preprocess import router as preprocess_router
from src.utils.exceptions import PreprocessingError


app = FastAPI(
    title="Multilingual Text Preprocessor",
    description="A modular text preprocessing API supporting English and Arabic",
    version="1.0.0",
)


# Global error handler for our custom exceptions
@app.exception_handler(PreprocessingError)
async def preprocessing_error_handler(request: Request, exc: PreprocessingError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# Register routers
app.include_router(preprocess_router, prefix="/api", tags=["Preprocessing"])

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")