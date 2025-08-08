# ⚠️ Integration Notice

## 🔄 Scripts Integration Completed

The functionality from this `scripts/` directory has been **fully integrated** into the main DocxMD Converter package.

### ✅ What was integrated:

- **Document Processing**: All processing logic moved to `docxmd_converter/processor.py`
- **Reporting System**: Report generation moved to `docxmd_converter/reporting.py`
- **CLI Integration**: New parameters added to main CLI interface
- **GUI Integration**: Post-processing controls added to GUI
- **API Integration**: Extended Python API with post-processing methods

### 📦 How to use the integrated features:

#### Command Line
```bash
# Use the main package CLI with post-processing
docxmd --src ./docs --dst ./md --direction docx2md --post-process --processor advanced
```

#### Python API
```python
from docxmd_converter import DocxMdConverter

converter = DocxMdConverter()
converter.convert_directory(
    src_dir="./docs",
    dst_dir="./md",
    direction="docx2md",
    post_process=True,
    processor_type="advanced"
)
```

#### GUI
Launch the GUI with integrated post-processing controls:
```bash
docxmd-gui
```

### 📋 Legacy Scripts Status

The files in this directory are **preserved for historical purposes** and reference:
- `document_processor.py` → Integrated into `processor.py`
- `advanced_document_processor.py` → Integrated into `processor.py`
- Supporting documentation → Available in main package docs

### 🚀 Recommended Usage

**Use the main package** instead of these scripts:
- ✅ **Integrated solution**: `docxmd --post-process`
- ❌ **Legacy scripts**: `python scripts/document_processor.py`

### 📚 Documentation

For complete documentation on post-processing features, see:
- Main README.md
- POST_PROCESSING_INTEGRATION.md
- Built-in help: `docxmd --help`

---

*Integration completed successfully. All functionality now available through the main DocxMD Converter package.*