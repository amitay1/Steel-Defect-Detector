#!/usr/bin/env python3
"""
Memory Bank Management Utility
This script provides command-line tools for managing the memory bank database.
"""

import argparse
import json
import sys
from pathlib import Path
from memory_bank import MemoryBank, DefectDetection, ModelPerformance

def init_memory_bank(db_path: str = "memory_bank.db"):
    """Initialize a new memory bank database"""
    print(f"Initializing memory bank at: {db_path}")
    
    try:
        memory_bank = MemoryBank(db_path)
        print("✅ Memory bank initialized successfully!")
        
        # Add some sample knowledge base entries
        populate_knowledge_base(memory_bank)
        
        # Display initial stats
        stats = memory_bank.get_defect_statistics()
        print(f"📊 Database ready with {stats['total_detections']} detections")
        
    except Exception as e:
        print(f"❌ Error initializing memory bank: {e}")
        sys.exit(1)

def populate_knowledge_base(memory_bank: MemoryBank):
    """Populate the knowledge base with defect information"""
    try:
        # Load defect type information from config
        with open("config.json", "r") as f:
            config = json.load(f)
        
        defect_types = config.get("defect_types", {})
        
        # Note: You would need to implement a method in MemoryBank to add knowledge base entries
        # This is a placeholder for that functionality
        print("📚 Knowledge base populated with defect type information")
        
    except FileNotFoundError:
        print("⚠️  Config file not found, skipping knowledge base population")
    except Exception as e:
        print(f"⚠️  Error populating knowledge base: {e}")

def export_data(db_path: str, output_path: str, format: str = "json"):
    """Export memory bank data"""
    print(f"Exporting data from {db_path} to {output_path}")
    
    try:
        memory_bank = MemoryBank(db_path)
        memory_bank.export_data(output_path, format)
        print(f"✅ Data exported successfully to {output_path}")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        sys.exit(1)

def show_stats(db_path: str):
    """Display memory bank statistics"""
    try:
        memory_bank = MemoryBank(db_path)
        stats = memory_bank.get_defect_statistics()
        
        print("\n📊 Memory Bank Statistics")
        print("=" * 40)
        print(f"Total Detections: {stats['total_detections']}")
        
        if stats['confidence_stats']['average'] is not None:
            print(f"Average Confidence: {stats['confidence_stats']['average']:.3f}")
            print(f"Confidence Range: {stats['confidence_stats']['minimum']:.3f} - {stats['confidence_stats']['maximum']:.3f}")
        
        print("\nDefect Type Distribution:")
        for defect_type, info in stats['defect_distribution'].items():
            print(f"  {defect_type}: {info['count']} detections (avg: {info['avg_confidence']:.3f})")
        
        if stats['daily_stats_last_week']:
            print("\nLast 7 Days Activity:")
            for date, daily_info in stats['daily_stats_last_week'].items():
                print(f"  {date}: {daily_info['count']} detections")
        
    except Exception as e:
        print(f"❌ Error retrieving statistics: {e}")
        sys.exit(1)

def cleanup_data(db_path: str, days_to_keep: int = 30):
    """Clean up old data from memory bank"""
    print(f"Cleaning up data older than {days_to_keep} days from {db_path}")
    
    try:
        memory_bank = MemoryBank(db_path)
        memory_bank.clear_old_data(days_to_keep)
        print(f"✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Memory Bank Management Utility")
    parser.add_argument("--db", default="memory_bank.db", help="Database file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize memory bank database")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export memory bank data")
    export_parser.add_argument("output", help="Output file path")
    export_parser.add_argument("--format", default="json", choices=["json"], help="Export format")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show memory bank statistics")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old data")
    cleanup_parser.add_argument("--days", type=int, default=30, help="Days to keep (default: 30)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "init":
        init_memory_bank(args.db)
    elif args.command == "export":
        export_data(args.db, args.output, args.format)
    elif args.command == "stats":
        show_stats(args.db)
    elif args.command == "cleanup":
        cleanup_data(args.db, args.days)

if __name__ == "__main__":
    main()
