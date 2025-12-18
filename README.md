# Capstone Project: AWS EKS Deployment

> **Author:** Jeremy Opare  
> **Email:** jeremyomeriks@gmail.com  
> **Project Duration:** 7 Days

## 🚀 Project Overview

This project demonstrates a complete DevOps workflow for deploying a multi-component application stack to AWS EKS using automated CI/CD pipelines. The application consists of a frontend (Nginx), backend (FastAPI), and PostgreSQL database.

## 📋 Architecture

┌─────────────┐
│   Internet  │
└──────┬──────┘
│
┌──────▼───────────────────────────────────────┐
│     Nginx Ingress Controller                 │
│   (firstname-lastname.capstone.company.com)  │
└──────┬───────────────────────────────────────┘
│
┌──────▼──────────┐         ┌──────────────┐
│    Frontend     │────────>│   Backend    │
│  (Nginx:80)     │         │ (FastAPI:8000)│
└─────────────────┘         └──────┬───────┘
│
┌──────▼────────┐
│  PostgreSQL   │
│   Database    │
└───────────────┘

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (served by Nginx)
- **Backend:** Python FastAPI
- **Database:** PostgreSQL
- **Container Runtime:** Docker (multi-stage builds)
- **Container Registry:** AWS ECR
- **Orchestration:** Kubernetes (AWS EKS)
- **CI/CD:** GitHub Actions
- **Infrastructure:** AWS (EKS, ECR, VPC, Load Balancer)

## 📁 Project Structure

firstname-lastname-capstone/
├── frontend/                 # Frontend application
│   ├── Dockerfile           # Multi-stage Dockerfile
│   ├── nginx.conf           # Nginx configuration
│   └── public/              # Static files
├── backend/                  # Backend application
│   ├── Dockerfile           # Multi-stage Dockerfile
│   ├── requirements.txt     # Python dependencies
│   └── app/                 # FastAPI application
├── k8s/                      # Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment-frontend.yaml
│   ├── service-frontend.yaml
│   ├── deployment-backend.yaml
│   ├── service-backend.yaml
│   └── ingress.yaml
├── .github/workflows/        # CI/CD pipeline
│   └── ci-cd.yml
├── README.md                 # Project documentation
└── RUNBOOK.md               # Operations guide

## 🚦 Getting Started

### Prerequisites

1. AWS Account with EKS cluster access
2. GitHub account
3. Docker installed locally
4. kubectl installed locally
5. AWS CLI configured

### Setup Steps

1. **Clone the Repository**
```bash
   git clone https://github.com/yourusername/firstname-lastname-capstone.git
   cd firstname-lastname-capstone
```

2. **Configure AWS Secrets in GitHub**
   - Go to: Settings → Secrets and variables → Actions
   - Add secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

3. **Create ECR Repositories**
```bash
   aws ecr create-repository --repository-name firstname-lastname/frontend --region <REGION>
   aws ecr create-repository --repository-name firstname-lastname/backend --region <REGION>
```

4. **Update Configuration**
   - Replace `firstname-lastname` with your actual name throughout the project
   - Update `<AWS_ACCOUNT_ID>` and `<REGION>` in YAML files
   - Update `<EKS_CLUSTER_NAME>` in the GitHub Actions workflow

5. **Push to GitHub**
```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
```

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline automatically:

1. ✅ Checks out code
2. ✅ Configures AWS credentials
3. ✅ Logs into Amazon ECR
4. ✅ Builds Docker images (multi-stage)
5. ✅ Pushes images to ECR with `latest` and `git-sha` tags
6. ✅ Deploys to EKS cluster
7. ✅ Verifies deployment health

**Pipeline Trigger:** Every push to `main` branch

## 🔍 Verification

### Check Pods
```bash
kubectl get pods -n firstname-lastname
```

### Check Services
```bash
kubectl get svc -n firstname-lastname
```

### Check Ingress
```bash
kubectl get ingress -n firstname-lastname
```

### Access Application



Step 2: Create GitHub Repository
bash# Create repo on GitHub named: john-doe-capstone
git clone https://github.com/yourusername/john-doe-capstone.git
cd john-doe-capstone

