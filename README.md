# 🏥 Wrist-Wise - Apple Health Analytics Dashboard

<div align="center">

![Wrist-Wise Logo](https://img.shields.io/badge/Wrist--Wise-Health%20Analytics-667eea?style=for-the-badge)

**A comprehensive web application for analyzing and visualizing Apple Health data with intelligent workout recommendations**

[Features](#-features) • [Screenshots](#-ui-design--screenshots) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [UI Design & Screenshots](#-ui-design--screenshots)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup-instructions)
- [API Documentation](#-api-documentation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Wrist-Wise** is a powerful health analytics platform that transforms your Apple Health export data into actionable insights. The application provides:

- 📊 **Comprehensive Data Visualization** - Interactive charts and graphs for all your health metrics
- 🧠 **AI-Powered Insights** - Intelligent recovery score calculation and workout recommendations
- 📈 **Activity Tracking** - Daily, weekly, and monthly activity summaries
- 💡 **Personalized Recommendations** - Smart suggestions on whether to workout or rest based on your activity patterns
- 🎨 **Beautiful Modern UI** - Clean, responsive design with gradient backgrounds and smooth animations

### What Makes Wrist-Wise Special?

Unlike basic health trackers, Wrist-Wise analyzes your complete health history to provide:
- **Recovery Score**: A 0-100 score based on your activity levels, calories burned, and heart rate patterns
- **Workout Recommendations**: Data-driven advice on whether to push hard, take it easy, or rest completely
- **Trend Analysis**: Long-term patterns in your health data to identify improvements or concerns
- **Comprehensive Dashboard**: All your health metrics in one beautiful, easy-to-understand interface

---

## ✨ Features

### 📊 Data Visualization
- **Health Data Types Distribution** - Doughnut chart showing distribution of different health metrics
- **Activity Timeline** - 30-day line chart tracking steps and heart rate trends
- **Heart Rate Trends** - Detailed heart rate analysis with min, max, and average values
- **Daily Activity Summary** - Bar chart showing today's key metrics (steps, calories, heart rate, distance)

### 🧠 Health Insights
- **Recovery Score** - Calculated based on:
  - Recent activity levels (steps)
  - Calories burned
  - Heart rate patterns
- **Workout Recommendations** - Four types of recommendations:
  - 🛌 **Rest** - When your body needs recovery
  - 🚶 **Light Activity** - Gentle movement for active recovery
  - 💪 **Moderate Workout** - Balanced exercise session
  - 🔥 **Full Workout** - Time to push your limits

### 📱 User Interface
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Modern Gradient UI** - Beautiful purple gradient theme
- **Real-time Updates** - Live data refresh every 30 seconds
- **Drag & Drop Upload** - Easy file upload interface
- **Progress Indicators** - Visual feedback for all operations

### 🔒 Data Management
- **Secure File Upload** - Handles large XML files (up to 600MB)
- **Batch Processing** - Efficient memory management for large datasets
- **PostgreSQL Database** - Robust data storage and retrieval
- **Streaming XML Parser** - Handles large files without memory issues

---

## 🎨 UI Design & Screenshots

### Design Philosophy

Wrist-Wise features a **modern, clean design** with:

- **Color Scheme**: Purple gradient background (#667eea to #764ba2) with white cards
- **Typography**: Clean, readable Segoe UI font family
- **Layout**: Card-based grid system for easy information scanning
- **Icons**: Font Awesome icons for visual clarity
- **Animations**: Smooth transitions and hover effects

### Key UI Components

#### 1. **Status Dashboard**
- API Status indicator (Online/Offline)
- Total Records count
- Metadata Entries count
- Real-time status updates

#### 2. **Upload Section**
- Large drag-and-drop area
- File type validation (.xml only)
- File size validation (600MB limit)
- Progress bar with percentage
- Success/Error notifications

#### 3. **Health Statistics Cards**
- Average Heart Rate (BPM)
- Total Steps
- Total Calories Burned
- Average Sleep Hours

#### 4. **Visualization Charts**
- **Data Types Distribution**: Doughnut chart with color-coded segments
- **Activity Timeline**: Dual-axis line chart (Steps + Heart Rate)
- **Heart Rate Trends**: Multi-line chart (Avg, Min, Max)
- **Daily Activity Summary**: Colorful bar chart

#### 5. **Health Insights Section**
- **Recovery Score Circle**: Large circular display with score and level
- **Workout Recommendation Card**: 
  - Color-coded recommendation type
  - Detailed reasoning
  - Actionable suggestions list

#### 6. **Recent Activity Feed**
- Chronological list of recent health events
- Icons for different activity types
- Formatted values and timestamps

### Visual Features

- **Gradient Backgrounds**: Purple gradient throughout
- **Glass Morphism**: Semi-transparent cards with backdrop blur
- **Color Coding**: 
  - Green: Good/Excellent metrics
  - Yellow: Moderate/Fair metrics
  - Red: Rest/Poor metrics
- **Responsive Grid**: Adapts to screen size
- **Smooth Animations**: Hover effects and transitions

---

## 🛠 Technology Stack

### Backend
- **Python 3.12+** - Core programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **lxml** - XML parsing for Apple Health exports
- **psycopg2** - PostgreSQL adapter

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern features (gradients, animations)
- **JavaScript (ES6+)** - Interactivity
- **Chart.js** - Data visualization library
- **Font Awesome** - Icon library

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Poetry** - Python dependency management

### Development Tools
- **VS Code** - Recommended IDE
- **Git** - Version control

---

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** installed and running
- **Git** for cloning the repository
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### 1. Clone the Repository

```bash
git clone https://github.com/Shashankdotio/Wrist-Wise.git
cd Wrist-Wise
```

### 2. Start with Docker Compose

```bash
docker-compose up -d
```

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

### 4. Upload Your Apple Health Data

1. Export your Apple Health data from the Health app (Settings → Health → Export Health Data)
2. Drag and drop the `export.xml` file onto the upload area
3. Wait for processing to complete
4. Explore your health insights!

---

## 📖 Detailed Setup Instructions

### Option 1: Docker Compose (Recommended)

This is the easiest way to get started. Docker Compose will set up both the database and backend server automatically.

#### Step 1: Install Docker Desktop

- **macOS**: Download from [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- **Windows**: Download from [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- **Linux**: Follow [Docker installation guide](https://docs.docker.com/engine/install/)

#### Step 2: Start the Services

```bash
# Navigate to project directory
cd Wrist-Wise

# Start all services (database + backend)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Step 3: Verify Installation

```bash
# Check if containers are running
docker ps

# Test the API
curl http://localhost:8000/health
```

You should see:
```json
{"message":"Apple Health backend server is running.","status":"ok"}
```

### Option 2: Local Development Setup

For development and customization, you can run the application locally.

#### Step 1: Install Python Dependencies

**Using Poetry (Recommended):**

```bash
# Install Poetry
pipx install poetry==1.8.5

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

**Using pip:**

```bash
pip install -r requirements.txt
```

#### Step 2: Set Up PostgreSQL Database

**Option A: Using Docker (Easiest)**

```bash
# Start only the database container
docker-compose up -d db

# The database will be available at localhost:5432
```

**Option B: Manual PostgreSQL Setup**

1. Install PostgreSQL on your system
2. Create database and user:

```sql
CREATE USER appleuser WITH PASSWORD 'applepass';
CREATE DATABASE appledb OWNER appleuser;
GRANT ALL PRIVILEGES ON DATABASE appledb TO appleuser;
```

#### Step 3: Configure Environment Variables

Create `env/.env` file:

```env
DATABASE_USER=appleuser
DATABASE_PASS=applepass
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=appledb
```

#### Step 4: Run the Server

```bash
# Make sure you're in the project directory
cd Wrist-Wise

# Run the server
python backend_server.py
```

The server will start on `http://localhost:8000`

#### Step 5: Run with VS Code (Optional)

1. Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask (backend_server.py)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend_server.py",
      "envFile": "${workspaceFolder}/env/.env",
      "env": {
        "FLASK_ENV": "development"
      },
      "console": "integratedTerminal"
    }
  ]
}
```

2. Press `F5` to start debugging

---

## 📚 API Documentation

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "message": "Apple Health backend server is running.",
  "status": "ok"
}
```

### Upload Health Data

```http
POST /upload
Content-Type: multipart/form-data
```

**Request:**
- `file`: Apple Health export XML file (max 600MB)

**Response:**
```json
{
  "message": "Successfully ingested 6543768 records."
}
```

### Get Record Counts

```http
GET /count
```

**Response:**
```json
{
  "records": 6543768,
  "metadata_entries": 12345
}
```

### Get Health Statistics

```http
GET /analytics/health-stats
```

**Response:**
```json
{
  "total_records": 6543768,
  "unique_types": 36,
  "avg_heart_rate": 121.1,
  "total_steps": 78806175,
  "total_calories": 2086294,
  "avg_sleep_hours": 0
}
```

### Get Data Types Distribution

```http
GET /analytics/data-types
```

**Response:**
```json
{
  "data_types": [
    {"type": "HKQuantityTypeIdentifierStepCount", "count": 1234567},
    {"type": "HKQuantityTypeIdentifierHeartRate", "count": 987654}
  ]
}
```

### Get Activity Timeline

```http
GET /analytics/timeline
```

**Response:**
```json
{
  "daily_steps": [
    {"date": "2025-07-20", "steps": 12345}
  ],
  "daily_heart_rate": [
    {"date": "2025-07-20", "heart_rate": 72.5}
  ]
}
```

### Get Heart Rate Trends

```http
GET /analytics/heart-rate-trends
```

**Response:**
```json
{
  "heart_rate_trends": [
    {
      "date": "2025-07-20",
      "avg": 72.5,
      "min": 60,
      "max": 95
    }
  ]
}
```

### Get Daily Summary

```http
GET /analytics/daily-summary
```

**Response:**
```json
{
  "daily_summary": {
    "date": "2025-07-20",
    "steps": 12345,
    "calories": 450,
    "avg_heart_rate": 72.5,
    "distance_km": 8.5
  }
}
```

### Get Health Insights

```http
GET /analytics/health-insights
```

**Response:**
```json
{
  "insights": {
    "recent_activity": {
      "avg_daily_steps": 8500,
      "avg_daily_calories": 420,
      "avg_heart_rate": 72.5
    },
    "yesterday_activity": {
      "steps": 12000,
      "calories": 550
    },
    "recovery_score": {
      "score": 75.5,
      "level": "good",
      "breakdown": {
        "activity_score": 85.0,
        "calorie_score": 84.0,
        "heart_rate_score": 80.0
      }
    },
    "workout_recommendation": {
      "recommendation": "moderate_workout",
      "confidence": "high",
      "reason": "Your recent activity levels are moderate and your heart rate suggests good recovery. You're ready for a workout.",
      "suggestions": [
        "Strength training or cardio workout",
        "Aim for 45-60 minutes of exercise",
        "Include both cardio and strength components",
        "Monitor your heart rate during exercise"
      ]
    }
  }
}
```

### Get Recent Activity

```http
GET /analytics/recent-activity
```

**Response:**
```json
{
  "recent_activity": [
    {
      "type": "Heart Rate",
      "value": "72 BPM",
      "time": "14:30",
      "date": "Jul 20",
      "icon": "fas fa-heartbeat"
    }
  ]
}
```

---

## 📖 Usage Guide

### 1. Exporting Apple Health Data

**On iPhone/iPad:**

1. Open the **Health** app
2. Tap your profile picture (top right)
3. Scroll down and tap **Export Health Data**
4. Choose how to share (AirDrop, Files, etc.)
5. Save the `export.xml` file

**On Mac:**

1. Open the **Health** app
2. Click **File** → **Export** → **Export All Health Data**
3. Save the `export.xml` file

### 2. Uploading to Wrist-Wise

1. Open Wrist-Wise in your browser (`http://localhost:8000`)
2. Locate the **Upload Section**
3. Either:
   - **Drag and drop** your `export.xml` file onto the upload area
   - **Click** the upload area and browse for your file
4. Wait for the upload progress to complete
5. You'll see a success message with the number of records processed

### 3. Exploring Your Data

After upload, the dashboard will automatically update with:

- **Health Statistics**: Overview of your key metrics
- **Charts**: Visual representations of your data
- **Insights**: Recovery score and workout recommendations
- **Recent Activity**: Latest health events

### 4. Understanding Recommendations

**Recovery Score Levels:**
- **Excellent (80-100)**: You're well-recovered and ready for intense workouts
- **Good (60-79)**: Good recovery, moderate workouts recommended
- **Fair (40-59)**: Some fatigue, light activity recommended
- **Poor (0-39)**: Need rest, avoid intense exercise

**Workout Recommendations:**
- **Rest**: Complete rest day, focus on recovery
- **Light Activity**: Gentle movement (walking, yoga, stretching)
- **Moderate Workout**: Balanced exercise (30-60 minutes)
- **Full Workout**: Intense training session

---

## 📁 Project Structure

```
Wrist-Wise/
├── backend_server.py          # Main Flask application entry point
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies (pip)
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Poetry lock file
├── start.sh                    # Startup script
│
├── frontend/                   # Frontend files
│   ├── index.html              # Main HTML file
│   ├── styles.css              # CSS styling
│   ├── script.js               # Main JavaScript
│   └── analytics.js            # Chart and analytics logic
│
├── routes/                     # API routes
│   ├── router.py               # Route registration
│   ├── health.py               # Health check endpoint
│   ├── upload.py               # File upload endpoint
│   ├── count.py                # Record count endpoint
│   └── analytics.py             # Analytics endpoints
│
├── models/                     # Database models
│   ├── db.py                   # Database initialization
│   └── record.py               # Record and RecordMetadata models
│
├── env/                        # Environment configuration
│   └── service.env             # Environment variables (not in git)
│
└── temp/                       # Temporary file storage (not in git)
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Docker Containers Won't Start

**Problem**: `docker-compose up` fails

**Solutions:**
- Ensure Docker Desktop is running
- Check if ports 8000 and 5432 are available:
  ```bash
  lsof -i :8000
  lsof -i :5432
  ```
- Restart Docker Desktop
- Try rebuilding: `docker-compose up --build`

#### 2. Database Connection Error

**Problem**: `Database connection failed`

**Solutions:**
- Verify database container is running: `docker ps`
- Check environment variables in `env/service.env`
- Ensure database credentials match in all config files
- Restart database: `docker-compose restart db`

#### 3. Upload Fails or Times Out

**Problem**: File upload doesn't complete

**Solutions:**
- Check file size (max 600MB)
- Verify file is valid XML format
- Check server logs: `docker-compose logs backend`
- Ensure sufficient disk space
- Try uploading a smaller test file first

#### 4. Charts Not Displaying

**Problem**: Charts show empty or no data

**Solutions:**
- Verify data was uploaded successfully
- Check browser console for JavaScript errors
- Ensure Chart.js library loaded correctly
- Refresh the page after upload completes
- Check API endpoints return data: `curl http://localhost:8000/analytics/timeline`

#### 5. Module Not Found Errors

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solutions:**
- Install dependencies: `poetry install` or `pip install -r requirements.txt`
- Activate virtual environment: `poetry shell`
- Check Python path in VS Code launch.json
- Rebuild Docker image: `docker-compose up --build`

#### 6. Port Already in Use

**Problem**: `Address already in use`

**Solutions:**
- Find process using port: `lsof -i :8000`
- Kill the process: `kill -9 <PID>`
- Or change port in `docker-compose.yml`

### Getting Help

If you encounter issues not covered here:

1. Review Docker logs: `docker-compose logs`
2. Check browser console for frontend errors
3. Verify all prerequisites are installed

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add comments for complex logic
- Test your changes before submitting
- Update documentation as needed

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🧪 Test coverage

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Authors

**Shashank Kamble**
- GitHub: [@Shashankdotio](https://github.com/Shashankdotio)

**Dheeraj Bangera**
- GitHub: [@Dheeraj-Bangera](https://github.com/Dheeraj-Bangera)

---

## 🙏 Acknowledgments

- **Apple Health** for providing comprehensive health data export
- **Chart.js** for beautiful data visualizations
- **Flask** community for excellent documentation
- **Docker** for simplifying deployment

---

<div align="center">

**Made with ❤️ for better health insights**

⭐ Star this repo if you find it helpful!

</div>
