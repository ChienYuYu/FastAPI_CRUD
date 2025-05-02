import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# 連接SQLite資料庫 & 建立資料表
conn = sqlite3.connect('posts.db', check_same_thread=False)
cursor = conn.cursor()

# 建立posts資料表(如果尚未建立)
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT TRUE
)
""")
conn.commit()


#===============================
class Post(BaseModel):
  id: Optional[int] = None
  title:str
  content:str
  published: bool = True # 沒帶published參數就預設給true

@app.get('/')
def read_root():
  return '安安你好'

# 取得所有Post
@app.get('/posts')
def readPosts():
  cursor.execute("SELECT * FROM posts")
  posts = cursor.fetchall()
  posts_arr = []
  for post in posts:
    post_dict = {
      "id": post[0],
      "title": post[1],
      "content": post[2],
      "published": post[3]
    }
    posts_obj.append(post_dict)
 
  return {"Status": "success", "Posts": posts_arr}

# 取得單筆Post
@app.get('/posts/{id}')
def getPost(id: int):
  cursor.execute("SELECT * FROM posts WHERE id = ?",(id,))
  post = cursor.fetchone()
  if post:
    post_dict = {
      "id": post[0],
      "title": post[1],
      "content": post[2],
      "published": post[3]
    }
    return {'Post': post_dict}
  else:
    return {"msg": "查無資料"}

# 新增Post
@app.post('/createpost')
def createPost(post:Post):
  cursor.execute("INSERT INTO posts (title, content, published) VALUES(?,?,?)",
                  (post.title, post.content, post.published))
  conn.commit()
  return {'Status':'success', "post":post.dict()}

# 修改post
@app.put('/posts/{id}')
def editP(id: int, post:Post):
  cursor.execute("UPDATE posts SET title = ?, content = ?, published = ? WHERE id = ?",
                  (post.title, post.content, post.published, id))
  conn.commit()
  return {'msg': f'{id}已修改'}


# 刪除post
@app.delete('/posts/{id}')
def dPost(id: int):
  cursor.execute("DELETE FROM posts WHERE id = ?",(id,))
  conn.commit()
  return {"msg": f"{id}已刪除"}