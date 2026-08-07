from sqlalchemy import create_engine

# 資料庫連線字串格式：postgresql://帳號:密碼@主機位置:埠號/資料庫名稱
# 請把 'mysecretpassword' 換成你剛剛在步驟二設定的密碼
DATABASE_URL = "postgresql://postgres:KenKen960622@localhost:5432/web_db"

try:
    # 建立資料庫引擎並嘗試連接
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("🎉 恭喜你！Python 成功連上 PostgreSQL 資料庫了！")
    connection.close()
except Exception as e:
    print("❌ 連線失敗，錯誤訊息如下：")
    print(e)