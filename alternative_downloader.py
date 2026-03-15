#!/usr/bin/env python3
"""
ALTERNATIVE FRONTEND DOWNLOADER
Uses different YouTube frontends to bypass restrictions
"""

import os
import subprocess
import time
import random

def load_video_ids():
    with open('all_video_ids.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def try_alternative_frontends(video_id):
    """Try downloading through various alternative frontends"""
    
    frontends = [
        # Invidious instances
        f'https://yewtu.be/watch?v={video_id}',
        f'https://yewtu.be/watch?v={video_id}?local=1', 
        f'https://invidious.snopyta.org/watch?v={video_id}',
        f'https://yewtu.be/api/v1/videos/{video_id}',
        
        # YouTube NoCookie
        f'https://www.youtube-nocookie.com/embed/{video_id}',
        
        # Direct approach with different parameters
        f'https://www.youtube.com/watch?v={video_id}&hl=en&disable_polymer=1',
        f'https://www.youtube.com/watch?v={video_id}&nomobile=1',
    ]
    
    for i, url in enumerate(frontends):
        print(f"  Frontend {i+1}: ", end='')
        
        if 'embed' in url:
            # For embed URLs, we need a different approach
            cmd = [
                'python', '-m', 'yt_dlp', url,
                '--output', f'video-archive/{video_id}-embed.%(ext)s',
                '--format', 'worst',
                '--no-playlist',
                '--ignore-errors'
            ]
        else:
            cmd = [
                'python', '-m', 'yt_dlp', url,
                '--output', f'video-archive/{video_id}-alt{i}.%(ext)s',
                '--format', 'worst[height>=240]',
                '--no-playlist',
                '--ignore-errors',
                '--user-agent', random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                ])
            ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            
            if result.returncode == 0:
                # Check for created files
                for ext in ['.mp4', '.webm', '.mkv']:
                    for suffix in ['', '-embed', f'-alt{i}']:
                        test_file = f'video-archive/{video_id}{suffix}{ext}'
                        if os.path.exists(test_file) and os.path.getsize(test_file) > 500000:
                            # Rename to standard format
                            final_name = f'video-archive/{video_id}{ext}'
                            if test_file != final_name:
                                os.rename(test_file, final_name)
                            print(f"SUCCESS! ({os.path.getsize(final_name)/1024/1024:.1f}MB)")
                            return True
            
            print("Failed")
            
        except subprocess.TimeoutExpired:
            print("Timeout")
        except Exception as e:
            print(f"Error: {str(e)[:30]}")
        
        time.sleep(2)  # Wait between frontends
    
    return False

def main():
    print("ALTERNATIVE FRONTEND DOWNLOADER")
    print("=" * 50)
    print("Trying different YouTube frontends to bypass restrictions...")
    
    os.makedirs('video-archive', exist_ok=True)
    
    video_ids = load_video_ids()
    print(f"Target: {len(video_ids)} videos")
    
    # Check what's already downloaded
    already_downloaded = set()
    for file in os.listdir('video-archive'):
        if file.endswith(('.mp4', '.webm', '.mkv')):
            video_id = file.split('.')[0].split('-')[0]
            already_downloaded.add(video_id)
    
    print(f"Already downloaded: {len(already_downloaded)}")
    
    missing = [vid for vid in video_ids if vid not in already_downloaded]
    print(f"Still need: {len(missing)}")
    
    success_count = 0
    for i, video_id in enumerate(missing[:30]):  # Try first 30
        print(f"{i+1:2d}. Trying {video_id}:")
        
        if try_alternative_frontends(video_id):
            success_count += 1
        
        # Random delay
        time.sleep(random.uniform(3, 8))
    
    print(f"\nAlternative frontend results: {success_count} new downloads")
    print(f"Total progress: {len(already_downloaded) + success_count}/{len(video_ids)}")

if __name__ == "__main__":
    main()
