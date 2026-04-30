# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during build (not at runtime)
RUN python -c "\
import nltk; \
nltk.download('punkt_tab'); \
nltk.download('stopwords'); \
nltk.download('wordnet'); \
nltk.download('averaged_perceptron_tagger'); \
"

# Copy project files
COPY src/ ./src/
COPY static/ ./static/

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]