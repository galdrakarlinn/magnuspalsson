#!/bin/bash
cd "/c/Users/VeigaMagnusdottir/projects/magnusPalsson/magnuspalsson/images/studios/"

echo "Processing large studio files..."
find . -maxdepth 1 -type f -size +2M -name "*.jpg" -not -path "./medium/*" -not -path "./thumbs/*" | while read file; do
    filename=$(basename "$file")
    echo "Processing $filename"

    # Create medium version (800x600, ~80KB)
    if [ ! -f "medium/$filename" ]; then
        ffmpeg -i "$file" -vf "scale=800:600:force_original_aspect_ratio=decrease,pad=800:600:(ow-iw)/2:(oh-ih)/2" -q:v 5 "medium/$filename" -y 2>/dev/null && echo "  Medium created"
    fi

    # Create thumb version (150x150, ~5KB)
    if [ ! -f "thumbs/$filename" ]; then
        ffmpeg -i "$file" -vf "scale=150:150:force_original_aspect_ratio=decrease,pad=150:150:(ow-iw)/2:(oh-ih)/2" -q:v 7 "thumbs/$filename" -y 2>/dev/null && echo "  Thumb created"
    fi
done

echo "Studio optimization complete!"