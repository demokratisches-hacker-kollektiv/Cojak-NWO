# Video Download Verification Script
# Ensure all 318 PUSH IT H-TOWN videos are downloaded

# Check if URLs file exists and has content
if (!(Test-Path "video_urls.txt")) {
    Write-Host "video_urls.txt not found. Extracting URLs..."
    python scrape-videos.js
}

$urls = Get-Content "video_urls.txt" | Where-Object { $_ -match "https://" }
$urlCount = $urls.Count
Write-Host "Found $urlCount video URLs"

# Check download archive
$downloadedCount = 0
if (Test-Path "downloaded.txt") {
    $downloadedCount = (Get-Content "downloaded.txt" | Measure-Object -Line).Lines
}
Write-Host "Downloaded videos: $downloadedCount"

# Check actual video files
$videoFiles = Get-ChildItem "video-archive" -Filter "*.mp4" | Measure-Object
$actualCount = $videoFiles.Count
Write-Host "Video files in archive: $actualCount"

# Calculate completion
$completionRate = if ($urlCount -gt 0) { [math]::Round(($actualCount / $urlCount) * 100, 2) } else { 0 }
Write-Host "Completion rate: $completionRate%"

# If incomplete, initiate download
if ($actualCount -lt $urlCount) {
    Write-Host "Downloads incomplete. Initiating download process..."
    
    # Use yt-dlp to download with archive
    yt-dlp --batch-file video_urls.txt --download-archive downloaded.txt --output "video-archive/%(title)s.%(ext)s" --format "best[height<=720]" --retries 10 --sleep-interval 1 --max-sleep-interval 5 --continue --ignore-errors
}

# Final verification
$finalFiles = Get-ChildItem "video-archive" -Filter "*.mp4" | Measure-Object
$finalCount = $finalFiles.Count
$finalRate = if ($urlCount -gt 0) { [math]::Round(($finalCount / $urlCount) * 100, 2) } else { 0 }
Write-Host "Final completion: $finalCount / $urlCount videos ($finalRate%)"

# Update report
$reportContent = @"
# Complete Video Archive Download Report

## Download Statistics
- **Total Videos Expected**: $urlCount
- **Videos Successfully Downloaded**: $finalCount
- **Download Archive Entries**: $downloadedCount
- **Total Storage Used**: TBD
- **Download Completion Rate**: $finalRate%

## Download Configuration
- **Tool Used**: yt-dlp (YouTube downloader)
- **Format**: Best quality up to 720p
- **Location**: video-archive/ subdirectory
- **Retry Policy**: 10 retries per video
- **Resume Capability**: Enabled via download archive

## Files Created
- **video_urls.txt**: List of all video URLs ($urlCount entries)
- **downloaded.txt**: Download archive tracking
- **video-archive/**: Directory containing downloaded videos

## Verification Process
1. URL extraction from pushit-videos.json
2. Archive-based resume downloads
3. File count verification
4. Storage size calculation

**Status**: $(if ($finalRate -eq 100) { "COMPLETE" } else { "INCOMPLETE - REQUIRES RETRY" })
"@

$reportContent | Out-File -FilePath "video-archive/download-report.md" -Encoding UTF8
Write-Host "Report updated in video-archive/download-report.md"
