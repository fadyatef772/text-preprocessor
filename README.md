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

A modular REST API for cleaning and normalizing English and Arabic text, with a web GUI and configurable per-request pipeline.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Preprocessing Options](#preprocessing-options)
- [English Pipeline](#english-pipeline)
- [Arabic Pipeline](#arabic-pipeline)
- [Running Locally](#running-locally)
- [Docker](#docker)
- [Dependencies](#dependencies)

---

## Features

| Feature | English | Arabic |
|---|---|---|
| Lowercase normalization | ✅ | — |
| Repeated character normalization | ✅ | ✅ |
| URL removal | ✅ | ✅ |
| Emoji removal | ✅ | ✅ |
| Punctuation removal | ✅ | ✅ (includes ؟ ، ؛) |
| Number removal | ✅ | ✅ (includes Arabic-Indic ٠–٩) |
| Stopword removal | ✅ | ✅ (negations protected: لا ليس لم لن) |
| Stemming | ✅ Porter | ✅ ISRI |
| Lemmatization | ✅ WordNet | — |
| Tashkeel (diacritics) removal | — | ✅ |
| Tatweel removal | — | ✅ |
| Alef normalization (أ إ آ → ا) | — | ✅ |
| Ya normalization (ى → ي) | — | ✅ |
| Web GUI | ✅ | ✅ |
| Swagger UI | ✅ | ✅ |

---

## Project Structure

```
text-preprocessor/
├── Dockerfile
├── requirements.txt
├── static/
│   └── index.html              # Web GUI
└── src/
    ├── main.py                 # FastAPI app, routes, error handlers
    ├── models/
    │   └── schemas.py          # Pydantic request/response models
    ├── routers/
    │   └── preprocess.py       # POST /api/preprocess endpoint
    ├── services/
    │   ├── pipeline.py         # Language routing
    │   ├── english_processor.py
    │   └── arabic_processor.py
    └── utils/
        ├── cleaning.py         # Language-agnostic utilities
        ├── arabic_cleaning.py  # Arabic-specific utilities
        └── exceptions.py       # Custom exception hierarchy
```

---

## API Reference

### `POST /api/preprocess`

Preprocess text with a configurable pipeline.

**Request body**

```json
{
  "text": "The students are Running quickly!! Visit https://example.com 😊",
  "language": "en",
  "options": {
    "normalize": true,
    "remove_urls": true,
    "remove_emojis": true,
    "remove_punctuation": true,
    "remove_numbers": false,
    "remove_stopwords": true,
    "stemming": false,
    "lemmatize": true
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | ✅ | Input text to process |
| `language` | `"en"` \| `"ar"` | ✅ | Language code |
| `options` | object | ✅ | Preprocessing options (all default to `false`) |

**Response body**

```json
{
  "original_text": "The students are Running quickly!! Visit https://example.com 😊",
  "processed_text": "student run quickly",
  "language": "en",
  "applied_steps": [
    "lowercase",
    "normalize_repeated_chars",
    "remove_urls",
    "remove_emojis",
    "remove_punctuation",
    "remove_stopwords",
    "lemmatize"
  ]
}
```

**Error responses**

| Status | Condition |
|---|---|
| `400` | Unsupported language code |
| `422` | Text becomes empty after processing |
| `500` | NLP resource failed to load |

---

## Preprocessing Options

| Option | Default | Description |
|---|---|---|
| `normalize` | `false` | Lowercase (EN) · repeated char normalization · Arabic script normalization (AR) |
| `remove_urls` | `false` | Strip `http://`, `https://`, and `www.` URLs |
| `remove_emojis` | `false` | Remove emoji and Unicode symbol characters |
| `remove_punctuation` | `false` | Remove punctuation, including Arabic ؟ ، ؛ « » |
| `remove_numbers` | `false` | Remove digits (0–9 and Arabic-Indic ٠–٩) |
| `remove_stopwords` | `false` | Remove stopwords (Arabic negations are preserved) |
| `stemming` | `false` | Porter stemmer (EN) / ISRI stemmer (AR) |
| `lemmatize` | `false` | WordNet lemmatization (EN only) |

---

## English Pipeline

Steps execute in this fixed order; each step only runs if its option is enabled:

1. **normalize** — lowercase, then cap repeated chars at 2 (`soooo` → `soo`)
2. **remove_urls** — strip `http(s)://` and `www.` URLs
3. **remove_emojis** — strip emoji/symbol characters
4. **remove_punctuation** — strip `#` symbols then all punctuation
5. **remove_numbers** — strip digit sequences
6. **tokenize** — NLTK `word_tokenize`
7. **remove_stopwords** — NLTK English stopword list
8. **stemming** — Porter stemmer
9. **lemmatize** — WordNet lemmatizer
10. Join tokens, collapse whitespace

**Example**

```
Input:   "The students are Runninggg quickly!! Visit https://example.com 😊"
Options: normalize=true, remove_urls=true, remove_emojis=true,
         remove_punctuation=true, remove_stopwords=true, lemmatize=true

Output:  "student run quickly"
Steps:   lowercase → normalize_repeated_chars → remove_urls → remove_emojis
         → remove_punctuation → remove_stopwords → lemmatize
```

---

## Arabic Pipeline

Steps execute in this fixed order; each step only runs if its option is enabled:

1. **normalize** —
   - Remove tashkeel (diacritics: fatha, damma, kasra …)
   - Remove tatweel (stretching char `ـ`)
   - Normalize alef variants: أ إ آ → ا
   - Normalize ya: ى → ي
   - Cap repeated chars at 2
2. **remove_urls** — strip URLs
3. **remove_emojis** — strip emoji/symbol characters
4. **remove_punctuation** — strip punctuation including Arabic ؟ ، ؛ « »
5. **remove_numbers** — strip digits (0–9 and ٠–٩)
6. **tokenize** — whitespace split
7. **remove_stopwords** — NLTK Arabic stopwords; **negations preserved**: لا ليس ليست لم لن ما غير
8. **stemming** — ISRI stemmer
9. Join tokens, collapse whitespace

**Example**

```
Input:   "الطُّلابُ يَدرُسُونَ فِي الجَامِعَةِ!! العدد ١٢٣"
Options: normalize=true, remove_punctuation=true,
         remove_numbers=true, remove_stopwords=true

Output:  "طلاب يدرسون جامعه"
Steps:   remove_tashkeel → remove_tatweel → normalize_alef → normalize_ya
         → normalize_repeated_chars → remove_punctuation → remove_numbers
         → remove_stopwords_safe
```

**Negation protection example**

```
Input:   "هذا المنتج ليس جيداً"
Options: normalize=true, remove_stopwords=true

Output:  "المنتج ليس جيدا"   ← "ليس" is preserved
```

---

## Running Locally

**Requirements:** Python 3.10+

```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

- Web GUI: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

---

## Docker

```bash
# Build
docker build -t text-preprocessor .

# Run
docker run -p 7860:7860 text-preprocessor
```

- Web GUI: http://localhost:7860
- Swagger UI: http://localhost:7860/docs

The container respects a `PORT` environment variable and defaults to `7860`.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.115.0 | Web framework |
| `uvicorn` | 0.30.6 | ASGI server |
| `pydantic` | 2.9.0 | Request / response validation |
| `nltk` | 3.9.1 | Tokenization, stopwords, stemming, lemmatization |
| `pyarabic` | 0.6.15 | Arabic text utilities |
