from src.models.schemas import PreprocessRequest, PreprocessResponse

# ✅ Valid request
req = PreprocessRequest(
    text="Hello world",
    language="en",
    options={"remove_stopwords": True, "normalize": True}
)
print("Text:", req.text)
print("Language:", req.language)
print("Remove stopwords:", req.options.remove_stopwords)
print("Stemming:", req.options.stemming)  # Should be False (default)

# ✅ Valid response
resp = PreprocessResponse(
    original_text="Hello world",
    preprocessed_text ="hello world",
    language="en",
    applied_steps=["normalize"]
)
print("\nResponse:", resp.model_dump())

# Empty text — should raise ValidationError
try:
    bad1 = PreprocessRequest(text="", language="en")
except Exception as e:
    print("\nEmpty text error:", e)

# Wrong language — should raise ValidationError
try:
    bad2 = PreprocessRequest(text="Hello", language="fr")
except Exception as e:
    print("\nBad language error:", e)