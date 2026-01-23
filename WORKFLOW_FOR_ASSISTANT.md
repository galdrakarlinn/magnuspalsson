# Magnús Pálsson Archive - Assistant Workflow

## Overview
Adding ~160 artworks from Dropbox folders to the magnuspalsson.is website. Each Dropbox folder contains images, sometimes videos, and occasionally text descriptions.

## Current Status
- ✅ 10 works already added to website
- 🎯 ~160 works remaining to process
- 📍 All source materials in Dropbox folders

## Workflow Steps

### 1. FOLDER ANALYSIS
For each Dropbox folder:
- **Folder name** = artwork title
- **Identify year** (often in folder name or text files)
- **Count images/videos** available
- **Read any text files** for descriptions/context
- **Note special requirements** (videos to shorten, high-res images to compress)

### 2. IMAGE PROCESSING

#### Image Requirements:
- **Web images**: 800-1200px wide max
- **Thumbnails**: 400px wide max
- **File format**: JPG (JPEG quality 80-85%)
- **File naming**: MUST use suffix `-medium` or `-thumb` (see below)
- **Select 3-8 best images** per work (not all images needed)

#### IMPORTANT: Folder Structure & Naming Convention
**MUST follow this exact structure:**
```
images/work-id/
  ├── medium/
  │   ├── work-id-01-medium.jpg
  │   ├── work-id-02-medium.jpg
  │   └── work-id-03-medium.jpg
  └── thumbs/           (note: "thumbs" with 's', NOT "thumb")
      ├── work-id-01-thumb.jpg
      ├── work-id-02-thumb.jpg
      └── work-id-03-thumb.jpg
```

**Key naming rules:**
- Folder name: `thumbs/` (plural with 's')
- Medium files: `workname-##-medium.jpg`
- Thumb files: `workname-##-thumb.jpg`
- Always include the `-medium` or `-thumb` suffix!

#### Image Processing Steps:
1. **Select best images** - choose most representative/highest quality
2. **Create folder structure** - `images/work-id/medium/` and `images/work-id/thumbs/`
3. **Resize for medium** - max 1200px wide, maintain aspect ratio, save as `work-id-##-medium.jpg`
4. **Resize for thumbs** - max 400px wide, maintain aspect ratio, save as `work-id-##-thumb.jpg`
5. **Compress** - JPEG quality 85% for medium, 80% for thumbs

#### Tools for Image Processing:
- **Photoshop/GIMP**: Batch resize and compress
- **Online tools**: TinyPNG, Squoosh.app for compression
- **Bulk rename tools**: Better File Rename, Name Mangler

### 3. VIDEO PROCESSING

#### Video Requirements:
- **Format**: MP4 (H.264 codec)
- **Duration**: 30 seconds to 2 minutes max for previews
- **Resolution**: 720p or 1080p max
- **File size**: Under 10MB if possible
- **Naming**: `workname-preview.mp4`

#### Video Processing Steps:
1. **Shorten videos** to key moments/highlights
2. **Compress** for web playback
3. **Test playback** on mobile devices
4. **Force add to git** (videos are in .gitignore)

#### Tools for Video Processing:
- **HandBrake**: Free compression tool
- **FFmpeg**: Command line tool for cutting/compressing
- **QuickTime**: Basic editing and export

### 4. WORK ENTRY TEMPLATE

Each artwork needs this JSON structure in `works.json`:

**IMPORTANT:** ALL works MUST include the `exhibitions` field, even if empty!

```json
{
  "id": "work_title_year",
  "title": "Artwork Title",
  "year": 1975,
  "description": "Detailed description of the work, materials, context, and significance. Include any available historical information.",
  "images": [
    {
      "url": "images/work-title-year/medium/work-title-year-01-medium.jpg",
      "caption": "Descriptive caption",
      "thumbnail": "images/work-title-year/thumbs/work-title-year-01-thumb.jpg"
    }
  ],
  "tags": ["sculpture", "performance", "video", "sound", "installation"],
  "exhibitions": [],
  "materials": ["plaster", "video", "sound", "metal"],
  "searchText": "relevant keywords for search functionality",
  "contentStatus": "draft",
  "mediaStatus": "images draft"
}
```

