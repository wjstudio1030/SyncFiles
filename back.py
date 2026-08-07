from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# 1. 設定資料庫連線位置
DATABASE_URL = "postgresql://postgres:KenKen960622@localhost:5432/web_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 定義資料庫欄位
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# 讓程式啟動時，自動去資料庫建立表格
Base.metadata.create_all(bind=engine)

# 3. 建立資料庫連線的工具函式
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- 以下是網頁 API 的路徑設定 (CRUD) ----

# 【C】reate：手動新增一個使用者到資料庫
@app.post("/users/add")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    new_user = UserDB(name=name, email=email)
    db.add(new_user)
    db.commit()          # 確認寫入資料庫
    db.refresh(new_user) # 刷新資料
    return {"status": "成功寫入！", "user": new_user}

# 【R】ead：撈取資料庫裡所有的使用者
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

# 【R】ead：指定撈取某一個 ID 的使用者
@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="找不到該使用者")
    return user

# 【U】pdate：修改指定 ID 的使用者資料
@app.put("/users/update/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    # 先去資料庫把這個人找出來
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="找不到該使用者，無法修改")
    
    # 修改資料
    user.name = name
    user.email = email
    
    db.commit()   # 存檔
    db.refresh(user)
    return {"status": "修改成功！", "user": user}

# 【D】elete：刪除指定 ID 的使用者
@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 先去資料庫把這個人找出來
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="找不到該使用者，無法刪除")
    
    # 刪除資料
    db.delete(user)
    db.commit()   # 存檔
    return {"status": f"成功刪除 ID 為 {user_id} 的使用者！"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run("back:app", host="0.0.0.0", port=8000, reload=True)