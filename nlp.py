import streamlit as st
from transformers import pipeline 

@st.cache_resource
def load_model():
    """
    Tải và cache mô hình Transformer phân loại cảm xúc
    Chỉ chạy một lần và sử dụng lại cho các lần sau
    """
    
    model_name = '5CD-AI/Vietnamese-Sentiment-visobert'
    st.write(f"Tải mô hình từ {model_name}...")
    
    try:
        classifier = pipeline("text-classification", model=model_name, tokenizer=model_name)
        st.success("Mô hình đã được tải thành công!")
        return classifier
    except Exception as e:
        st.error(f"Lỗi khi tải mô hình: {e}")
        return None
