#!/usr/bin/env python3
"""
FINAL ASSAULT DOWNLOADER
The ultimate download machine
"""

import os
import subprocess
import time
import threading

def final_assault_worker():
    """Final assault worker"""
    print("FINAL ASSAULT DOWNLOADER - ULTIMATE MODE ACTIVATED")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    assault_count = 0
    
    while True:
        assault_count += 1
        print(f"\nFINAL ASSAULT #{assault_count} - {time.strftime('%H:%M:%S')}")
        
        # Count downloads
        downloaded = 0
        total_size = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv')):
                downloaded += 1
                total_size += os.path.getsize(f'video-archive/{file}')
        
        progress = (downloaded / len(video_ids)) * 100
        print(f"PROGRESS: {downloaded}/{len(video_ids)} ({progress:.1f}%) - {total_size/1024/1024:.1f}MB")
        
        if downloaded >= len(video_ids):
            print("🎉🎉🎉 FINAL ASSAULT VICTORY! ALL VIDEOS DOWNLOADED! 🎉🎉🎉")
            break
        
        # Find missing videos
        missing = []
        for video_id in video_ids:
            exists = False
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            if not exists:
                missing.append(video_id)
        
        print(f"ASSAULTING {len(missing)} MISSING VIDEOS")
        
        # Assault first 10 missing videos
        for i, video_id in enumerate(missing[:10]):
            print(f"  {i+1:2d}. Assaulting {video_id}...", end=' ')
            
            # Try every possible method
            methods = [
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-final.%(ext)s" --format "worst" --no-playlist --ignore-errors',
                f'python -m yt_dlp "https://yewtu.be/watch?v={video_id}" --output "video-archive/{video_id}-final.%(ext)s" --format "worst" --no-playlist --ignore-errors',
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-final.%(ext)s" --format "worst[height>=240]" --extractor-args "youtube:player_client=android" --no-playlist --ignore-errors'
            ]
            
            success = False
            for method in methods:
                try:
                    result = subprocess.run(method, shell=True, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        # Check success
                        for ext in ['.mp4', '.webm', '.mkv']:
                            test_file = f'video-archive/{video_id}-final{ext}'
                            if os.path.exists(test_file) and os.path.getsize(test_file) > 100000:
                                final_file = f'video-archive/{video_id}{ext}'
                                if not os.path.exists(final_file):
                                    os.rename(test_file, final_file)
                                    print(f"VICTORY! ({os.path.getsize(final_file)/1024/1024:.1f}MB)")
                                    success = True
                                    break
                        
                        if success:
                            break
                            
                except:
                    continue
            
            if not success:
                print("Failed")
            
            time.sleep(2)
        
        print(f"Assault #{assault_count} completed. Preparing next assault...")
        time.sleep(15)

if __name__ == "__main__":
    final_assault_worker()
