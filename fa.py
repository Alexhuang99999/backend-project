import pymysql
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# 密钥
SECRET_KEY = "alexhuang888secretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 连接 MySQL
def get_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Alexhuang888",
        database="shopdb"
    )
    return conn

# 初始化数据库
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            email VARCHAR(100),
            password VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 数据结构
class User(BaseModel):
    name: str
    age: int
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

# 生成 Token
def create_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expire}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 验证 Token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token无效")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token无效")

# 注册接口
@app.post("/register")
def register(user: User):
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    )
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, age, email, password)
        VALUES (%s, %s, %s, %s)
    """, (user.name, user.age, user.email, hashed_password))
    conn.commit()
    conn.close()
    return {"message": f"注册成功！欢迎，{user.name}"}

# 登录接口
@app.post("/login")
def login(data: Login):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (data.email,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return {"message": "用户不存在"}

    if bcrypt.checkpw(data.password.encode("utf-8"), user[4]):
        token = create_token(data.email)
        return {
            "message": f"登录成功！欢迎回来，{user[1]}",
            "token": token
        }
    else:
        return {"message": "密码错误"}

# 查询所有用户（需要 Token）
@app.get("/users")
def get_users(current_user: str = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": users}