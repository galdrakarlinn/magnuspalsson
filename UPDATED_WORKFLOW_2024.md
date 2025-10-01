# Updated Workflow for Adding New Works (2024)

## Current Status & Structure

**✅ Completed:** Repository optimized with ~60 works using the new structure
**✅ Current Structure:** All works use `medium/` and `thumbs/` folders only
**🎯 Goal:** Add remaining works from images-not-used and new Dropbox content

## Current Optimized Folder Structure

```
images/work-id/
├── medium/
│   ├── work-name-01-medium.jpg  (max 800x600, ~100-300KB)
│   ├── work-name-02-medium.jpg
│   └── work-name-03-medium.jpg
├── thumbs/
│   ├── work-name-01-thumb.jpg   (150x150 square, ~5-10KB)
│   ├── work-name-02-thumb.jpg
│   └── work-name-03-thumb.jpg
└── [optional files: audio.mp3, video.mp4, catalog.pdf]
```

## Updated Workflow Steps

### 1. SOURCE ANALYSIS
- **Check images-not-used folder first** for existing archived works
- **Dropbox folders** for new works
- **Identify**: title, year, best images (3-8 max)
- **Note**: materials, exhibitions, description sources

### 2. IMAGE PROCESSING (Automated)

#### Create Processing Script:
```python
# Use FFmpeg for consistent optimization:
# Medium: max 800x600, maintaining aspect ratio
ffmpeg -i input.jpg -vf "scale=800:600:force_original_aspect_ratio=decrease" -q:v 3 medium.jpg

# Thumbnail: 150x150 square, cropped
ffmpeg -i input.jpg -vf "scale=150:150:force_original_aspect_ratio=increase,crop=150:150" -q:v 4 thumb.jpg
```

#### Naming Convention:
- **Medium**: `work-name-##-medium.jpg`
- **Thumbnail**: `work-name-##-thumb.jpg`
- **Sequential numbering**: 01, 02, 03, etc.

### 3. FOLDER CREATION

#### Work ID Format:
- **Pattern**: `descriptive-name-year` (all lowercase, hyphens)
- **Examples**:
  - "New Installation" (2023) → `new-installation-2023`
  - "Þyrlulending" (1976) → `thyrlulending-1976`

#### Automated Folder Setup:
```bash
# Create folder structure
mkdir -p images/work-id/{medium,thumbs}

# Process and place images
process_images.py --input dropbox/folder --output images/work-id
```

### 4. JSON ENTRY (Required Properties)

```json
{
  "id": "work_id_format",
  "title": "Actual Work Title",
  "year": 2023,
  "description": "Comprehensive description with context, materials, significance",
  "images": [
    {
      "url": "images/work-id/medium/work-name-01-medium.jpg",
      "caption": "Descriptive caption"
    }
  ],
  "tags": ["medium", "theme", "decade"],
  "exhibitions": [
    {
      "title": "Exhibition Name",
      "venue": "Venue Name",
      "year": 2023,
      "city": "City"
    }
  ],
  "materials": ["material1", "material2"],
  "searchText": "searchable keywords and phrases"
}
```

**⚠️ CRITICAL:** All works MUST have `exhibitions` and `materials` arrays (even if empty) to prevent JavaScript errors.

### 5. QUALITY CONTROL CHECKLIST

#### Before Adding:
- ✅ **Folder structure**: medium/ and thumbs/ folders present
- ✅ **Image optimization**: Medium ~100-300KB, thumbs ~5-10KB
- ✅ **Naming consistency**: Follows convention exactly
- ✅ **JSON validation**: All required properties present
- ✅ **Local testing**: localhost:8000 displays correctly
- ✅ **Mobile check**: Responsive display works

#### File Size Targets:
- **Medium images**: 800x600 max, 100-300KB each
- **Thumbnails**: 150x150 exact, 5-10KB each
- **Total per work**: Under 2MB for all files

### 6. DEPLOYMENT PROCESS

#### Git Workflow:
```bash
# 1. Add new work folder
git add images/new-work-folder/

# 2. Update JSON
git add works.json

# 3. Commit with clear message
git commit -m "Add [Work Title] (Year) - brief description"

# 4. Push to production
git push origin main

# 5. Verify live site (GitHub Pages deploys automatically)
```

## Automated Tools Needed

### 1. Image Processing Script
```python
def process_work_images(source_folder, work_id):
    """
    Process all images for a work:
    1. Select best 3-8 images
    2. Create medium/ and thumbs/ folders
    3. Generate optimized versions
    4. Apply consistent naming
    """
```

### 2. JSON Template Generator
```python
def create_work_json(work_id, title, year, images):
    """
    Generate JSON entry with:
    1. All required properties
    2. Image array from processed files
    3. Empty exhibitions/materials arrays
    4. Basic searchText from title/year
    """
```

### 3. Validation Script
```python
def validate_work(work_id):
    """
    Check:
    1. Folder structure exists
    2. Images properly optimized
    3. JSON syntax valid
    4. All required properties present
    """
```

## Priority Works to Add

### Phase 1: From images-not-used
- **Advantage**: Images already exist, just need optimization
- **Process**: Copy → optimize → add JSON
- **Estimate**: ~20-30 works available

### Phase 2: High-Priority New Works
- **Venice Biennale works** (1980, 1984)
- **Major exhibitions** (SÚM, major museums)
- **Significant collaborations** (Dieter Roth, etc.)
- **Chronologically important** (early works 1960s-1970s)

### Phase 3: Complete Archive
- **Remaining Dropbox content**
- **Recent works** (2000s-2020s)
- **Documentation projects**

## Efficiency Improvements

### Batch Processing:
1. **Group similar works** by decade/medium
2. **Process images in batches** using scripts
3. **Template JSON entries** for similar works
4. **Test batches of 5-10 works** before large commits

### Quality Shortcuts:
- **Use existing optimized images** when available
- **Focus on best 3-5 images** per work (not exhaustive)
- **Leverage AI for initial descriptions** (then refine)
- **Copy exhibition/material data** from similar works

## Next Steps

1. **Create automation scripts** for image processing
2. **Process 5 test works** from images-not-used
3. **Refine workflow** based on results
4. **Scale up** to batch processing
5. **Maintain momentum** with regular additions

The goal is to make adding new works as streamlined as possible while maintaining the high quality and consistent structure you've established.