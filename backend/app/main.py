from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import os
import logging
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Capstone Backend API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "innovation.c3m2emiiu9qh.eu-west-1.rds.amazonaws.com"),
    "port": os.getenv("DB_PORT", "3306"),
    "database": os.getenv("DB_NAME", "capstone"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "EEbY2M:M1d(TId_ba.OB)65zqo(C"),
}

# In-memory storage as fallback
IN_MEMORY_ITEMS = [
    {"id": 1, "name": "Sample Item 1", "description": "This is a sample item", "created_at": datetime.now()},
    {"id": 2, "name": "Sample Item 2", "description": "Another sample item", "created_at": datetime.now()},
    {"id": 3, "name": "Sample Item 3", "description": "Yet another sample item", "created_at": datetime.now()},
]
NEXT_ID = 4
USE_IN_MEMORY = False  # Flag to track if using in-memory storage

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    environment: str
    storage_mode: str

# Database connection helper with retries
def get_db_connection(retries: int = 3, delay: int = 2):
    """Try to connect to database with retries"""
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            logger.info("Database connection successful")
            return conn
        except Exception as e:
            logger.warning(f"Database connection failed (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    return None

# Initialize database table (gracefully handles failures)
def init_db():
    """
    Try to initialize database table.
    If it fails, app will use in-memory storage instead.
    """
    global USE_IN_MEMORY
    
    try:
        conn = get_db_connection(retries=2, delay=1)
        if not conn:
            logger.warning("Database connection failed. Using in-memory storage.")
            USE_IN_MEMORY = True
            return
        
        cursor = conn.cursor()
        
        # Try to create table (will fail if no permissions, which is okay)
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Check if table has data
            cursor.execute("SELECT COUNT(*) FROM items")
            count = cursor.fetchone()[0]
            
            if count == 0:
                sample_items = [
                    ("Sample Item 1", "This is a sample item"),
                    ("Sample Item 2", "Another sample item"),
                    ("Sample Item 3", "Yet another sample item"),
                ]
                cursor.executemany(
                    "INSERT INTO items (name, description) VALUES (%s, %s)",
                    sample_items
                )
            
            conn.commit()
            logger.info("Database initialized successfully")
            USE_IN_MEMORY = False
            
        except psycopg2.Error as db_error:
            logger.warning(f"Database initialization failed (no CREATE permissions?): {db_error}")
            logger.info("Using in-memory storage instead")
            USE_IN_MEMORY = True
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.info("Falling back to in-memory storage")
        USE_IN_MEMORY = True

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up backend API...")
    init_db()
    storage_mode = "in-memory" if USE_IN_MEMORY else "database"
    logger.info(f"Storage mode: {storage_mode}")

# Health endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    conn = get_db_connection(retries=1, delay=0)
    db_status = "connected" if conn else "disconnected"
    
    if conn:
        conn.close()
    
    storage_mode = "in-memory" if USE_IN_MEMORY else "database"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        database=db_status,
        environment=os.getenv("ENVIRONMENT", "production"),
        storage_mode=storage_mode
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    storage_mode = "in-memory" if USE_IN_MEMORY else "database"
    return {
        "message": "Capstone Backend API",
        "version": "1.0.0",
        "storage_mode": storage_mode,
        "endpoints": {
            "health": "/health",
            "items": "/items",
            "item_by_id": "/items/{id}",
            "create_item": "POST /items",
        }
    }

# Get all items (works with both database and in-memory)
@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items from database or in-memory storage"""
    
    # Use in-memory storage if database not available
    if USE_IN_MEMORY:
        return [Item(**item) for item in IN_MEMORY_ITEMS]
    
    # Try database
    conn = get_db_connection(retries=1, delay=0)
    if not conn:
        # Fallback to in-memory
        logger.info("Database unavailable, using in-memory storage")
        return [Item(**item) for item in IN_MEMORY_ITEMS]
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, created_at FROM items ORDER BY id")
        rows = cursor.fetchall()
        
        items = [
            Item(
                id=row[0],
                name=row[1],
                description=row[2],
                created_at=row[3]
            )
            for row in rows
        ]
        
        cursor.close()
        conn.close()
        
        return items
    except Exception as e:
        logger.error(f"Error fetching items from database: {e}")
        # Fallback to in-memory
        return [Item(**item) for item in IN_MEMORY_ITEMS]

# Get single item
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a single item by ID"""
    
    # Use in-memory storage if database not available
    if USE_IN_MEMORY:
        item = next((item for item in IN_MEMORY_ITEMS if item["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item(**item)
    
    # Try database
    conn = get_db_connection(retries=1, delay=0)
    if not conn:
        # Fallback to in-memory
        item = next((item for item in IN_MEMORY_ITEMS if item["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item(**item)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, description, created_at FROM items WHERE id = %s",
            (item_id,)
        )
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return Item(
            id=row[0],
            name=row[1],
            description=row[2],
            created_at=row[3]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching item: {e}")
        # Fallback to in-memory
        item = next((item for item in IN_MEMORY_ITEMS if item["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item(**item)

# Create item
@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    global NEXT_ID
    
    # Use in-memory storage if database not available
    if USE_IN_MEMORY:
        new_item = {
            "id": NEXT_ID,
            "name": item.name,
            "description": item.description,
            "created_at": datetime.now()
        }
        IN_MEMORY_ITEMS.append(new_item)
        NEXT_ID += 1
        return Item(**new_item)
    
    # Try database
    conn = get_db_connection(retries=1, delay=0)
    if not conn:
        # Fallback to in-memory
        new_item = {
            "id": NEXT_ID,
            "name": item.name,
            "description": item.description,
            "created_at": datetime.now()
        }
        IN_MEMORY_ITEMS.append(new_item)
        NEXT_ID += 1
        return Item(**new_item)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, created_at",
            (item.name, item.description)
        )
        result = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return Item(
            id=result[0],
            name=item.name,
            description=item.description,
            created_at=result[1]
        )
    except Exception as e:
        logger.error(f"Error creating item in database: {e}")
        # Fallback to in-memory
        new_item = {
            "id": NEXT_ID,
            "name": item.name,
            "description": item.description,
            "created_at": datetime.now()
        }
        IN_MEMORY_ITEMS.append(new_item)
        NEXT_ID += 1
        return Item(**new_item)

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item by ID"""
    
    # Use in-memory storage if database not available
    if USE_IN_MEMORY:
        item = next((item for item in IN_MEMORY_ITEMS if item["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        IN_MEMORY_ITEMS.remove(item)
        return {"message": "Item deleted successfully", "id": item_id}
    
    # Try database
    conn = get_db_connection(retries=1, delay=0)
    if not conn:
        # Fallback to in-memory
        item = next((item for item in IN_MEMORY_ITEMS if item["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        IN_MEMORY_ITEMS.remove(item)
        return {"message": "Item deleted successfully", "id": item_id}
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s RETURNING id", (item_id,))
        result = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {"message": "Item deleted successfully", "id": item_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item from database: {e}")
        # Fallback to in-memory
        item = next((item for item in IN_MEMORY_ITEMS if item["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        IN_MEMORY_ITEMS.remove(item)
        return {"message": "Item deleted successfully", "id": item_id}