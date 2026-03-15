#!/usr/bin/env python3
"""
INFINITE LOOP DOWNLOADER
Never stops, never gives up
"""

import os
import subprocess
import time

def infinite_loop():
    """Infinite download loop"""
    print("INFINITE LOOP DOWNLOADER - WILL NEVER STOP")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    loop_count = 0
    
    while True:
        loop_count += 1
        print(f"\nINFINITE LOOP #{loop_count} - {time.strftime('%H:%M:%S')}")
        
        # Count current downloads
        downloaded = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv')):
                downloaded += 1
        
        print(f"Progress: {downloaded}/{len(video_ids)}")
        
        if downloaded >= len(video_ids):
            print("🎉 INFINITE LOOP COMPLETE - ALL VIDEOS DOWNLOADED! 🎉")
            break
        
        # Try downloading first missing video with multiple methods
        for video_id in video_ids:
            # Check if exists
            exists = False
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            
            if not exists:
                print(f"Loop targeting {video_id}...")
                
                # Method 1: Basic
                try:
                    cmd1 = [
                        'python', '-m', 'yt_dlp',
                        f'https://www.youtube.com/watch?v={video_id}',
                        '--output', f'video-archive/{video_id}-inf.%(ext)s',
                        '--format', 'worst',
                        '--no-playlist',
                        '--ignore-errors'
                    ]
                    result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=30)
                    
                    if result1.returncode == 0:
                        for ext in ['.mp4', '.webm', '.mkv']:
                            test_file = f'video-archive/{video_id}-inf{ext}'
                            if os.path.exists(test_file) and os.path.getsize(test_file) > 100000:
                                final_file = f'video-archive/{video_id}{ext}'
                                if not os.path.exists(final_file):
                                    os.rename(test_file, final_file)
                                    print(f"INFINITE SUCCESS: {video_id}")
                                    break
                except:
                    pass
                
                time.sleep(3)
                break  # One video per loop iteration
        
        time.sleep(10)  # Wait before next loop

if __name__ == "__main__":
    infinite_loop()
