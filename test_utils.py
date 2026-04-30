from src.utils.cleaning import (
    remove_punctuation,
    remove_numbers,
    normalize_whitespace,
)

# Test English punctuation
text1 = "Hello, world! How are you?"
print(remove_punctuation(text1))
# Expected: "Hello world How are you"

# Test Arabic punctuation
text2 = "مرحبا، كيف حالك؟"
print(remove_punctuation(text2))
# Expected: "مرحبا كيف حالك"

# Test mixed numbers
text3 = "الطلب رقم 123 والكود ٤٥٦"
print(remove_numbers(text3))
# Expected: "الطلب رقم  والكود "

# Test whitespace cleanup
text4 = "Hello    world   test"
print(normalize_whitespace(text4))
# Expected: "Hello world test"