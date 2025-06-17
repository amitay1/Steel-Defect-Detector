"""
Memory Bank for YOLOv8 Metal Defect Detection System
This module provides persistent storage and retrieval of detection results,
model performance metrics, and user feedback.
"""

import json
import sqlite3
import datetime
import os
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import cv2
import base64
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class DefectDetection:
    """Data class for storing defect detection results"""
    timestamp: str
    image_hash: str
    defect_type: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]
    image_size: Tuple[int, int]  # (width, height)
    model_version: str
    user_feedback: Optional[str] = None
    is_verified: bool = False

@dataclass
class ModelPerformance:
    """Data class for storing model performance metrics"""
    timestamp: str
    total_detections: int
    avg_confidence: float
    defect_types_count: Dict[str, int]
    processing_time: float
    model_version: str

class MemoryBank:
    """Memory bank for storing and retrieving detection data"""
    
    def __init__(self, db_path: str = "memory_bank.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Defect detections table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS defect_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    image_hash TEXT NOT NULL,
                    defect_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    bbox_x1 REAL NOT NULL,
                    bbox_y1 REAL NOT NULL,
                    bbox_x2 REAL NOT NULL,
                    bbox_y2 REAL NOT NULL,
                    image_width INTEGER NOT NULL,
                    image_height INTEGER NOT NULL,
                    model_version TEXT NOT NULL,
                    user_feedback TEXT,
                    is_verified BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Model performance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    total_detections INTEGER NOT NULL,
                    avg_confidence REAL NOT NULL,
                    defect_types_count TEXT NOT NULL,
                    processing_time REAL NOT NULL,
                    model_version TEXT NOT NULL
                )
            """)
            
            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    images_processed INTEGER DEFAULT 0,
                    defects_found INTEGER DEFAULT 0
                )
            """)
            
            # Knowledge base table for defect patterns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    defect_type TEXT NOT NULL,
                    pattern_description TEXT,
                    typical_confidence_range TEXT,
                    common_locations TEXT,
                    severity_indicators TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    def store_detection(self, detection: DefectDetection) -> int:
        """Store a defect detection in the memory bank"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO defect_detections 
                (timestamp, image_hash, defect_type, confidence, 
                 bbox_x1, bbox_y1, bbox_x2, bbox_y2, 
                 image_width, image_height, model_version, 
                 user_feedback, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                detection.timestamp, detection.image_hash, detection.defect_type,
                detection.confidence, detection.bbox[0], detection.bbox[1],
                detection.bbox[2], detection.bbox[3], detection.image_size[0],
                detection.image_size[1], detection.model_version,
                detection.user_feedback, detection.is_verified
            ))
            conn.commit()
            return cursor.lastrowid
    
    def store_performance_metrics(self, performance: ModelPerformance) -> int:
        """Store model performance metrics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO model_performance 
                (timestamp, total_detections, avg_confidence, 
                 defect_types_count, processing_time, model_version)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                performance.timestamp, performance.total_detections,
                performance.avg_confidence, json.dumps(performance.defect_types_count),
                performance.processing_time, performance.model_version
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_detection_history(self, 
                            defect_type: Optional[str] = None,
                            min_confidence: float = 0.0,
                            limit: int = 100) -> List[DefectDetection]:
        """Retrieve detection history with optional filtering"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT timestamp, image_hash, defect_type, confidence,
                       bbox_x1, bbox_y1, bbox_x2, bbox_y2,
                       image_width, image_height, model_version,
                       user_feedback, is_verified
                FROM defect_detections
                WHERE confidence >= ?
            """
            params = [min_confidence]
            
            if defect_type:
                query += " AND defect_type = ?"
                params.append(defect_type)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            detections = []
            for row in rows:
                detection = DefectDetection(
                    timestamp=row[0],
                    image_hash=row[1],
                    defect_type=row[2],
                    confidence=row[3],
                    bbox=[row[4], row[5], row[6], row[7]],
                    image_size=(row[8], row[9]),
                    model_version=row[10],
                    user_feedback=row[11],
                    is_verified=bool(row[12])
                )
                detections.append(detection)
            
            return detections
    
    def get_defect_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about detected defects"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total detections
            cursor.execute("SELECT COUNT(*) FROM defect_detections")
            total_detections = cursor.fetchone()[0]
            
            # Defect type distribution
            cursor.execute("""
                SELECT defect_type, COUNT(*), AVG(confidence)
                FROM defect_detections
                GROUP BY defect_type
                ORDER BY COUNT(*) DESC
            """)
            defect_distribution = {
                row[0]: {"count": row[1], "avg_confidence": row[2]}
                for row in cursor.fetchall()
            }
            
            # Confidence distribution
            cursor.execute("""
                SELECT 
                    AVG(confidence) as avg_conf,
                    MIN(confidence) as min_conf,
                    MAX(confidence) as max_conf
                FROM defect_detections
            """)
            conf_stats = cursor.fetchone()
            
            # Recent performance trend (last 7 days)
            week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
            cursor.execute("""
                SELECT DATE(timestamp) as date, COUNT(*), AVG(confidence)
                FROM defect_detections
                WHERE timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date
            """, (week_ago,))
            daily_stats = {
                row[0]: {"count": row[1], "avg_confidence": row[2]}
                for row in cursor.fetchall()
            }
            
            return {
                "total_detections": total_detections,
                "defect_distribution": defect_distribution,
                "confidence_stats": {
                    "average": conf_stats[0] if conf_stats[0] else 0,
                    "minimum": conf_stats[1] if conf_stats[1] else 0,
                    "maximum": conf_stats[2] if conf_stats[2] else 0
                },
                "daily_stats_last_week": daily_stats
            }
    
    def update_user_feedback(self, detection_id: int, feedback: str, is_verified: bool = False):
        """Update user feedback for a specific detection"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE defect_detections 
                SET user_feedback = ?, is_verified = ?
                WHERE id = ?
            """, (feedback, is_verified, detection_id))
            conn.commit()
    
    def get_similar_detections(self, 
                             defect_type: str, 
                             confidence_threshold: float = 0.1) -> List[DefectDetection]:
        """Find similar detections based on defect type and confidence range"""
        return self.get_detection_history(
            defect_type=defect_type,
            min_confidence=max(0.0, confidence_threshold)
        )
    
    def export_data(self, output_path: str, format: str = "json"):
        """Export memory bank data to file"""
        data = {
            "detections": [asdict(d) for d in self.get_detection_history(limit=10000)],
            "statistics": self.get_defect_statistics(),
            "export_timestamp": datetime.datetime.now().isoformat()
        }
        
        if format.lower() == "json":
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def clear_old_data(self, days_to_keep: int = 30):
        """Remove old detection data to manage storage"""
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days_to_keep)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM defect_detections 
                WHERE timestamp < ? AND is_verified = FALSE
            """, (cutoff_date,))
            
            cursor.execute("""
                DELETE FROM model_performance 
                WHERE timestamp < ?
            """, (cutoff_date,))
            
            conn.commit()

def generate_image_hash(image: np.ndarray) -> str:
    """Generate a hash for an image for duplicate detection"""
    # Convert to grayscale and resize for consistent hashing
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
    resized = cv2.resize(gray, (64, 64))
    
    # Create a simple hash based on image content
    hash_value = hash(resized.tobytes())
    return str(abs(hash_value))

def format_detection_summary(detections: List[DefectDetection]) -> str:
    """Format detection results for display"""
    if not detections:
        return "No defects detected."
    
    summary = f"Found {len(detections)} defect(s):\n"
    for i, detection in enumerate(detections, 1):
        summary += f"{i}. {detection.defect_type} (confidence: {detection.confidence:.2f})\n"
    
    return summary
