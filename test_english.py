from src.services.english_processor import process_english

# Test 1: Full pipeline
text = "The students are Running quickly! They scored 95 points."
options = {
    "normalize": True,
    "remove_punctuation": True,
    "remove_numbers": True,
    "remove_stopwords": True,
    "lemmatize": True,
}

result, steps = process_english(text, options)
print("Result:", result)
print("Steps:", steps)

# Test 2: No options — text should stay the same
text2 = "Hello World!"
result2, steps2 = process_english(text2, {})
print("\nResult2:", result2)
print("Steps2:", steps2)

# Test 3: Only stemming
text3 = "The cats are playing with running dogs"
result3, steps3 = process_english(text3, {"stemming": True})
print("\nResult3:", result3)
print("Steps3:", steps3)

