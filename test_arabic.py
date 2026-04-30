from src.services.arabic_processor import process_arabic

# Test 1: Full pipeline
text = "الطُّلابُ يَدرُسُونَ فِي الجَامِعَةِ!! العدد ١٢٣"
options = {
    "normalize": True,
    "remove_punctuation": True,
    "remove_numbers": True,
    "remove_stopwords": True,
}

result, steps = process_arabic(text, options)
print("Result:", result)
print("Steps:", steps)

# Test 2: Negation protection
text2 = "هذا المنتج ليس جيداً"
options2 = {"normalize": True, "remove_stopwords": True}

result2, steps2 = process_arabic(text2, options2)
print("\nResult2:", result2)
print("Steps2:", steps2)
print("'ليس' preserved?", "ليس" in result2)

# Test 3: Tatweel removal
text3 = "كتـــــاب جميـــــل"
options3 = {"normalize": True}

result3, steps3 = process_arabic(text3, options3)
print("\nResult3:", result3)
print("Steps3:", steps3)