#!/usr/bin/env python3
"""
NEVER SURRENDER DOWNLOADER
Keeps trying the most basic approach forever
"""

import os
import subprocess
import time

def main():
    print("NEVER SURRENDER DOWNLOADER")
    print("Will keep trying until ALL videos are downloaded!")
    print("=" * 60)
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    print(f"Target: {len(video_ids)} videos")
    
    attempt = 0
    while True:
        attempt += 1
        print(f"\nATTEMPT #{attempt} - {time.strftime('%H:%M:%S')}")
        
        # Count current downloads
        downloaded = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv')):
                downloaded += 1
        
        print(f"Current progress: {downloaded}/{len(video_ids)}")
        
        if downloaded >= len(video_ids):
            print("🎉 MISSION ACCOMPLISHED! ALL VIDEOS DOWNLOADED! 🎉")
            break
        
        # Try downloading first missing video
        for video_id in video_ids:
            # Check if already downloaded
            already_exists = False
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    already_exists = True
                    break
            
            if not already_exists:
                print(f"Trying {video_id}...", end=' ')
                
                # Simplest possible command
                cmd = [
                    'python', '-m', 'yt_dlp', 
                    f'https://www.youtube.com/watch?v={video_id}',
                    '--output', f'video-archive/{video_id}.%(ext)s',
                    '--format', 'worst',
                    '--no-playlist',
                    '--ignore-errors'
                ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        # Check if file created
                        for ext in ['.mp4', '.webm', '.mkv']:
                            if os.path.exists(f'video-archive/{video_id}{ext}'):
                                size = os.path.getsize(f'video-archive/{video_id}{ext}')
                                print(f"SUCCESS! ({size/1024/1024:.1f}MB)")
                                break
                        else:
                            print("No file created")
                    else:
                        print("Failed")
                        
                except:
                    print("Error")
                
                break  # Only try one video per attempt
        
        # Wait before next attempt
        print("Waiting 30 seconds...")
        time.sleep(30)

if __name__ == "__main__":
    main()
