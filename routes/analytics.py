from flask import Blueprint, jsonify
from sqlalchemy import func, text, desc
from datetime import datetime, timedelta
from models.db import db
from models.record import Record, RecordMetadata

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/health-stats", methods=["GET"])
def get_health_stats():
    """Get overall health statistics"""
    try:
        # Get total records count
        total_records = db.session.query(func.count(Record.id)).scalar()
        
        # Get unique record types count
        unique_types = db.session.query(func.count(func.distinct(Record.type))).scalar()
        
        # Get date range
        date_range = db.session.query(
            func.min(Record.start_date),
            func.max(Record.start_date)
        ).first()
        
        # Get average heart rate (cast to numeric)
        avg_heart_rate = db.session.query(func.avg(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierHeartRate',
            Record.unit == 'count/min'
        ).scalar()
        
        # Get total steps (cast to numeric)
        total_steps = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierStepCount'
        ).scalar()
        
        # Get total calories (cast to numeric)
        total_calories = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierActiveEnergyBurned'
        ).scalar()
        
        # Get average sleep (in hours) - skip for now as sleep data is categorical
        avg_sleep = None
        
        return jsonify({
            "total_records": total_records or 0,
            "unique_types": unique_types or 0,
            "date_range": {
                "start": date_range[0].isoformat() if date_range and date_range[0] else None,
                "end": date_range[1].isoformat() if date_range and date_range[1] else None
            },
            "avg_heart_rate": round(avg_heart_rate, 1) if avg_heart_rate else 0,
            "total_steps": int(total_steps) if total_steps else 0,
            "total_calories": int(total_calories) if total_calories else 0,
            "avg_sleep_hours": round(avg_sleep, 1) if avg_sleep else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/data-types", methods=["GET"])
def get_data_types():
    """Get distribution of health data types"""
    try:
        # Get count of each record type
        type_counts = db.session.query(
            Record.type,
            func.count(Record.id).label('count')
        ).group_by(Record.type).order_by(desc('count')).limit(10).all()
        
        return jsonify({
            "data_types": [
                {"type": record_type, "count": count}
                for record_type, count in type_counts
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/timeline", methods=["GET"])
def get_timeline_data():
    """Get activity timeline data - using available data"""
    try:
        # Get the most recent 30 days of data (or all available data if less than 30 days)
        # First, get the date range of available data
        date_range = db.session.query(
            func.min(Record.start_date),
            func.max(Record.start_date)
        ).first()
        
        if not date_range or not date_range[0] or not date_range[1]:
            return jsonify({
                "daily_steps": [],
                "daily_heart_rate": []
            })
        
        # Get the most recent 30 days from the latest date in the data
        latest_date = date_range[1].date()
        thirty_days_ago = latest_date - timedelta(days=30)
        
        # Get daily step counts for the most recent 30 days of data
        daily_steps = db.session.query(
            func.date(Record.start_date).label('date'),
            func.sum(func.cast(Record.value, db.Numeric)).label('steps')
        ).filter(
            Record.type == 'HKQuantityTypeIdentifierStepCount',
            func.date(Record.start_date) >= thirty_days_ago,
            func.date(Record.start_date) <= latest_date
        ).group_by(func.date(Record.start_date)).order_by('date').all()
        
        # Get daily heart rate averages for the most recent 30 days of data
        daily_heart_rate = db.session.query(
            func.date(Record.start_date).label('date'),
            func.avg(func.cast(Record.value, db.Numeric)).label('heart_rate')
        ).filter(
            Record.type == 'HKQuantityTypeIdentifierHeartRate',
            Record.unit == 'count/min',
            func.date(Record.start_date) >= thirty_days_ago,
            func.date(Record.start_date) <= latest_date
        ).group_by(func.date(Record.start_date)).order_by('date').all()
        
        # If no recent data, get the most recent 30 days of any data
        if not daily_steps and not daily_heart_rate:
            # Get the most recent 30 days of step data
            daily_steps = db.session.query(
                func.date(Record.start_date).label('date'),
                func.sum(func.cast(Record.value, db.Numeric)).label('steps')
            ).filter(
                Record.type == 'HKQuantityTypeIdentifierStepCount'
            ).group_by(func.date(Record.start_date)).order_by(desc('date')).limit(30).all()
            
            # Get the most recent 30 days of heart rate data
            daily_heart_rate = db.session.query(
                func.date(Record.start_date).label('date'),
                func.avg(func.cast(Record.value, db.Numeric)).label('heart_rate')
            ).filter(
                Record.type == 'HKQuantityTypeIdentifierHeartRate',
                Record.unit == 'count/min'
            ).group_by(func.date(Record.start_date)).order_by(desc('date')).limit(30).all()
        
        return jsonify({
            "daily_steps": [
                {"date": date.isoformat(), "steps": int(steps) if steps else 0}
                for date, steps in daily_steps
            ],
            "daily_heart_rate": [
                {"date": date.isoformat(), "heart_rate": round(heart_rate, 1) if heart_rate else 0}
                for date, heart_rate in daily_heart_rate
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/heart-rate-trends", methods=["GET"])
def get_heart_rate_trends():
    """Get heart rate trends over time - using available data"""
    try:
        # Get heart rate data for the last 30 days (or available data)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        heart_rate_data = db.session.query(
            func.date(Record.start_date).label('date'),
            func.avg(func.cast(Record.value, db.Numeric)).label('avg_heart_rate'),
            func.min(func.cast(Record.value, db.Numeric)).label('min_heart_rate'),
            func.max(func.cast(Record.value, db.Numeric)).label('max_heart_rate')
        ).filter(
            Record.type == 'HKQuantityTypeIdentifierHeartRate',
            Record.unit == 'count/min',
            Record.start_date >= thirty_days_ago
        ).group_by(func.date(Record.start_date)).order_by('date').limit(30).all()
        
        # If no recent data, get the most recent 30 days of heart rate data
        if not heart_rate_data:
            heart_rate_data = db.session.query(
                func.date(Record.start_date).label('date'),
                func.avg(func.cast(Record.value, db.Numeric)).label('avg_heart_rate'),
                func.min(func.cast(Record.value, db.Numeric)).label('min_heart_rate'),
                func.max(func.cast(Record.value, db.Numeric)).label('max_heart_rate')
            ).filter(
                Record.type == 'HKQuantityTypeIdentifierHeartRate',
                Record.unit == 'count/min'
            ).group_by(func.date(Record.start_date)).order_by(desc('date')).limit(30).all()
        
        return jsonify({
            "heart_rate_trends": [
                {
                    "date": date.isoformat(),
                    "avg": round(avg_hr, 1) if avg_hr else 0,
                    "min": int(min_hr) if min_hr else 0,
                    "max": int(max_hr) if max_hr else 0
                }
                for date, avg_hr, min_hr, max_hr in heart_rate_data
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/recent-activity", methods=["GET"])
def get_recent_activity():
    """Get recent health activity - diverse recent records"""
    try:
        # Get recent records from different types to show variety
        activity_list = []
        
        # Get recent heart rate records
        heart_rate_records = db.session.query(Record).filter(
            Record.type == 'HKQuantityTypeIdentifierHeartRate',
            Record.unit == 'count/min'
        ).order_by(desc(Record.start_date)).limit(5).all()
        
        for record in heart_rate_records:
            activity_list.append({
                "type": "Heart Rate",
                "value": f"{int(float(record.value))} BPM",
                "time": record.start_date.strftime("%H:%M"),
                "date": record.start_date.strftime("%b %d"),
                "icon": "fas fa-heartbeat"
            })
        
        # Get recent step records (but only significant ones)
        step_records = db.session.query(Record).filter(
            Record.type == 'HKQuantityTypeIdentifierStepCount',
            func.cast(Record.value, db.Numeric) > 100  # Only show significant step counts
        ).order_by(desc(Record.start_date)).limit(5).all()
        
        for record in step_records:
            activity_list.append({
                "type": "Steps",
                "value": f"{int(float(record.value)):,} steps",
                "time": record.start_date.strftime("%H:%M"),
                "date": record.start_date.strftime("%b %d"),
                "icon": "fas fa-running"
            })
        
        # Get recent calorie records
        calorie_records = db.session.query(Record).filter(
            Record.type == 'HKQuantityTypeIdentifierActiveEnergyBurned'
        ).order_by(desc(Record.start_date)).limit(5).all()
        
        for record in calorie_records:
            activity_list.append({
                "type": "Calories",
                "value": f"{int(float(record.value))} cal",
                "time": record.start_date.strftime("%H:%M"),
                "date": record.start_date.strftime("%b %d"),
                "icon": "fas fa-fire"
            })
        
        # Get recent sleep records
        sleep_records = db.session.query(Record).filter(
            Record.type == 'HKCategoryTypeIdentifierSleepAnalysis'
        ).order_by(desc(Record.start_date)).limit(3).all()
        
        for record in sleep_records:
            activity_list.append({
                "type": "Sleep",
                "value": record.value.replace('HKCategoryValueSleepAnalysis', ''),
                "time": record.start_date.strftime("%H:%M"),
                "date": record.start_date.strftime("%b %d"),
                "icon": "fas fa-bed"
            })
        
        # Get other interesting record types
        other_records = db.session.query(Record).filter(
            Record.type.notin_([
                'HKQuantityTypeIdentifierHeartRate',
                'HKQuantityTypeIdentifierStepCount', 
                'HKQuantityTypeIdentifierActiveEnergyBurned',
                'HKCategoryTypeIdentifierSleepAnalysis'
            ])
        ).order_by(desc(Record.start_date)).limit(5).all()
        
        for record in other_records:
            # Format other record types
            type_name = record.type.replace('HKQuantityTypeIdentifier', '').replace('HKCategoryTypeIdentifier', '')
            type_name = ' '.join([word.capitalize() for word in type_name.split()])
            
            activity_list.append({
                "type": type_name,
                "value": f"{record.value} {record.unit or ''}",
                "time": record.start_date.strftime("%H:%M"),
                "date": record.start_date.strftime("%b %d"),
                "icon": "fas fa-chart-line"
            })
        
        # Sort by date and limit to 20 most recent
        activity_list.sort(key=lambda x: x['date'] + ' ' + x['time'], reverse=True)
        activity_list = activity_list[:20]
        
        return jsonify({
            "recent_activity": activity_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/daily-summary", methods=["GET"])
def get_daily_summary():
    """Get daily activity summary - using most recent data"""
    try:
        # Get the most recent date with data
        most_recent_date = db.session.query(func.max(func.date(Record.start_date))).scalar()
        
        if not most_recent_date:
            return jsonify({
                "daily_summary": {
                    "date": datetime.now().date().isoformat(),
                    "steps": 0,
                    "calories": 0,
                    "avg_heart_rate": 0,
                    "distance_km": 0
                }
            })
        
        # Get steps for the most recent date
        recent_steps = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierStepCount',
            func.date(Record.start_date) == most_recent_date
        ).scalar()
        
        # Get calories for the most recent date
        recent_calories = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierActiveEnergyBurned',
            func.date(Record.start_date) == most_recent_date
        ).scalar()
        
        # Get average heart rate for the most recent date
        recent_heart_rate = db.session.query(func.avg(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierHeartRate',
            Record.unit == 'count/min',
            func.date(Record.start_date) == most_recent_date
        ).scalar()
        
        # Get distance for the most recent date
        recent_distance = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierDistanceWalkingRunning',
            func.date(Record.start_date) == most_recent_date
        ).scalar()
        
        return jsonify({
            "daily_summary": {
                "date": most_recent_date.isoformat(),
                "steps": int(recent_steps) if recent_steps else 0,
                "calories": int(recent_calories) if recent_calories else 0,
                "avg_heart_rate": round(recent_heart_rate, 1) if recent_heart_rate else 0,
                "distance_km": round(recent_distance, 2) if recent_distance else 0
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route("/analytics/health-insights", methods=["GET"])
def get_health_insights():
    """Get health insights and workout recommendations"""
    try:
        # Get recent activity data (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # Get average daily steps for the last 7 days
        recent_steps = db.session.query(func.avg(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierStepCount',
            Record.start_date >= seven_days_ago
        ).scalar()
        
        # Get average daily calories for the last 7 days
        recent_calories = db.session.query(func.avg(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierActiveEnergyBurned',
            Record.start_date >= seven_days_ago
        ).scalar()
        
        # Get average heart rate for the last 7 days
        recent_heart_rate = db.session.query(func.avg(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierHeartRate',
            Record.unit == 'count/min',
            Record.start_date >= seven_days_ago
        ).scalar()
        
        # Get yesterday's activity
        yesterday = datetime.now().date() - timedelta(days=1)
        yesterday_steps = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierStepCount',
            func.date(Record.start_date) == yesterday
        ).scalar()
        
        yesterday_calories = db.session.query(func.sum(func.cast(Record.value, db.Numeric))).filter(
            Record.type == 'HKQuantityTypeIdentifierActiveEnergyBurned',
            func.date(Record.start_date) == yesterday
        ).scalar()
        
        # Calculate workout recommendation
        recommendation = calculate_workout_recommendation(
            recent_steps or 0,
            recent_calories or 0,
            recent_heart_rate or 0,
            yesterday_steps or 0,
            yesterday_calories or 0
        )
        
        # Calculate recovery score
        recovery_score = calculate_recovery_score(
            recent_steps or 0,
            recent_calories or 0,
            recent_heart_rate or 0
        )
        
        return jsonify({
            "insights": {
                "recent_activity": {
                    "avg_daily_steps": int(recent_steps) if recent_steps else 0,
                    "avg_daily_calories": int(recent_calories) if recent_calories else 0,
                    "avg_heart_rate": round(recent_heart_rate, 1) if recent_heart_rate else 0
                },
                "yesterday_activity": {
                    "steps": int(yesterday_steps) if yesterday_steps else 0,
                    "calories": int(yesterday_calories) if yesterday_calories else 0
                },
                "recovery_score": recovery_score,
                "workout_recommendation": recommendation
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def calculate_workout_recommendation(avg_steps, avg_calories, avg_hr, yesterday_steps, yesterday_calories):
    """Calculate workout recommendation based on recent activity"""
    
    # Define thresholds
    high_activity_steps = 10000
    high_activity_calories = 500
    moderate_activity_steps = 7000
    moderate_activity_calories = 300
    
    # Check if yesterday was a high activity day
    yesterday_high_activity = yesterday_steps > high_activity_steps or yesterday_calories > high_activity_calories
    
    # Check recent activity levels
    recent_high_activity = avg_steps > high_activity_steps or avg_calories > high_activity_calories
    recent_moderate_activity = avg_steps > moderate_activity_steps or avg_calories > moderate_activity_calories
    
    # Heart rate considerations
    elevated_hr = avg_hr > 80  # Assuming resting HR around 60-70
    
    if yesterday_high_activity and recent_high_activity:
        return {
            "recommendation": "rest",
            "confidence": "high",
            "reason": "You've had high activity levels recently. Your body needs recovery time to prevent overtraining and injury.",
            "suggestions": [
                "Take a complete rest day",
                "Focus on light stretching or yoga",
                "Ensure adequate sleep (7-9 hours)",
                "Stay hydrated and eat nutritious meals"
            ]
        }
    elif yesterday_high_activity and not recent_high_activity:
        return {
            "recommendation": "light_activity",
            "confidence": "medium",
            "reason": "Yesterday was intense but your recent activity has been moderate. Light activity can help with recovery.",
            "suggestions": [
                "Go for a gentle walk (30-45 minutes)",
                "Try light yoga or stretching",
                "Swimming or cycling at low intensity",
                "Listen to your body and stop if you feel tired"
            ]
        }
    elif recent_moderate_activity and not elevated_hr:
        return {
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
    elif not recent_moderate_activity:
        return {
            "recommendation": "workout",
            "confidence": "high",
            "reason": "Your recent activity levels are low. A workout would be beneficial for your health and fitness goals.",
            "suggestions": [
                "Start with a moderate-intensity workout",
                "Aim for 30-45 minutes of exercise",
                "Include both cardio and strength training",
                "Gradually increase intensity over time"
            ]
        }
    else:
        return {
            "recommendation": "light_activity",
            "confidence": "medium",
            "reason": "Your activity levels suggest a light activity day would be most beneficial.",
            "suggestions": [
                "Go for a walk or light jog",
                "Try a beginner-friendly workout",
                "Focus on movement and staying active",
                "Build up gradually to more intense workouts"
            ]
        }

def calculate_recovery_score(avg_steps, avg_calories, avg_hr):
    """Calculate a recovery score from 0-100"""
    
    # Normalize metrics (these are rough estimates)
    steps_score = min(100, (avg_steps / 10000) * 100)  # 10k steps = 100%
    calories_score = min(100, (avg_calories / 500) * 100)  # 500 cal = 100%
    
    # Heart rate score (lower is better for recovery)
    if avg_hr < 70:
        hr_score = 100
    elif avg_hr < 80:
        hr_score = 80
    elif avg_hr < 90:
        hr_score = 60
    else:
        hr_score = 40
    
    # Weighted average
    recovery_score = (steps_score * 0.4 + calories_score * 0.4 + hr_score * 0.2)
    
    return {
        "score": round(recovery_score, 1),
        "level": "excellent" if recovery_score >= 80 else "good" if recovery_score >= 60 else "fair" if recovery_score >= 40 else "poor",
        "breakdown": {
            "activity_score": round(steps_score, 1),
            "calorie_score": round(calories_score, 1),
            "heart_rate_score": round(hr_score, 1)
        }
    }
