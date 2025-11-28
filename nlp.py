import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os

@st.cache_resource
def load_model():
    """
    Tải và cache mô hình Transformer.
    Cơ chế thông minh:
    1. Kiểm tra xem thư mục model_local có tồn tại không.
    2. Nếu KHÔNG (lần đầu chạy): Tự động tải từ HuggingFace về và LƯU vào model_local.
    3. Nếu CÓ (lần sau chạy): Load trực tiếp từ model_local (nhanh, offline).
    """
    
    # Cấu hình đường dẫn và tên model
    local_path = "./model_local"
    online_model = "5CD-AI/Vietnamese-Sentiment-visobert"
    
    # --- TRƯỜNG HỢP 1: Model chưa được tải về máy ---
    if not os.path.exists(local_path):
        st.warning(f"⚠️ Chưa tìm thấy mô hình offline. Hệ thống đang tự động tải model '{online_model}' về máy...")
        st.info("⏳ Quá trình này chỉ diễn ra 1 lần duy nhất, vui lòng đợi trong giây lát (khoảng 100-300MB)...")
        
        try:
            # 1. Tải Tokenizer và Model từ HuggingFace
            tokenizer = AutoTokenizer.from_pretrained(online_model)
            model = AutoModelForSequenceClassification.from_pretrained(online_model)
            
            # 2. Lưu vào thư mục local để dùng cho lần sau
            os.makedirs(local_path, exist_ok=True)
            tokenizer.save_pretrained(local_path)
            model.save_pretrained(local_path)
            
            st.success(f"✅ Đã tải và lưu mô hình vào '{local_path}' thành công!")
            
            # Sau khi lưu xong, gán nguồn là local
            model_source = local_path
            
        except Exception as e:
            st.error(f"❌ Lỗi khi tải model từ mạng: {e}")
            # Nếu tải lỗi, thử dùng online trực tiếp như phương án dự phòng cuối cùng
            model_source = online_model
            
    # --- TRƯỜNG HỢP 2: Model đã có sẵn trong máy ---
    else:
        st.write(f"📂 Đang nạp mô hình từ bộ nhớ máy (Offline): {local_path}...")
        model_source = local_path

    # --- KHỞI TẠO PIPELINE ---
    try:
        # Tạo pipeline phân loại
        classifier = pipeline("sentiment-analysis", model=model_source)
        st.success("✅ Mô hình đã sẵn sàng!")
        return classifier
        
    except Exception as e:
        st.error(f"❌ Lỗi nghiêm trọng khi khởi tạo pipeline: {e}")
        return None