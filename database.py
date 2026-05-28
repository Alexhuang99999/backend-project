import sqlite3

# 连接数据库
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# 创建用户表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        email TEXT
    )
""")

conn.commit()
print("数据库创建成功！")

# 插入一条用户数据
cursor.execute("""
    INSERT INTO users (name, age, email)
    VALUES (?, ?, ?)
""", ("小明", 25, "xiaoming@gmail.com"))

conn.commit()
print("添加成功！")

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(user)

cursor.execute("""
    UPDATE users
    SET age = 30
    WHERE id = 1
""")

conn.commit()
print("修改成功！")

# 查询确认修改了
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(user)

cursor.execute("""
    DELETE FROM users
    WHERE id = 3
""")

conn.commit()
print("删除成功！")

# 查询确认删除了
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(user)