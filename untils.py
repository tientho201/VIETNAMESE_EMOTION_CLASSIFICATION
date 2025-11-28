import re
import json

try:
    with open('teen_code.json', 'r', encoding='utf-8') as f:
        teen_code = json.load(f)
except Exception as e:
    print(f"Error loading teencode: {e}")
    teen_code = {}


def preprocess_text(text):
    """
        Hàm tiền xử lý văn bản:
        1. Chuyển về chữ thường.
        2. Chuẩn hóa ký tự lặp.
        3. Thay thế Teencode & Icon.
        4. Loại bỏ ký tự đặc biệt (sau khi đã xử lý icon).
        5. Chuẩn hóa khoảng trắng.
    """
    if not text:
        return ""

    text = text.lower()
    
    text = re.sub(r'([a-z])\1{2,}', r'\1', text)
    
    words = text.split()
    processed_words = [teen_code.get(word, word) for word in words]
    text = " ".join(processed_words)
    
    text = re.sub(r'[^\w\s]', '', text)
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


