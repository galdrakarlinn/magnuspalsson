# Video Processing Guide for Magnús Pálsson Archive

## Video Requirements

### Technical Specifications
- **Format**: MP4 (H.264 codec)
- **Duration**: 30 seconds to 2 minutes (preview clips)
- **Resolution**: 720p (1280x720) or 1080p (1920x1080) max
- **Frame rate**: 25fps or 30fps
- **File size**: Target under 10MB, max 20MB
- **Audio**: AAC codec, 128kbps
- **Naming**: `workname-preview.mp4` or `workname-video.mp4`

### Web Compatibility
- **Container**: MP4 (not MOV, AVI, or proprietary formats)
- **Video codec**: H.264 (most compatible)
- **Audio codec**: AAC (better than MP3 for video)
- **Compression**: High compression for web delivery
- **Mobile friendly**: Test on mobile devices

## Processing Workflow

### 1. Video Selection and Planning
From source material:
- **Identify key moments**: Most representative 30-120 seconds
- **Consider narrative**: Beginning, middle, end if applicable
- **Audio importance**: Include if integral to work
- **Quality assessment**: Choose best quality source

### 2. Editing Guidelines

#### For Performance/Conceptual Works:
- **Show process**: Setup, action, completion
- **Include audio** if it's part of the work
- **Maintain pacing** of original performance
- **Context shots**: Artist, audience, space

#### For Installation/Sculpture Works:
- **Multiple angles**: Show scale and context
- **Slow pans**: Allow viewers to absorb details
- **Detail shots**: Materials, craftsmanship
- **Environmental context**: Gallery, outdoor space

#### For Time-based Works:
- **Preserve essence**: Don't rush the experience
- **Key moments**: Most significant 1-2 minutes
- **Audio sync**: Maintain lip-sync if speech
- **Fade in/out**: Clean start and end

### 3. Compression Tools and Settings

#### Option A: HandBrake (Free, Recommended)
```
Preset: Web Optimized
Video Codec: H.264
Quality: RF 22-25 (lower = better quality)
Encoder: x264
Framerate: Same as source or 25fps
Resolution: 1280x720 (if source is larger)
Audio: AAC, 128kbps
```

#### Option B: FFmpeg (Command Line)
```bash
# Basic compression
ffmpeg -i input.mov -c:v libx264 -crf 25 -c:a aac -b:a 128k -vf scale=1280:720 output.mp4

# With duration trimming (30 seconds from start)
ffmpeg -i input.mov -t 30 -c:v libx264 -crf 25 -c:a aac -b:a 128k -vf scale=1280:720 output.mp4

# Extract specific segment (from 1:30 to 2:30)
ffmpeg -i input.mov -ss 90 -t 60 -c:v libx264 -crf 25 -c:a aac -b:a 128k output.mp4
```

#### Option C: Adobe Premiere/Final Cut
```
Export Settings:
- Format: H.264/MP4
- Resolution: 1280x720
- Frame Rate: 25fps
- Bitrate: VBR, 2-5 Mbps
- Audio: AAC, 128kbps
```

### 4. File Naming and Organization

#### Naming Convention:
- **Single video**: `workname-preview.mp4`
- **Multiple videos**: `workname-video-01.mp4`, `workname-video-02.mp4`
- **Audio only**: `workname-audio.mp3`
- **Documentation**: `workname-documentation.mp4`

#### Examples:
```
yxn-2002-preview.mp4
helicopter-landing-1976-video.mp4
augustus-my-god-1984-audio.mp3
```

### 5. Audio Processing

#### For Audio-Only Works:
- **Format**: MP3, 128-192kbps
- **Duration**: Can be longer than video (up to 5 minutes)
- **Normalization**: Consistent volume levels
- **Fade in/out**: Clean beginnings and endings

#### For Video with Important Audio:
- **Sync critical**: Maintain lip-sync
- **Clear dialogue**: Enhance voice if needed
- **Background noise**: Reduce if distracting
- **Music/effects**: Preserve artistic intent

### 6. Quality Control Checklist

Before adding each video:
- ✅ **Plays in browser**: Test Chrome, Safari, Firefox
- ✅ **Mobile compatible**: Test on phone/tablet
- ✅ **File size reasonable**: Under 10MB preferred
- ✅ **Audio sync**: Check lip-sync if applicable
- ✅ **Visual quality**: Clear, not overly compressed
- ✅ **Duration appropriate**: 30s-2min for previews
- ✅ **Starts/ends cleanly**: No abrupt cuts

### 7. Git Workflow for Videos

#### Important: Videos are in .gitignore
Videos need to be force-added to git:

```bash
# Navigate to magnuspalsson directory
cd magnuspalsson

# Force add video file (bypasses .gitignore)
git add -f images/work-folder/work-preview.mp4

# Commit and push
git commit -m "Add video preview for [Work Title]"
git push origin main
```

#### Verification:
1. **Check git status**: Ensure video is tracked
2. **Test locally**: Verify video plays at localhost:8000
3. **Check live site**: Confirm video appears after deployment

### 8. Troubleshooting Common Issues

#### Video Won't Play in Browser:
- **Check codec**: Must be H.264 in MP4 container
- **Verify file path**: Exact filename in JSON
- **Test different browsers**: Chrome, Safari, Firefox
- **Check console errors**: Browser developer tools

#### File Too Large:
- **Increase compression**: Higher CRF value (FFmpeg)
- **Reduce resolution**: 720p instead of 1080p
- **Shorter duration**: Trim to most essential moments
- **Remove audio**: If not essential to the work

#### Poor Quality After Compression:
- **Lower CRF value**: Better quality (FFmpeg)
- **Check source quality**: May need better original
- **Two-pass encoding**: Better quality (slower)
- **Adjust bitrate**: Higher bitrate for complex scenes

### 9. Special Considerations

#### Historic Video Materials:
- **Preserve artifacts**: Don't over-clean vintage footage
- **Respect original format**: 4:3 aspect ratio if original
- **Color correction**: Minimal, maintain artistic intent
- **Audio restoration**: Clean up tape hiss if severe

#### Performance Documentation:
- **Multiple cameras**: Edit together if available
- **Audience reactions**: Include if relevant
- **Environmental sound**: Gallery acoustics, ambient noise
- **Artist statements**: Include voice-over if available

#### Installation Views:
- **Establishing shots**: Wide views showing scale
- **Detail exploration**: Close-ups of components
- **Visitor interaction**: People engaging with work
- **Time passage**: Show changes over time if relevant

## Tools and Software

### Free Tools:
- **HandBrake**: Excellent compression tool
- **FFmpeg**: Command-line Swiss Army knife
- **OpenShot**: Simple video editor
- **DaVinci Resolve**: Professional editor (free version)

### Professional Tools:
- **Adobe Premiere Pro**: Industry standard
- **Final Cut Pro**: Mac video editing
- **Avid Media Composer**: Professional editing
- **Compressor**: Mac compression tool

### Online Tools:
- **CloudConvert**: Online video conversion
- **Clipchamp**: Browser-based editor
- **Kapwing**: Simple online video tools

## Getting Started

1. **Download test video** from Dropbox
2. **Practice with HandBrake**: Compress to web specs
3. **Test local playback**: Verify browser compatibility
4. **Force add to git**: Learn the git workflow
5. **Check live deployment**: Ensure it works on magnuspalsson.is

Remember: Web videos are previews - they should entice viewers while loading quickly on all devices.