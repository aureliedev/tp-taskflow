import os
import time
import psycopg
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

def conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST","postgres"),
        port=os.getenv("DB_PORT","5432"),
        dbname=os.getenv("DB_NAME","taskflow"),
        user=os.getenv("DB_USER","taskflow"),
        password=os.getenv("DB_PASSWORD","taskflow"),
    )

def init_db():
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT DEFAULT '',
                status VARCHAR(30) NOT NULL DEFAULT 'todo'
            )""")
        c.commit()

@asynccontextmanager
async def lifespan(app):
    for attempt in range(30):
        try:
            init_db()
            break
        except Exception as e:
            print(f"Database not ready yet (attempt {attempt+1}/30):", e)
            time.sleep(2)
    yield

app=FastAPI(title="TaskFlow API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

class TaskCreate(BaseModel):
    title:str
    description:str=""

class TaskUpdate(BaseModel):
    status:str

@app.get("/api/health")
def health():
    return {"status":"ok","service":"taskflow-api"}

@app.get("/api/tasks")
def tasks():
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT id,title,description,status FROM tasks ORDER BY id DESC")
            rows=cur.fetchall()
    return [{"id":r[0],"title":r[1],"description":r[2],"status":r[3]} for r in rows]

@app.post("/api/tasks",status_code=201)
def create(t:TaskCreate):
    if not t.title.strip():
        raise HTTPException(400,"Title is required")
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO tasks(title,description) VALUES(%s,%s) RETURNING id,title,description,status",
                        (t.title.strip(),t.description.strip()))
            r=cur.fetchone()
        c.commit()
    return {"id":r[0],"title":r[1],"description":r[2],"status":r[3]}

@app.patch("/api/tasks/{task_id}")
def update(task_id:int,t:TaskUpdate):
    if t.status not in {"todo","doing","done"}:
        raise HTTPException(400,"Invalid status")
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("UPDATE tasks SET status=%s WHERE id=%s RETURNING id,title,description,status",
                        (t.status,task_id))
            r=cur.fetchone()
        c.commit()
    if not r: raise HTTPException(404,"Task not found")
    return {"id":r[0],"title":r[1],"description":r[2],"status":r[3]}

@app.delete("/api/tasks/{task_id}",status_code=204)
def delete(task_id:int):
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id=%s",(task_id,))
        c.commit()