**Required fields (MUST be included):**
- `id` - work identifier (lowercase, hyphens)
- `title` - work title
- `year` - year created
- `description` - description text
- `images` - array of image objects with `url`, `caption`, and `thumbnail`
- `tags` - array of tags
- `exhibitions` - array (can be empty `[]` if no exhibitions)
- `materials` - array of materials
- `searchText` - search keywords
- `contentStatus` - workflow status for content (see Status Workflow below)
- `mediaStatus` - workflow status for images/media (see Status Workflow below)

**Optional fields:**
- `photographer` - in image objects
- Exhibition details (if exhibitions exist): `title`, `venue`, `year`, `city`

### 4.5. STATUS WORKFLOW

Two separate status fields track content and media preparation independently:

#### Content Status (`contentStatus`):
- **`"draft"`** - Content needs to be written or enhanced
- **`"needs review"`** - Content is complete and ready for review/approval

#### Media Status (`mediaStatus`):
- **`"images draft"`** - Images need to be processed, selected, or organized
- **`"images review"`** - Images are ready for review/approval
- **`"images done"`** - Images are finalized and approved

**Check current status:**
```bash
python check_status.py
```

This shows:
- Count of works at each status level
- List of works needing attention
- Both content and media status for each work
```

### 5. WORK ID NAMING CONVENTION
- **Format**: `title_year` in lowercase
- **Replace spaces** with underscores
- **Remove special characters** (áéíóú becomes aeiou)
- **Examples**:
  - "Helicopter Landing" (1976) → `helicopter_landing_1976`
  - "Þyrlulending" (1976) → `thyrlulending_1976`

### 6. BATCH PROCESSING APPROACH

#### Recommended Order:
1. **Process 5-10 works** as test batch
2. **Review and refine** workflow
3. **Process chronologically** (earliest works first)
4. **Focus on significant works** first (Venice Biennale, major exhibitions)

#### Efficiency Tips:
- **Batch similar tasks** (all image processing, then all JSON entry)
- **Use templates** and copy/paste structure
- **Keep notes** on special requirements per work
- **Test regularly** on localhost before publishing

### 7. QUALITY CONTROL

#### Before Adding Each Work:
- ✅ Images load properly on localhost
- ✅ Videos play in browser
- ✅ No broken file paths
- ✅ Descriptive captions and metadata
- ✅ Proper JSON syntax (no trailing commas)

#### Testing Checklist:
- Desktop browser display
- Mobile responsiveness
- Search functionality includes new work
- Filter system works with new tags

### 8. PUBLICATION WORKFLOW

#### Git Process:
1. **Test locally** at localhost:8000
2. **Add images** to git: `git add images/new-work-folder/`
3. **Force add videos** if needed: `git add -f path/to/video.mp4`
4. **Update works.json** with new entries
5. **Commit changes**: `git commit -m "Add [Work Title] (Year)"`
6. **Push to GitHub**: `git push origin main`
7. **Verify live site** at magnuspalsson.is

### 9. COMMUNICATION

#### Progress Reporting:
- **Weekly updates** on works completed
- **Flag any issues** with source materials
- **Request clarification** on unclear content
- **Share preview links** for review

#### Questions to Ask:
- Which works are highest priority?
- Should incomplete works be added with "coming soon" placeholder?
- How to handle works with missing information?
- Preferred approach for works with many images?

## Tools & Resources

### Essential Tools:
- **Code editor**: VS Code, Sublime Text
- **Image processing**: Photoshop, GIMP, or online tools
- **Video processing**: HandBrake, FFmpeg
- **Git client**: GitHub Desktop or command line
- **Local server**: Python `http.server` or similar

### Reference Files:
- `works.json` - Current structure and examples
- `style.css` - Visual styling reference
- `works.js` - How works are displayed
- Existing `images/` folders for structure examples

## Getting Started

1. **Set up local environment** (git, local server)
2. **Process 1-2 test works** to understand workflow
3. **Get feedback** on quality and approach
4. **Scale up** to batch processing
5. **Maintain regular communication** throughout

---

**Contact**: Check with Veiga for any questions or clarifications during the process.