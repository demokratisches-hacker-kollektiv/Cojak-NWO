#!/usr/bin/env python3
"""
RAPID FIRE DOWNLOADER
High-speed video acquisition system
"""

import os
import subprocess
import time
import random
from concurrent.futures import ThreadPoolExecutor

def rapid_fire_download():
    """Ultra-fast downloader with multiple threads"""
    print("RAPID FIRE DOWNLOADER - MAXIMUM SPEED ACTIVATED")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    def download_single_rapid(video_id):
        """Download one video as fast as possible"""
        # Check if already downloaded
        for ext in ['.mp4', '.webm', '.mkv']:
            if os.path.exists(f'video-archive/{video_id}{ext}'):
                return False
        
        # Try fastest method first
        cmd = [
            'python', '-m', 'yt_dlp',
            f'https://www.youtube.com/watch?v={video_id}',
            '--output', f'video-archive/{video_id}-rapid.%(ext)s',
            '--format', 'worst',
            '--no-playlist',
            '--ignore-errors',
            '--retries', '1',
            '--socket-timeout', '30'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            
            if result.returncode == 0:
                # Check and rename file
                for ext in ['.mp4', '.webm', '.mkv']:
                    test_file = f'video-archive/{video_id}-rapid{ext}'
                    if os.path.exists(test_file) and os.path.getsize(test_file) > 100000:
                        final_file = f'video-archive/{video_id}{ext}'
                        if not os.path.exists(final_file):
                            os.rename(test_file, final_file)
                            print(f"RAPID: {video_id} DOWNLOADED!")
                            return True
        except:
            pass
        
        return False
    
    round_count = 0
    while True:
        round_count += 1
        print(f"\nRAPID FIRE ROUND #{round_count}")
        
        # Get missing videos
        missing = []
        for video_id in video_ids:
            exists = False
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            if not exists:
                missing.append(video_id)
        
        if not missing:
            print("🎉 ALL VIDEOS DOWNLOADED! RAPID FIRE MISSION COMPLETE! 🎉")
            break
        
        print(f"Targeting {len(missing)} videos with rapid fire...")
        
        # Download with high parallelism
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(download_single_rapid, vid) for vid in missing[:50]]
            
            success_count = 0
            for future in futures:
                try:
                    if future.result():
                        success_count += 1
                except:
                    pass
            
            print(f"Rapid fire round result: +{success_count} videos")
        
        time.sleep(5)  # Brief pause between rounds

if __name__ == "__main__":
    rapid_fire_download()