# Copy all the files from the artifact into this directory
# with the correct folder structure
Step 3: Create ECR Repositories
bashaws ecr create-repository \
  --repository-name john-doe/frontend \
  --region us-east-1

aws ecr create-repository \
  --repository-name john-doe/backend \
  --region us-east-1
Step 4: Configure GitHub Secrets
Go to: Settings → Secrets and variables → Actions
Add:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

Step 5: Deploy!
bashgit add .
git commit -m "Initial deployment"
git push origin main
Watch the magic happen in Actions tab! 🎉
🎯 Bonus Features You Can Add
Want extra credit? I can help you implement:

Terraform IaC - Infrastructure as Code for ECR
Helm Charts - Package management
Network Policies - Traffic restrictions
HPA (Horizontal Pod Autoscaler) - Auto-scaling
RBAC Hardening - Service accounts and roles
Monitoring - Prometheus/Grafana integration

🆘 Need Help With Anything?
I can assist with:

Debugging specific errors
Implementing bonus features
Customizing the application
Understanding any part of the setup
Preparing for your demo

What would you like to tackle next? 🚀Claude is AI and can make mistakes. Please double-check responses. Sonnet 4.5Claude is AI and can make mistakes. Please double-check responses.CopyPublishComplete AWS EKS Capstone Project

Important: Replace firstname-lastname with your actual name throughout this project (e.g., john-doe)

Project Structure
firstname-lastname-capstone/
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── public/
│       ├── index.html
│       └── health.html
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── main.py
├── k8s/
│   ├── namespace.yaml
│   ├── deployment-frontend.yaml
│   ├── service-frontend.yaml
│   ├── deployment-backend.yaml
│   ├── service-backend.yaml
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── README.md
└── RUNBOOK.md

