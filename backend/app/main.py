from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import pymysql
import os
import logging
import time

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Capstone Backend API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL configuration (3306)
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# In-memory fallback
USE_IN_MEMORY = False
IN_MEMORY_ITEMS = []
NEXT_ID = 1


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


class HealthResponse(BaseModel):
    status: str
    database: str
    environment: str
    storage_mode: str
    timestamp: datetime


def get_db_connection(retries: int = 3, delay: int = 2):
    for attempt in range(retries):
        try:
            return pymysql.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
            )
        except Exception as e:
            logger.warning(f"DB connection failed ({attempt+1}/{retries}): {e}")
            time.sleep(delay)
    return None


def init_db():
    global USE_IN_MEMORY
    conn = get_db_connection()
    if not conn:
        USE_IN_MEMORY = True
        logger.warning("Using in-memory storage")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
        USE_IN_MEMORY = False
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"DB init failed: {e}")
        USE_IN_MEMORY = True
    finally:
        conn.close()


@app.on_event("startup")
async def startup():
    logger.info("Backend starting...")
    init_db()


@app.get("/health", response_model=HealthResponse)
async def health():
    conn = get_db_connection(retries=1, delay=0)
    db_status = "connected" if conn else "disconnected"
    if conn:
        conn.close()

    return HealthResponse(
        status="healthy",
        database=db_status,
        environment=os.getenv("ENVIRONMENT", "production"),
        storage_mode="in-memory" if USE_IN_MEMORY else "database",
        timestamp=datetime.utcnow(),
    )


@app.get("/items", response_model=List[Item])
async def get_items():
    if USE_IN_MEMORY:
        return IN_MEMORY_ITEMS

    conn = get_db_connection(retries=1, delay=0)
    if not conn:
        return IN_MEMORY_ITEMS

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM items ORDER BY id")
        rows = cursor.fetchall()

    conn.close()
    return rows


@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    global NEXT_ID

    if USE_IN_MEMORY:
        new_item = {
            "id": NEXT_ID,
            "name": item.name,
            "description": item.description,
            "created_at": datetime.utcnow(),
        }
        NEXT_ID += 1
        IN_MEMORY_ITEMS.append(new_item)
        return new_item

    conn = get_db_connection(retries=1, delay=0)
    if not conn:
        raise HTTPException(status_code=500, detail="Database unavailable")

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s)",
            (item.name, item.description),
        )
        conn.commit()
        item_id = cursor.lastrowid

    conn.close()
    return {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "created_at": datetime.utcnow(),
    }
