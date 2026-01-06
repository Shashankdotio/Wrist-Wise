# Wrist-Wise Setup Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (optional, for cloning)

### 1. Start the Application

```bash
# Navigate to the project directory
cd Wrist-Wise

# Start all services (database + backend + frontend)
docker-compose up --build -d
```

### 2. Access the Application

- **Frontend**: http://localhost:8000
- **API Health Check**: http://localhost:8000/
- **API Count Endpoint**: http://localhost:8000/count

### 3. Upload Apple Health Data

1. Open http://localhost:8000 in your browser
2. Drag and drop your Apple Health export XML file
3. Or click "browse files" to select a file
4. Wait for the upload to complete

## 📁 Project Structure

```
Wrist-Wise/
├── frontend/                 # Frontend files
│   ├── index.html           # Main HTML page
│   ├── styles.css           # CSS styling
│   └── script.js            # JavaScript functionality
├── backend_server.py        # Flask backend server
├── models/                  # Database models
│   ├── db.py               # Database configuration
│   └── record.py           # Record model
├── routes/                  # API routes
│   ├── health.py           # Health check endpoint
│   ├── upload.py           # File upload endpoint
│   ├── count.py            # Data count endpoint
│   └── router.py           # Route registration
├── env/                     # Environment configuration
│   └── service.env         # Database credentials
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Backend container configuration
└── pyproject.toml          # Python dependencies
```

## 🔧 Development Setup

### Local Development (without Docker)

1. **Install Python Dependencies**
   ```bash
   # Install Poetry (if not already installed)
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install dependencies
   poetry install
   ```

2. **Start PostgreSQL Database**
   ```bash
   # Using Docker for database only
   docker run -d \
     --name wrist-wise-db \
     -e POSTGRES_USER=appleuser \
     -e POSTGRES_PASSWORD=applepass \
     -e POSTGRES_DB=appledb \
     -p 5432:5432 \
     postgres:15
   ```

3. **Run the Backend**
   ```bash
   # Activate virtual environment
   poetry shell
   
   # Start the Flask server
   python backend_server.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:8000
   - API: http://localhost:8000/

## 🐳 Docker Commands

### Basic Commands
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build -d

# View running containers
docker ps
```

### Database Commands
```bash
# Connect to database
docker-compose exec db psql -U appleuser -d appledb

# View database logs
docker-compose logs db

# Reset database (removes all data)
docker-compose down -v
docker-compose up -d
```

### Backend Commands
```bash
# View backend logs
docker-compose logs backend

# Execute commands in backend container
docker-compose exec backend bash

# Restart backend only
docker-compose restart backend
```

## 📊 API Endpoints

### Health Check
```bash
GET /
# Response: {"status": "ok", "message": "Apple Health backend server is running."}
```

### Data Count
```bash
GET /count
# Response: {"records": 113000, "metadata_entries": 88219}
```

### File Upload
```bash
POST /upload
Content-Type: multipart/form-data
Body: file (XML file)
# Response: {"message": "Successfully ingested 113000 records."}
```

## 🔍 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Database connection failed**
   ```bash
   # Check if database container is running
   docker-compose ps
   
   # Restart database
   docker-compose restart db
   ```

3. **Upload fails with memory error**
   - The system is configured with 2GB memory limit
   - Large files (>200MB) may take time to process
   - Check Docker logs: `docker-compose logs backend`

4. **Frontend not loading**
   ```bash
   # Check if backend is serving static files
   curl http://localhost:8000/
   
   # Rebuild containers
   docker-compose up --build -d
   ```

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f backend
```

## 🎯 Features

### Frontend Features
- ✅ Modern, responsive design
- ✅ Real-time API status monitoring
- ✅ Drag & drop file upload
- ✅ Upload progress tracking
- ✅ Data visualization placeholders
- ✅ Activity feed

### Backend Features
- ✅ RESTful API endpoints
- ✅ PostgreSQL database integration
- ✅ Large file upload support (600MB limit)
- ✅ Streaming XML parsing for memory efficiency
- ✅ Batch processing for database operations
- ✅ Error handling and logging

### Data Processing
- ✅ Apple Health XML export parsing
- ✅ Health record extraction
- ✅ Metadata processing
- ✅ Database storage with relationships
- ✅ Memory-efficient processing

## 🔒 Security Notes

- Database credentials are stored in environment variables
- File upload size is limited to 600MB
- Only XML files are accepted for upload
- CORS is not configured (frontend and backend on same domain)

## 📈 Performance

- **Memory Usage**: 2GB limit for backend container
- **File Processing**: Streaming XML parser for large files
- **Database**: Batch commits every 1000 records
- **Frontend**: Optimized CSS and JavaScript

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use secure environment variable management
2. **Database**: Use managed PostgreSQL service
3. **File Storage**: Use cloud storage for uploaded files
4. **Load Balancing**: Add load balancer for multiple backend instances
5. **SSL/TLS**: Configure HTTPS
6. **Monitoring**: Add application monitoring and logging

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Test API endpoints manually
4. Check system resources (memory, disk space)

---

**Happy Health Data Analysis! 🏃‍♂️💓**

