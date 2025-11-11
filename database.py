import sqlite3
from datetime import datetime

DB_FILE = "sentiment_history.db"

def init_db():
    """
    Khởi tạo database và bảng lưu lịch sử trò chuyện
    
    """
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_message(text, sentiment , score):
    """
    Thêm tin nhắn vào database
    """
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    try:
        c.execute('''
            INSERT INTO history (text, sentiment, score, timestamp) VALUES (?, ?, ?, ?)
        ''', (text, sentiment, score, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm tin nhắn vào database: {e}")
    finally:
        conn.close()
        
def get_history(limit = 50):
    """
    Lấy lịch sử trò chuyện từ database
    """
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f'''
        SELECT text, sentiment, score, timestamp FROM history ORDER BY timestamp DESC LIMIT {limit}
    ''')
    history = c.fetchall()
    conn.close()
    return history