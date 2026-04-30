# Multilingual Text Preprocessor

A modular text preprocessing API supporting English and Arabic.

## Features
- English: lowercase, punctuation removal, stopwords, stemming, lemmatization
- Arabic: tashkeel, tatweel, alef normalization, smart stopwords, stemming
- Web GUI with real-time processing
- Configurable pipeline via JSON

## Run with Docker

Build:
docker build -t text-preprocessor .

Run:
docker run -p 8000:8000 text-preprocessor

Open: http://localhost:8000

API Docs: http://localhost:8000/docs