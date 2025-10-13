# Data Directory

This directory contains the PDF file that the chatbot uses to answer questions.

## Required File

Place your geospatial PDF here with the name:
```
geospatial_book.pdf
```

Full path should be:
```
data/geospatial_book.pdf
```

## Instructions

### Windows (PowerShell):
```powershell
Copy-Item "C:\path\to\your\pdf.pdf" -Destination "data\geospatial_book.pdf"
```

### Linux/Mac:
```bash
cp /path/to/your/pdf.pdf data/geospatial_book.pdf
```

## PDF Requirements

- **Format**: PDF (.pdf)
- **Size**: Up to 100 MB recommended
- **Content**: Text-based (not scanned images)
- **Language**: English (for best results)
- **Pages**: Any number

## Supported Content Types

✅ Text-based PDFs
✅ PDFs with embedded text
✅ Academic papers
✅ Technical documentation
✅ Books
✅ Reports

❌ Scanned images (without OCR)
❌ Password-protected PDFs
❌ Corrupted PDFs

## Custom PDF Name

If you want to use a different filename, edit `app.py`:

```python
PDF_PATH = "data/your_custom_name.pdf"
```

## Multiple PDFs

To use multiple PDFs, you can:

1. **Merge them first** using a PDF tool
2. **Modify the code** to load multiple files
3. **Run multiple instances** with different PDFs

## Security Note

This directory is in `.gitignore` to prevent committing large PDF files or sensitive documents to version control.

Only `.gitkeep` is tracked by git to preserve the folder structure.
