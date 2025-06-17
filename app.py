import os
import cv2
import gradio as gr
import datetime
import time
from ultralytics import YOLO
from memory_bank import MemoryBank, DefectDetection, ModelPerformance, generate_image_hash, format_detection_summary

# Load model
MODEL_PATH = "yolov8_model.pt"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file {MODEL_PATH} not found. Please upload it to your Space.")
model = YOLO(MODEL_PATH)

# Initialize memory bank
memory_bank = MemoryBank()

# Model version (you can update this when you retrain the model)
MODEL_VERSION = "v1.0"

def detect_defects(image):
    """Run detection and return annotated image + detection data"""
    try:
        start_time = time.time()
        
        # Generate image hash for tracking
        image_hash = generate_image_hash(image)
        
        # Run YOLOv8 detection
        results = model(image)
        processing_time = time.time() - start_time
        
        # Extract detection information
        detections = []
        defect_types_count = {}
        
        if results[0].boxes is not None:
            boxes = results[0].boxes
            for i in range(len(boxes)):
                # Extract detection details
                box = boxes.xyxy[i].cpu().numpy()  # [x1, y1, x2, y2]
                confidence = float(boxes.conf[i].cpu().numpy())
                class_id = int(boxes.cls[i].cpu().numpy())
                
                # Get class name (defect type)
                defect_type = model.names[class_id] if class_id in model.names else f"class_{class_id}"
                
                # Count defect types
                defect_types_count[defect_type] = defect_types_count.get(defect_type, 0) + 1
                
                # Create detection object
                detection = DefectDetection(
                    timestamp=datetime.datetime.now().isoformat(),
                    image_hash=image_hash,
                    defect_type=defect_type,
                    confidence=confidence,
                    bbox=box.tolist(),
                    image_size=(image.shape[1], image.shape[0]),  # (width, height)
                    model_version=MODEL_VERSION
                )
                
                # Store in memory bank
                memory_bank.store_detection(detection)
                detections.append(detection)
        
        # Store performance metrics
        if detections:
            avg_confidence = sum(d.confidence for d in detections) / len(detections)
            performance = ModelPerformance(
                timestamp=datetime.datetime.now().isoformat(),
                total_detections=len(detections),
                avg_confidence=avg_confidence,
                defect_types_count=defect_types_count,
                processing_time=processing_time,
                model_version=MODEL_VERSION
            )
            memory_bank.store_performance_metrics(performance)
        
        # Create annotated image
        annotated_img = results[0].plot(line_width=2)
        annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        
        # Create detection summary
        detection_summary = format_detection_summary(detections)
        
        return annotated_img_rgb, detection_summary
        
    except Exception as e:
        print(f"Error: {e}")
        return image, f"Error during detection: {str(e)}"

def get_memory_bank_stats():
    """Get formatted memory bank statistics"""
    try:
        stats = memory_bank.get_defect_statistics()
        
        stats_text = f"""
## Memory Bank Statistics

**Total Detections:** {stats['total_detections']}

**Confidence Statistics:**
- Average: {stats['confidence_stats']['average']:.3f}
- Minimum: {stats['confidence_stats']['minimum']:.3f}
- Maximum: {stats['confidence_stats']['maximum']:.3f}

**Defect Type Distribution:**
"""
        
        for defect_type, info in stats['defect_distribution'].items():
            stats_text += f"- {defect_type}: {info['count']} detections (avg confidence: {info['avg_confidence']:.3f})\n"
        
        if stats['daily_stats_last_week']:
            stats_text += "\n**Last 7 Days Activity:**\n"
            for date, daily_info in stats['daily_stats_last_week'].items():
                stats_text += f"- {date}: {daily_info['count']} detections\n"
        
        return stats_text
        
    except Exception as e:
        return f"Error retrieving statistics: {str(e)}"

def clear_memory_bank():
    """Clear old data from memory bank"""
    try:
        memory_bank.clear_old_data(days_to_keep=30)
        return "Successfully cleared data older than 30 days."
    except Exception as e:
        return f"Error clearing data: {str(e)}"

# Enhanced UI with Memory Bank features
with gr.Blocks(title="🔧 Steel Surface Defect Detector with Memory Bank") as interface:
    gr.Markdown("# 🔧 Steel Surface Defect Detector with Memory Bank")
    gr.Markdown("Upload an image to detect surface defects (crazing, scratches, etc.) and track detection history.")
    
    with gr.Tab("Defect Detection"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(label="Upload Steel Surface Image", type="numpy")
                detect_btn = gr.Button("Detect Defects", variant="primary")
            
            with gr.Column():
                image_output = gr.Image(label="Detected Defects")
                detection_summary = gr.Textbox(
                    label="Detection Summary", 
                    lines=5, 
                    placeholder="Detection results will appear here..."
                )
        
        detect_btn.click(
            fn=detect_defects,
            inputs=image_input,
            outputs=[image_output, detection_summary]
        )
    
    with gr.Tab("Memory Bank Statistics"):
        with gr.Row():
            with gr.Column():
                stats_btn = gr.Button("Refresh Statistics", variant="secondary")
                clear_btn = gr.Button("Clear Old Data (30+ days)", variant="stop")
            
            with gr.Column():
                stats_output = gr.Markdown(label="Statistics")
                clear_output = gr.Textbox(label="Clear Data Result", lines=2)
        
        stats_btn.click(
            fn=get_memory_bank_stats,
            outputs=stats_output
        )
        
        clear_btn.click(
            fn=clear_memory_bank,
            outputs=clear_output
        )

if __name__ == "__main__":
    interface.launch()