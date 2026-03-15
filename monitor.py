#!/usr/bin/env python3
"""
Download Monitor - Tracks progress of all downloaders
"""

import os
import time
from datetime import datetime

def count_downloaded_videos():
    """Count downloaded video files"""
    count = 0
    total_size = 0
    if os.path.exists('video-archive'):
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov')):
                count += 1
                total_size += os.path.getsize(f'video-archive/{file}')
    return count, total_size

def main():
    print("DOWNLOAD MONITOR - Tracking Progress")
    print("=" * 50)
    
    # Load total target
    with open('all_video_ids.txt', 'r') as f:
        total_videos = len([line.strip() for line in f if line.strip()])
    
    print(f"Target: {total_videos} videos")
    print(f"Started monitoring: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    last_count = 0
    while True:
        count, size = count_downloaded_videos()
        
        if count != last_count:
            progress = (count / total_videos) * 100
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloaded: {count}/{total_videos} ({progress:.1f}%) - {size/1024/1024:.1f}MB")
            last_count = count
        
        time.sleep(30)  # Check every 30 seconds
        
        if count >= total_videos:
            print("\n🎉 ALL VIDEOS DOWNLOADED! MISSION COMPLETE! 🎉")
            break

if __name__ == "__main__":
    main()
