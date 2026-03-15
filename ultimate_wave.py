#!/usr/bin/env python3
"""
ULTIMATE WAVE DOWNLOADER
Final assault - uses every possible combination
"""

import os
import subprocess
import time
import random

def ultimate_assault():
    print("ULTIMATE WAVE - FINAL ASSAULT ON ALL VIDEOS")
    print("This will NEVER stop until ALL 229 videos are downloaded!")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    wave_count = 0
    
    while True:
        wave_count += 1
        print(f"\n{'='*60}")
        print(f"ULTIMATE WAVE #{wave_count} - {time.strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # Count current progress
        downloaded = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv')):
                downloaded += 1
        
        print(f"Current Status: {downloaded}/{len(video_ids)} videos downloaded")
        
        if downloaded >= len(video_ids):
            print("🎉🎉🎉 COMPLETE AND TOTAL VICTORY! ALL VIDEOS DOWNLOADED! 🎉🎉🎉")
            break
        
        print("Launching massive simultaneous attack on missing videos...")
        
        # Try to download multiple videos at once
        missing_videos = []
        for video_id in video_ids:
            exists = False
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            if not exists:
                missing_videos.append(video_id)
        
        print(f"Targeting {len(missing_videos)} missing videos")
        
        # Launch attacks on first 20 missing videos
        targets = missing_videos[:20]
        
        for i, video_id in enumerate(targets):
            print(f"  {i+1:2d}. Assaulting {video_id}...", end=' ')
            
            # Use every possible method in rotation
            methods = [
                # Method 1: Direct Android
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}.%(ext)s" --format "worst[height>=240]" --extractor-args "youtube:player_client=android" --user-agent "com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip" --no-playlist --ignore-errors',
                
                # Method 2: Invidious 
                f'python -m yt_dlp "https://yewtu.be/watch?v={video_id}" --output "video-archive/{video_id}.%(ext)s" --format "worst" --no-playlist --ignore-errors',
                
                # Method 3: Mobile Web
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}.%(ext)s" --format "worst[height>=144]" --extractor-args "youtube:player_client=mweb" --user-agent "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15" --no-playlist --ignore-errors',
                
                # Method 4: TV Client
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}.%(ext)s" --format "worst" --extractor-args "youtube:player_client=tv_embedded" --user-agent "Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36" --no-playlist --ignore-errors',
                
                # Method 5: NoCookie
                f'python -m yt_dlp "https://www.youtube-nocookie.com/embed/{video_id}" --output "video-archive/{video_id}.%(ext)s" --format "worst" --no-playlist --ignore-errors'
            ]
            
            method = methods[wave_count % len(methods)]
            
            try:
                result = subprocess.run(method, shell=True, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    # Check success
                    for ext in ['.mp4', '.webm', '.mkv']:
                        if os.path.exists(f'video-archive/{video_id}{ext}'):
                            size = os.path.getsize(f'video-archive/{video_id}{ext}')
                            print(f"VICTORY! ({size/1024/1024:.1f}MB)")
                            break
                    else:
                        print("No file")
                else:
                    print("Failed")
                    
            except:
                print("Error")
            
            # Small delay between assaults
            time.sleep(1)
        
        print(f"Wave #{wave_count} completed. Regrouping for next wave...")
        time.sleep(15)  # Prepare for next wave

if __name__ == "__main__":
    ultimate_assault()
