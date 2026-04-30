---
title: Multilingual Text Preprocessor
emoji: 🔤
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Multilingual Text Preprocessor

A modular REST API for preprocessing English and Arabic text, with a web GUI and configurable pipeline.

## Features

- **English**: lowercase, punctuation removal, stopword filtering, stemming, lemmatization
- **Arabic**: tashkeel removal, tatweel removal, alef normalization, stopword filtering, stemming
- **Web GUI** with real-time processing
- **Configurable pipeline** via JSON request body
- **Swagger UI** at `/docs`

## Run with Docker

```bash
# Build
docker build -t text-preprocessor .

# Run
docker run -p 7860:7860 text-preprocessor
```

Open the app: [http://localhost:7860](http://localhost:7860)

API docs: [http://localhost:7860/docs](http://localhost:7860/docs)