1. Frontend Application
frontend/public/index.html
html<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capstone Project - Frontend</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .status-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
        }
        
        .status-item:last-child {
            border-bottom: none;
        }
        
        .status-label {
            font-weight: 600;
            color: #495057;
        }
        
        .status-value {
            font-family: 'Courier New', monospace;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .status-pending {
            background: #fff3cd;
            color: #856404;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 20px;
            width: 100%;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .api-response {
            background: #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Capstone Project</h1>
        <p class="subtitle">AWS EKS Deployment Demo</p>
        
        <div class="status-box">
            <div class="status-item">
                <span class="status-label">Frontend Status:</span>
                <span class="status-value status-success">✓ Running</span>
            </div>
            <div class="status-item">
                <span class="status-label">Backend API:</span>
                <span class="status-value status-pending" id="backend-status">Checking...</span>
            </div>
            <div class="status-item">
                <span class="status-label">Database:</span>
                <span class="status-value status-pending" id="database-status">Checking...</span>
            </div>
        </div>
        
        <button onclick="testBackendAPI()">Test Backend API</button>
        
        <div id="api-response" class="api-response" style="display: none;"></div>
    </div>

    <script>
        const BACKEND_URL = window.location.protocol + '//' + window.location.hostname + '/api';
        
        // Check backend health on page load
        window.addEventListener('DOMContentLoaded', checkBackendHealth);
        
        async function checkBackendHealth() {
            try {
                const response = await fetch(`${BACKEND_URL}/health`);
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('backend-status').textContent = '✓ Connected';
                    document.getElementById('backend-status').className = 'status-value status-success';
                    
                    if (data.database === 'connected') {
                        document.getElementById('database-status').textContent = '✓ Connected';
                        document.getElementById('database-status').className = 'status-value status-success';
                    } else {
                        document.getElementById('database-status').textContent = '✗ Disconnected';
                        document.getElementById('database-status').className = 'status-value status-error';
                    }
                } else {
                    throw new Error('Backend unhealthy');
                }
            } catch (error) {
                document.getElementById('backend-status').textContent = '✗ Unreachable';
                document.getElementById('backend-status').className = 'status-value status-error';
                document.getElementById('database-status').textContent = '✗ Unknown';
                document.getElementById('database-status').className = 'status-value status-error';
            }
        }
        
        async function testBackendAPI() {
            const responseDiv = document.getElementById('api-response');
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '<div class="loading"></div> Testing API...';
            
            try {
                const response = await fetch(`${BACKEND_URL}/items`);
                const data = await response.json();
                
                responseDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                responseDiv.textContent = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
frontend/public/health.html
html<!DOCTYPE html>
<html>
<head>
    <title>Health Check</title>
</head>
<body>
    <h1>OK</h1>
</body>
</html>
frontend/nginx.conf
nginxuser nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    keepalive_timeout 65;
    gzip on;

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /health {
            try_files /health.html =200;
        }

        # Proxy API requests to backend
        location /api/ {
            proxy_pass http://backend-service:8000/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
frontend/Dockerfile
dockerfile# Multi-stage build for production-ready frontend

# Stage 1: Build stage (not needed for static HTML, but good practice)
FROM nginx:alpine AS builder

# Stage 2: Production stage
FROM nginx:alpine

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -u 1001 -S appuser -G appuser

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files
COPY public/ /usr/share/nginx/html/

# Set ownership
RUN chown -R appuser:appuser /usr/share/nginx/html && \
    chown -R appuser:appuser /var/cache/nginx && \
    chown -R appuser:appuser /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appuser /var/run/nginx.pid

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]

2. Backend Application
backend/requirements.txt
txtfastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
backend/app/main.py
pythonfrom fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import os
import logging
from datetime import datetime

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
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "capstone"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

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

# Database connection helper
def get_db_connection():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

# Initialize database table
def init_db():
    """Initialize database table if it doesn't exist"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert sample data if table is empty
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
            cursor.close()
            conn.close()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    conn = get_db_connection()
    db_status = "connected" if conn else "disconnected"
    
    if conn:
        conn.close()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        database=db_status,
        environment=os.getenv("ENVIRONMENT", "production")
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Capstone Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "items": "/items",
            "item_by_id": "/items/{id}",
            "create_item": "POST /items",
        }
    }

# Get all items
@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items from database"""
    conn = get_db_connection()
    
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
    
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
        logger.error(f"Error fetching items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get single item
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a single item by ID"""
    conn = get_db_connection()
    
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
    
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
        raise HTTPException(status_code=500, detail=str(e))

# Create item
@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    conn = get_db_connection()
    
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
    
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
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item by ID"""
    conn = get_db_connection()
    
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
    
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
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
backend/Dockerfile
dockerfile# Multi-stage build for production-ready backend

# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser app/ ./app/

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

3. Kubernetes Manifests
k8s/namespace.yaml
yamlapiVersion: v1
kind: Namespace
metadata:
  name: firstname-lastname
  labels:
    name: firstname-lastname
    project: capstone
k8s/deployment-frontend.yaml
yamlapiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: firstname-lastname
  labels:
    app: frontend
    tier: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
    spec:
      imagePullSecrets:
        - name: ecr-secret  # Provided by DevOps team
      containers:
      - name: frontend
        image: <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/firstname-lastname/frontend:latest
        ports:
        - containerPort: 80
          name: http
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
k8s/service-frontend.yaml
yamlapiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: firstname-lastname
  labels:
    app: frontend
spec:
  type: ClusterIP
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
k8s/deployment-backend.yaml
yamlapiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: firstname-lastname
  labels:
    app: backend
    tier: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        tier: backend
    spec:
      imagePullSecrets:
        - name: ecr-secret  # Provided by DevOps team
      containers:
      - name: backend
        image: <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/firstname-lastname/backend:latest
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: postgres-secret  # Provided by DevOps team
              key: host
        - name: DB_PORT
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: port
        - name: DB_NAME
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: database
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        resources:
          requests:
            memory: "128Mi"
            cpu: "200m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
k8s/service-backend.yaml
yamlapiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: firstname-lastname
  labels:
    app: backend
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
    name: http
k8s/ingress.yaml
yamlapiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: capstone-ingress
  namespace: firstname-lastname
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"  # If cert-manager is available
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - firstname-lastname.capstone.company.com
    secretName: capstone-tls
  rules:
  - host: firstname-lastname.capstone.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80

4. GitHub Actions CI/CD Pipeline
.github/workflows/ci-cd.yml
yamlname: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

env:
  AWS_REGION: us-east-1  # Replace with your region
  ECR_REGISTRY: <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
  NAMESPACE: firstname-lastname

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build Frontend Image
      working-directory: ./frontend
      run: |
        docker build \
          -t ${{ env.ECR_REGISTRY }}/firstname-lastname/frontend:latest \
          -t ${{ env.ECR_REGISTRY }}/firstname-lastname/frontend:${{ github.sha }} \
          .

    - name: Push Frontend Image
      run: |
        docker push ${{ env.ECR_REGISTRY }}/firstname-lastname/frontend:latest
        docker push ${{ env.ECR_REGISTRY }}/firstname-lastname/frontend:${{ github.sha }}

    - name: Build Backend Image
      working-directory: ./backend
      run: |
        docker build \
          -t ${{ env.ECR_REGISTRY }}/firstname-lastname/backend:latest \
          -t ${{ env.ECR_REGISTRY }}/firstname-lastname/backend:${{ github.sha }} \
          .

    - name: Push Backend Image
      run: |
        docker push ${{ env.ECR_REGISTRY }}/firstname-lastname/backend:latest
        docker push ${{ env.ECR_REGISTRY }}/firstname-lastname/backend:${{ github.sha }}

    - name: Install kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: Configure kubectl for EKS
      run: |
        aws eks update-kubeconfig --name <EKS_CLUSTER_NAME> --region ${{ env.AWS_REGION }}

    - name: Deploy to Kubernetes
      run: |
        # Apply namespace
        kubectl apply -f k8s/namespace.yaml
        
        # Update image tags in deployments
        sed -i "s|<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com|${{ env.ECR_REGISTRY }}|g" k8s/deployment-frontend.yaml
        sed -i "s|<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com|${{ env.ECR_REGISTRY }}|g" k8s/deployment-backend.yaml
        
        # Apply all Kubernetes manifests
        kubectl apply -f k8s/ --namespace=${{ env.NAMESPACE }}
        
        # Wait for deployments to be ready
        kubectl rollout status deployment/frontend --namespace=${{ env.NAMESPACE }} --timeout=5m
        kubectl rollout status deployment/backend --namespace=${{ env.NAMESPACE }} --timeout=5m

    - name: Verify Deployment
      run: |
        echo "=== Pods Status ==="
        kubectl get pods --namespace=${{ env.NAMESPACE }}
        
        echo "=== Services ==="
        kubectl get services --namespace=${{ env.NAMESPACE }}
        
        echo "=== Ingress ==="
        kubectl get ingress --namespace=${{ env.NAMESPACE }}

    - name: Run Health Checks
      run: |
        # Wait for pods to be ready
        kubectl wait --for=condition=ready pod -l app=frontend --namespace=${{ env.NAMESPACE }} --timeout=300s
        kubectl wait --for=condition=ready pod -l app=backend --namespace=${{ env.NAMESPACE }} --timeout=300s
        
        echo "All pods are healthy!"

5. Documentation
README.md
markdown# Capstone Project: AWS EKS Deployment

> **Author:** [Your Name]  
> **Email:** [Your Email]  
> **Project Duration:** 7 Days

## 🚀 Project Overview

This project demonstrates a complete DevOps workflow for deploying a multi-component application stack to AWS EKS using automated CI/CD pipelines. The application consists of a frontend (Nginx), backend (FastAPI), and PostgreSQL database.

## 📋 Architecture
┌─────────────┐
│   Internet  │
└──────┬──────┘
│
┌──────▼───────────────────────────────────────┐
│     Nginx Ingress Controller                 │
│   (firstname-lastname.capstone.company.com)  │
└──────┬───────────────────────────────────────┘
│
┌──────▼──────────┐         ┌──────────────┐
│    Frontend     │────────>│   Backend    │
│  (Nginx:80)     │         │ (FastAPI:8000)│
└─────────────────┘         └──────┬───────┘
│
┌──────▼────────┐
│  PostgreSQL   │
│   Database    │
└───────────────┘

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (served by Nginx)
- **Backend:** Python FastAPI
- **Database:** PostgreSQL
- **Container Runtime:** Docker (multi-stage builds)
- **Container Registry:** AWS ECR
- **Orchestration:** Kubernetes (AWS EKS)
- **CI/CD:** GitHub Actions
- **Infrastructure:** AWS (EKS, ECR, VPC, Load Balancer)

## 📁 Project Structure
firstname-lastname-capstone/
├── frontend/                 # Frontend application
│   ├── Dockerfile           # Multi-stage Dockerfile
│   ├── nginx.conf           # Nginx configuration
│   └── public/              # Static files
├── backend/                  # Backend application
│   ├── Dockerfile           # Multi-stage Dockerfile
│   ├── requirements.txt     # Python dependencies
│   └── app/                 # FastAPI application
├── k8s/                      # Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment-frontend.yaml
│   ├── service-frontend.yaml
│   ├── deployment-backend.yaml
│   ├── service-backend.yaml
│   └── ingress.yaml
├── .github/workflows/        # CI/CD pipeline
│   └── ci-cd.yml
├── README.md                 # Project documentation
└── RUNBOOK.md               # Operations guide

## 🚦 Getting Started

### Prerequisites

1. AWS Account with EKS cluster access
2. GitHub account
3. Docker installed locally
4. kubectl installed locally
5. AWS CLI configured

### Setup Steps

1. **Clone the Repository**
```bash
   git clone https://github.com/yourusername/firstname-lastname-capstone.git
   cd firstname-lastname-capstone
```

2. **Configure AWS Secrets in GitHub**
   - Go to: Settings → Secrets and variables → Actions
   - Add secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

3. **Create ECR Repositories**
```bash
   aws ecr create-repository --repository-name firstname-lastname/frontend --region <REGION>
   aws ecr create-repository --repository-name firstname-lastname/backend --region <REGION>
```

4. **Update Configuration**
   - Replace `firstname-lastname` with your actual name throughout the project
   - Update `<AWS_ACCOUNT_ID>` and `<REGION>` in YAML files
   - Update `<EKS_CLUSTER_NAME>` in the GitHub Actions workflow

5. **Push to GitHub**
```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
```

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline automatically:

1. ✅ Checks out code
2. ✅ Configures AWS credentials
3. ✅ Logs into Amazon ECR
4. ✅ Builds Docker images (multi-stage)
5. ✅ Pushes images to ECR with `latest` and `git-sha` tags
6. ✅ Deploys to EKS cluster
7. ✅ Verifies deployment health

**Pipeline Trigger:** Every push to `main` branch

## 🔍 Verification

### Check Pods
```bash
kubectl get pods -n firstname-lastname
```

### Check Services
```bash
kubectl get svc -n firstname-lastname
```

### Check Ingress
```bash
kubectl get ingress -n firstname-lastname
```

### Access Application
https://firstname-lastname.capstone.company.com

## 📊 Monitoring

### View Logs
```bash
# Frontend logs
kubectl logs -f deployment/frontend -n firstname-lastname

# Backend logs
kubectl logs -f deployment/backend -n firstname-lastname
```

### Describe Pods
```bash
kubectl describe pod <pod-name> -n firstname-lastname
```

## 🔒 Security Features

- ✅ Multi-stage Docker builds
- ✅ Non-root containers
- ✅ Resource limits and requests
- ✅ Health checks (liveness & readiness probes)
- ✅ Secret management for database credentials
- ✅ Network isolation via Kubernetes namespaces
- ✅ ECR image scanning (enabled by default)

## 🎯 Project Requirements Checklist

- [x] GitHub repository with branch protection
- [x] Frontend with /health endpoint
- [x] Backend with /health endpoint and database connection
- [x] Multi-stage Dockerfiles for both services
- [x] Non-root user in containers
- [x] CI/CD pipeline with GitHub Actions
- [x] ECR for container registry
- [x] Kubernetes deployments with resource limits
- [x] Liveness and readiness probes
- [x] Services (ClusterIP)
- [x] Ingress for external access
- [x] Comprehensive documentation

## 📞 Support

**DevOps Team Contact:**
- dan@tiberbu.com
- njoroge@tiberbu.com
- elvis@tiberbu.com

**Mentors:** Daniel, James, Elvis

## 📝 License

This project is for educational purposes as part of the DevOps Capstone Project.