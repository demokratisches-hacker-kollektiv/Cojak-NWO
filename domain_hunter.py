#!/usr/bin/env python3
"""
DOMAIN HUNTER DOWNLOADER
Hunts videos across all YouTube domains and mirrors
"""

import os
import subprocess
import time

def domain_hunter():
    """Hunter that searches all YouTube domains"""
    print("DOMAIN HUNTER - SCANNING ALL YOUTUBE DOMAINS")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    # All possible YouTube domains and methods
    domains = [
        # Standard YouTube
        f'https://www.youtube.com/watch?v={{video_id}}',
        f'https://youtube.com/watch?v={{video_id}}',
        f'https://m.youtube.com/watch?v={{video_id}}',
        
        # YouTube embeds
        f'https://www.youtube.com/embed/{{video_id}}',
        f'https://youtube.com/embed/{{video_id}}',
        f'https://www.youtube-nocookie.com/embed/{{video_id}}',
        
        # YouTube short links
        f'https://youtu.be/{{video_id}}',
        
        # Invidious instances (alternative frontends)
        f'https://yewtu.be/watch?v={{video_id}}',
        f'https://yewtu.be/watch?v={{video_id}}?local',
        f'https://yewtu.be/watch?v={{video_id}}&quality=240',
        f'https://invidious.snopyta.org/watch?v={{video_id}}',
        f'https://yewtu.be/api/v1/videos/{{video_id}}',
        
        # Other YouTube alternatives
        f'https://yewtu.be/latest_version',
        f'https://tube.cadence.moe/watch?v={{video_id}}',
        f'https://yewtu.be/watch?v={{video_id}}&format=json'
    ]
    
    hunt_count = 0
    
    while True:
        hunt_count += 1
        print(f"\nDOMAIN HUNT #{hunt_count} - {time.strftime('%H:%M:%S')}")
        
        # Count current downloads
        downloaded = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov')):
                downloaded += 1
        
        print(f"Hunt progress: {downloaded}/{len(video_ids)} videos captured")
        
        if downloaded >= len(video_ids):
            print("🎯 DOMAIN HUNT COMPLETE - ALL VIDEOS CAPTURED! 🎯")
            break
        
        # Find missing videos
        missing = []
        for video_id in video_ids:
            exists = False
            for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            if not exists:
                missing.append(video_id)
        
        print(f"Hunting across {len(domains)} domains for {len(missing)} missing videos...")
        
        # Hunt first 3 missing videos across all domains
        for i, video_id in enumerate(missing[:3]):
            print(f"  Hunt {i+1}: Tracking {video_id} across domains...")
            
            for j, domain_template in enumerate(domains):
                url = domain_template.replace('{{video_id}}', video_id)
                print(f"    Domain {j+1}: {url.split('//')[1].split('/')[0]}...", end=' ')
                
                try:
                    cmd = [
                        'python', '-m', 'yt_dlp', url,
                        '--output', f'video-archive/{video_id}-hunt{j}.%(ext)s',
                        '--format', 'worst',
                        '--no-playlist',
                        '--ignore-errors',
                        '--retries', '1',
                        '--socket-timeout', '20'
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        # Check for success
                        for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                            test_file = f'video-archive/{video_id}-hunt{j}{ext}'
                            if os.path.exists(test_file) and os.path.getsize(test_file) > 50000:
                                final_file = f'video-archive/{video_id}{ext}'
                                if not os.path.exists(final_file):
                                    os.rename(test_file, final_file)
                                    size = os.path.getsize(final_file)
                                    print(f"CAPTURED! ({size/1024/1024:.1f}MB)")
                                    break
                        else:
                            print("No file")
                    else:
                        print("Failed")
                        
                except Exception as e:
                    print(f"Error: {str(e)[:20]}")
                
                # Check if we got the video
                for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                    if os.path.exists(f'video-archive/{video_id}{ext}'):
                        print(f"    ✓ {video_id} successfully captured!")
                        break
                else:
                    continue  # Try next domain
                break  # Video captured, move to next video
            
            time.sleep(5)  # Wait between videos
        
        print(f"Hunt #{hunt_count} completed. Regrouping for next hunt...")
        time.sleep(30)

if __name__ == "__main__":
    domain_hunter()
