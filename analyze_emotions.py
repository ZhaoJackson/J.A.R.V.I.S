# analyze_emotions.py - Emotion Data Analysis and Visualization

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from src.commonconst import CSV_EXPORT_PATH
from src.application.db_manager import get_emotion_statistics

def create_emotion_charts():
    """Create visualization charts for emotion data"""
    try:
        # Read the CSV data directly
        df = pd.read_csv(CSV_EXPORT_PATH)
        
        if df.empty:
            print("No emotion data found to visualize.")
            return
        
        # Create a figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('JARVIS Emotion Analysis Dashboard', fontsize=16)
        
        # 1. Most common emotions
        emotion_counts = df['Detected Emotion'].value_counts().head(10)
        ax1.bar(emotion_counts.index, emotion_counts.values)
        ax1.set_title('Top Emotions')
        ax1.set_xlabel('Emotions')
        ax1.set_ylabel('Frequency')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Philosophy books usage
        book_counts = df['Philosophy Book'].value_counts()
        ax2.pie(book_counts.values, labels=book_counts.index, autopct='%1.1f%%')
        ax2.set_title('Philosophy Books Usage')
        
        # 3. Music playlists
        playlist_counts = df['Music Playlist'].value_counts()
        ax3.bar(playlist_counts.index, playlist_counts.values)
        ax3.set_title('Music Playlists')
        ax3.set_xlabel('Playlists')
        ax3.set_ylabel('Times Played')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Daily activity (convert timestamp to date)
        df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
        daily_counts = df['Date'].value_counts().sort_index()
        ax4.plot(daily_counts.index, daily_counts.values, marker='o')
        ax4.set_title('Daily Emotion Sessions')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Sessions')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        chart_path = 'db/emotion_analysis.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Emotion charts saved to: {chart_path}")
        return chart_path
        
    except ImportError:
        print("📊 Install matplotlib and pandas for visualization: pip install matplotlib pandas")
    except Exception as e:
        print(f"❌ Chart creation failed: {e}")

def print_emotion_summary():
    """Print a text-based emotion summary"""
    stats = get_emotion_statistics()
    
    print("=" * 50)
    print("📊 JARVIS EMOTION ANALYSIS SUMMARY")
    print("=" * 50)
    
    print(f"📈 Total Sessions: {stats['total_sessions']}")
    print()
    
    print("😊 Top 5 Emotions:")
    for i, (emotion, count) in enumerate(stats['top_emotions'][:5], 1):
        print(f"  {i}. {emotion}: {count} times")
    print()
    
    print("📚 Philosophy Books Usage:")
    for i, (book, count) in enumerate(stats['top_books'], 1):
        print(f"  {i}. {book}: {count} times")
    print()
    
    print("📅 Recent Activity (Last 7 Days):")
    for date, count in stats['recent_activity']:
        print(f"  {date}: {count} sessions")
    
    print("=" * 50)

if __name__ == "__main__":
    print("🔍 Analyzing your emotion data...")
    
    # Print text summary
    print_emotion_summary()
    
    # Create charts if possible
    create_emotion_charts()
    
    # Show CSV location
    print(f"📄 Data file location: {CSV_EXPORT_PATH}")
    print("\n💡 You can open the CSV file in Excel or Google Sheets for detailed analysis!")
    print(f"📊 Charts updated: db/emotion_analysis.png")
    print("\n🔄 Run this script anytime to refresh the visualization!")
