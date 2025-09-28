# Image Processing Guide for Magnús Pálsson Archive

## Image Requirements

### File Specifications
- **Format**: JPG (JPEG)
- **Quality**: 80-85% (balance between quality and file size)
- **Width**: Maximum 1200px (maintain aspect ratio)
- **File size**: Target 200KB-800KB per image
- **Color space**: sRGB
- **Naming**: descriptive, no spaces, use hyphens

### Folder Structure
```
magnuspalsson/images/
├── work-title-year/
│   ├── work-title-01.jpg
│   ├── work-title-02.jpg
│   ├── work-title-03.jpg
│   └── work-title-video.mp4
```

## Processing Workflow

### 1. Image Selection
From each Dropbox folder:
- **Choose 3-8 best images** (not all available)
- **Prioritize**:
  - Overall view of the work
  - Detail shots showing materials/technique
  - Installation/exhibition context
  - Process documentation (if performance/conceptual work)
- **Avoid**:
  - Blurry or poorly lit images
  - Redundant similar angles
  - Images with distracting backgrounds

### 2. Batch Processing Tools

#### Option A: Photoshop (Recommended)
```
File → Scripts → Image Processor
- Set quality to 8-9 (80-90%)
- Resize to fit: Width 1200px
- Include ICC Profile
- Convert to sRGB
```

#### Option B: GIMP (Free Alternative)
```
File → Export As → JPEG
- Quality: 80-85
- Image → Scale Image → Width: 1200px
- Colors → Auto → Color Enhance
```

#### Option C: Online Tools
- **Squoosh.app**: Google's image optimizer
- **TinyPNG**: Compression tool
- **Bulk Resize Photos**: Online batch processor

### 3. File Naming Convention

#### Format: `workname-##.jpg`
- Use work ID format (lowercase, hyphens instead of spaces)
- Number sequentially: 01, 02, 03, etc.
- Examples:
  ```
  helicopter-landing-1976-01.jpg
  helicopter-landing-1976-02.jpg
  yxn-2002-01.jpg
  yxn-2002-video.mp4
  ```

#### Special File Types:
- **Main image**: `workname-01.jpg`
- **Details**: `workname-02.jpg`, `workname-03.jpg`
- **Videos**: `workname-video.mp4` or `workname-preview.mp4`
- **Audio**: `workname-audio.mp3`
- **PDFs**: `workname-catalog.pdf`

### 4. Image Quality Checklist

Before finalizing each image:
- ✅ **Sharpness**: Image is crisp and clear
- ✅ **Exposure**: Good contrast, not too dark/bright
- ✅ **Color**: Accurate representation of artwork
- ✅ **Composition**: Work is well-framed
- ✅ **File size**: Under 1MB, ideally 200-800KB
- ✅ **Dimensions**: Max 1200px width

### 5. Folder Organization

#### Create New Work Folder:
1. Navigate to `magnuspalsson/images/`
2. Create folder with work ID: `work-title-year`
3. Copy processed images into folder
4. Verify file paths match JSON entries

#### Example Structure:
```
images/
├── helicopter-landing-1976/
│   ├── helicopter-landing-1976-01.jpg
│   ├── helicopter-landing-1976-02.jpg
│   └── helicopter-landing-1976-03.jpg
├── yxn-2002/
│   ├── yxn-2002-preview.mp4
│   ├── yxn-2002-audio.mp3
│   └── yxn-2002-catalog.pdf
```

## Specific Image Types

### Performance Documentation
- **Before/during/after** shots
- **Audience context** if relevant
- **Artist in action** (if available)
- **Documentation quality** over artistic beauty

### Sculpture Works
- **Overall view** from main angle
- **Detail shots** showing materials/technique
- **Scale reference** (person/object for size)
- **Installation context** in gallery/museum

### Installation Works
- **Wide shot** showing entire space
- **Detail views** of components
- **Visitor interaction** (if applicable)
- **Multiple angles** to show spatial relationships

### Conceptual/Text Works
- **Readable text** (high resolution for legibility)
- **Context shots** showing installation
- **Detail of materials** (paper, typeface, etc.)
- **Documentation** of process if available

## Quality Control

### Final Check Before Adding to Git:
1. **File paths match JSON**: Verify exact file names
2. **Images load locally**: Test at localhost:8000
3. **Mobile display**: Check responsive scaling
4. **Copyright info**: Ensure proper attribution
5. **File sizes reasonable**: Total folder under 5MB if possible

### Common Issues to Avoid:
- ❌ **File paths with spaces**: Use hyphens instead
- ❌ **Oversized files**: Keep under 1MB each
- ❌ **Poor image quality**: Don't over-compress
- ❌ **Inconsistent naming**: Follow the convention
- ❌ **Missing images**: Verify all files copied

## Tools and Resources

### Image Processing Software:
- **Adobe Photoshop**: Professional standard
- **GIMP**: Free alternative
- **Canva**: Online editor
- **Preview (Mac)**: Basic resize/export
- **Paint.NET (Windows)**: Free editor

### Batch Processing Tools:
- **ImageOptim (Mac)**: Lossless compression
- **RIOT**: Radical Image Optimization Tool
- **XnConvert**: Cross-platform batch converter
- **FastStone Image Viewer**: Windows batch tools

### Online Compression:
- **Squoosh.app**: Advanced compression options
- **TinyPNG/TinyJPG**: Smart lossy compression
- **Compressor.io**: Lossless and lossy options
- **Kraken.io**: API-based optimization

## Getting Started

1. **Download 2-3 test works** from Dropbox
2. **Process images** following this guide
3. **Test locally** to verify quality
4. **Get feedback** before processing large batches
5. **Refine workflow** based on results

Remember: Quality over quantity - better to have fewer high-quality images than many poor ones.