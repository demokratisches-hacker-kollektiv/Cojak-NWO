#!/usr/bin/env python3
"""
BROWSER-BASED YOUTUBE DOWNLOADER
Uses real browser to bypass restrictions
"""

import os
import time
import subprocess
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def browser_download_worker(worker_id):
    """Browser-based download worker"""
    print(f"Browser Worker {worker_id} starting...")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        # Initialize browser
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        with open('all_video_ids.txt', 'r') as f:
            video_ids = [line.strip() for line in f if line.strip()]
        
        while True:
            for video_id in video_ids:
                # Check if already downloaded
                downloaded = False
                for ext in ['.mp4', '.webm', '.mkv']:
                    if os.path.exists(f'video-archive/{video_id}{ext}'):
                        downloaded = True
                        break
                
                if not downloaded:
                    print(f"Browser Worker {worker_id}: Trying {video_id}")
                    
                    try:
                        # Navigate to video
                        driver.get(f'https://www.youtube.com/watch?v={video_id}')
                        time.sleep(3)
                        
                        # Try to get video title for verification
                        try:
                            title = driver.title
                            print(f"Browser Worker {worker_id}: Found video: {title[:50]}...")
                        except:
                            print(f"Browser Worker {worker_id}: Accessed video page")
                        
                        # Now try to download using yt-dlp with browser cookies
                        cmd = [
                            'python', '-m', 'yt_dlp',
                            f'https://www.youtube.com/watch?v={video_id}',
                            '--output', f'video-archive/{video_id}-browser{worker_id}.%(ext)s',
                            '--format', 'worst[height>=240]',
                            '--no-playlist',
                            '--ignore-errors',
                            '--cookies-from-browser', 'chrome'
                        ]
                        
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                        
                        if result.returncode == 0:
                            # Check and rename file
                            for ext in ['.mp4', '.webm', '.mkv']:
                                test_file = f'video-archive/{video_id}-browser{worker_id}{ext}'
                                if os.path.exists(test_file) and os.path.getsize(test_file) > 500000:
                                    final_file = f'video-archive/{video_id}{ext}'
                                    if not os.path.exists(final_file):
                                        os.rename(test_file, final_file)
                                        print(f"Browser Worker {worker_id}: SUCCESS! Downloaded {video_id}")
                                    break
                        
                        # Random delay to avoid detection
                        time.sleep(random.uniform(5, 15))
                        
                    except Exception as e:
                        print(f"Browser Worker {worker_id}: Error with {video_id}: {str(e)[:50]}")
                        time.sleep(10)
            
            time.sleep(30)  # Brief pause before restarting cycle
            
    except Exception as e:
        print(f"Browser Worker {worker_id}: Critical error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    worker_id = int(os.getenv('WORKER_ID', '1'))
    browser_download_worker(worker_id)
