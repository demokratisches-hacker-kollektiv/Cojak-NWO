#!/usr/bin/env python3
"""
RESEARCH & ADVANCED DOWNLOADER
Investigates and implements cutting-edge download methods
"""

import os
import subprocess
import time
import random
import json

def research_advanced_methods():
    """Research and implement advanced download methods"""
    print("RESEARCH MODE: INVESTIGATING ADVANCED DOWNLOAD METHODS")
    
    # Method 1: Try different extractors
    extractors = [
        'youtube',
        'youtube:tab', 
        'youtube:playlist',
        'youtube:video',
        'youtube:shorts',
        'youtube:live'
    ]
    
    # Method 2: Different format codes
    formats = [
        'worst',
        'worstvideo+worstaudio',
        'best[height<=360]',
        'best[height<=240]',
        'best[height<=144]',
        'mp4',
        'webm',
        '3gp'
    ]
    
    # Method 3: Different player clients
    clients = [
        'android',
        'android_music',
        'android_vr',
        'android_testsuite',
        'mweb',
        'ios',
        'ios_music',
        'tv',
        'tv_embedded',
        'mediaconnect',
        'watch_embedded',
        'embed',
        'create',
        'vr'
    ]
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    research_round = 0
    
    while True:
        research_round += 1
        print(f"\nRESEARCH ROUND #{research_round} - {time.strftime('%H:%M:%S')}")
        
        # Count current progress
        downloaded = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp')):
                downloaded += 1
        
        print(f"Current research results: {downloaded}/{len(video_ids)} videos acquired")
        
        if downloaded >= len(video_ids):
            print("🎉 RESEARCH COMPLETE - ALL VIDEOS ACQUIRED! 🎉")
            break
        
        # Find missing videos for research
        missing = []
        for video_id in video_ids:
            exists = False
            for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            if not exists:
                missing.append(video_id)
        
        print(f"Researching {len(missing)} missing videos...")
        
        # Test advanced methods on first 5 missing videos
        for i, video_id in enumerate(missing[:5]):
            print(f"  Research {i+1}: Testing {video_id}...")
            
            # Test different combinations
            test_combinations = [
                # Combination 1: Different extractor
                f'python -m yt_dlp --ies youtube "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-res1.%(ext)s" --format "worst" --no-playlist --ignore-errors',
                
                # Combination 2: Different client
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-res2.%(ext)s" --format "worst[height<=240]" --extractor-args "youtube:player_client=android_music" --no-playlist --ignore-errors',
                
                # Combination 3: TV client
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-res3.%(ext)s" --format "worst" --extractor-args "youtube:player_client=tv" --no-playlist --ignore-errors',
                
                # Combination 4: iOS client
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-res4.%(ext)s" --format "worst[height<=360]" --extractor-args "youtube:player_client=ios" --no-playlist --ignore-errors',
                
                # Combination 5: Embedded player
                f'python -m yt_dlp "https://www.youtube.com/embed/{video_id}" --output "video-archive/{video_id}-res5.%(ext)s" --format "worst" --no-playlist --ignore-errors',
                
                # Combination 6: NoCookie embed
                f'python -m yt_dlp "https://www.youtube-nocookie.com/embed/{video_id}" --output "video-archive/{video_id}-res6.%(ext)s" --format "worst" --no-playlist --ignore-errors',
                
                # Combination 7: Different format
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-res7.%(ext)s" --format "3gp" --no-playlist --ignore-errors',
                
                # Combination 8: Audio only (as backup)
                f'python -m yt_dlp "https://www.youtube.com/watch?v={video_id}" --output "video-archive/{video_id}-res8.%(ext)s" --extract-audio --audio-format "mp3" --no-playlist --ignore-errors'
            ]
            
            success = False
            for j, cmd in enumerate(test_combinations):
                try:
                    print(f"    Testing method {j+1}...", end=' ')
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45)
                    
                    if result.returncode == 0:
                        # Check for any file creation
                        for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp', '.mp3']:
                            for k in range(1, 9):
                                test_file = f'video-archive/{video_id}-res{k}{ext}'
                                if os.path.exists(test_file) and os.path.getsize(test_file) > 50000:
                                    final_file = f'video-archive/{video_id}{ext}'
                                    if not os.path.exists(final_file):
                                        os.rename(test_file, final_file)
                                        size = os.path.getsize(final_file)
                                        print(f"SUCCESS! Method {j+1} ({size/1024/1024:.1f}MB)")
                                        success = True
                                        break
                            if success:
                                break
                        
                        if not success:
                            print("No file")
                    else:
                        print("Failed")
                        
                except Exception as e:
                    print(f"Error: {str(e)[:30]}")
                
                if success:
                    break
                
                time.sleep(2)  # Wait between methods
            
            if not success:
                print(f"    All research methods failed for {video_id}")
            
            time.sleep(3)  # Wait between videos
        
        print(f"Research round {research_round} completed. Analyzing results...")
        time.sleep(20)  # Wait before next research round

if __name__ == "__main__":
    research_advanced_methods()
