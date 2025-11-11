import streamlit as st
import pandas as pd

from nlp import load_model
from database import init_db, add_message, get_history

def main():
    """
    Hàm chính của ứng dụng
    """
    
    st.title("Trợ Lý Phân Loại Cảm Xúc Tiếng Việt")
    st.write("Xây dựng dựa trên mô hình Transformer phân loại cảm xúc")
    
    # 1. Tải mô hình
    classifier = load_model()
    
    # 2. Khởi tạo database
    init_db()
    
    # Nếu mô hình chưa tỉa thì dừng
    if not classifier:
        st.error("Không thể tải mô hình. Vui lòng kiểm tra lại!")
        return

    # 3. Giao diện nhập 
    with st.form("sentiment_form"):
        user_input = st.text_area("Nhập câu văn của bạn để phân loại (tối thiếu 5 ký tự)", height=100, placeholder="Ví dụ: Món ăn này dở quá")
        
        submit_button = st.form_submit_button("Phân loại")
    
    # 4. Xử lý khi ấn nut
    if submit_button:
        # Kiểm tra đầu vào (theo yêu cầu của đồ án)
        if len(user_input) < 5:
            st.warning("Vui lòng nhập ít nhất 5 ký tự.")
        elif len(user_input) > 256: 
             st.warning("Vui lòng nhập dưới 256 ký tự.")
        else:
            with st.spinner("Đang phân tích..."):
                try:
                    result = classifier(user_input)
                    raw_result = result[0]
                    label = raw_result["label"].upper()
                    score = raw_result["score"]
                    if score < 0.5:
                        sentiment = "NEUTRAL"
                    else: 
                        sentiment = label 
                    
                    # Hiển thị kết quả
                    st.subheader("Kết quả phân loại:")
                    if sentiment == "POS":
                        st.success(f"Tích cực (POSITIVE) - Độ tin cậy: {score:.5f}")
                        sentiment = "POSITIVE"
                    elif sentiment == "NEG":
                        st.error(f"Tiêu cực (NEGATIVE) - Độ tin cậy: {score:.5f}")
                        sentiment = "NEGATIVE"
                    else:
                        st.info(f"Trung tính (NEUTRAL) - Độ tin cậy: {score:.5f}")
                        sentiment = "NEUTRAL"
                    # Lưu vào CSDL
                    add_message(user_input, sentiment , score)

                except Exception as e:
                    st.error(f"Đã xảy ra lỗi khi xử lý: {e}")

    # 5. Hiển thị lịch sử
    st.subheader("Lịch sử phân loại (50 lần gần nhất)")
    
    history_data = get_history(limit=50)
    
    if not history_data:
        st.info("Chưa có lịch sử phân loại nào.")
    else:
        # Dùng Pandas DataFrame để hiển thị bảng cho đẹp
        df = pd.DataFrame(history_data, columns=[ "Văn bản đã nhập", "Cảm xúc", "Độ tin cậy", "Thời gian"])
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()