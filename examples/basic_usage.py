#!/usr/bin/env python3
"""
Basic usage examples for DocxMD Converter.

This script demonstrates how to use the DocxMdConverter class
programmatically for various conversion tasks.
"""

from pathlib import Path

# Import the converter (assuming package is installed)
try:
    from docxmd_converter import DocxMdConverter
except ImportError:
    # If running from source directory
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from docxmd_converter import DocxMdConverter


def example_single_file_conversion():
    """Example: Convert a single file."""
    print("=== Single File Conversion Example ===")

    # Initialize converter
    converter = DocxMdConverter(log_level="INFO")

    # Example paths (adjust these to your actual files)
    input_file = "example_document.docx"
    output_file = "example_document.md"

    # Convert .docx to .md
    success = converter.convert_file(
        input_file=input_file, output_file=output_file, direction="docx2md"
    )

    if success:
        print(f"✅ Successfully converted {input_file} to {output_file}")
    else:
        print(f"❌ Failed to convert {input_file}")


def example_directory_conversion():
    """Example: Convert entire directory."""
    print("\n=== Directory Conversion Example ===")

    # Initialize converter
    converter = DocxMdConverter(log_level="INFO")

    # Example directory paths
    src_directory = "./documents"  # Directory with .docx files
    dst_directory = "./markdown"  # Output directory for .md files

    # Convert all .docx files to .md
    try:
        successful, total = converter.convert_directory(
            src_dir=src_directory, dst_dir=dst_directory, direction="docx2md"
        )

        print(f"✅ Converted {successful}/{total} files")

    except Exception as e:
        print(f"❌ Directory conversion failed: {e}")


def example_template_conversion():
    """Example: Convert with template."""
    print("\n=== Template Conversion Example ===")

    # Initialize converter
    converter = DocxMdConverter(log_level="INFO")

    # Example paths
    src_directory = "./markdown"  # Directory with .md files
    dst_directory = "./documents"  # Output directory for .docx files
    template_file = "./template.docx"  # Template file

    # First, validate the template
    if Path(template_file).exists():
        is_valid = converter.validate_template(template_file)

        if is_valid:
            print(f"✅ Template is valid: {template_file}")

            # Convert .md to .docx using template
            try:
                successful, total = converter.convert_directory(
                    src_dir=src_directory,
                    dst_dir=dst_directory,
                    direction="md2docx",
                    template_path=template_file,
                )

                print(f"✅ Converted {successful}/{total} files using template")

            except Exception as e:
                print(f"❌ Template conversion failed: {e}")
        else:
            print(f"❌ Invalid template: {template_file}")
    else:
        print(f"❌ Template file not found: {template_file}")


def example_create_sample_files():
    """Create sample files for testing."""
    print("\n=== Creating Sample Files ===")

    # Create directories
    Path("./documents").mkdir(exist_ok=True)
    Path("./markdown").mkdir(exist_ok=True)

    # Create a sample markdown file
    sample_md = Path("./markdown/sample.md")
    sample_md.write_text(
        """
# Sample Document

This is a **sample** document for testing the DocxMD Converter.

## Features

- Convert between .docx and .md formats
- Support for templates
- Recursive directory processing
- Both CLI and GUI interfaces

### Code Example

```python
from docxmd_converter import DocxMdConverter

converter = DocxMdConverter()
converter.convert_file("input.docx", "output.md", "docx2md")
```

### Table Example

| Feature | Supported |
|---------|-----------|
| .docx → .md | ✅ |
| .md → .docx | ✅ |
| Templates | ✅ |
| Recursive | ✅ |

> This is a blockquote example.
>
> It can span multiple lines.

---

That's all for this sample document!
"""
    )

    print(f"✅ Created sample file: {sample_md}")

    # Create a simple template instruction
    template_instruction = Path("./template_instructions.txt")
    template_instruction.write_text(
        """
Template Creation Instructions:
==============================

To create a template for .md → .docx conversion:

1. Create a new Word document (.docx)
2. Set up your desired styles:
   - Heading 1, Heading 2, etc.
   - Body text font and spacing
   - List styles
   - Table styles
3. Save the document as your template
4. Use it with: --template your_template.docx

The template's formatting will be applied to converted documents.
"""
    )

    print(f"✅ Created template instructions: {template_instruction}")


def main():
    """Run all examples."""
    print("DocxMD Converter - Usage Examples")
    print("=" * 40)

    try:
        # Check if converter can be initialized
        converter = DocxMdConverter()
        print("✅ DocxMdConverter initialized successfully")
        print(f"✅ Supported directions: {converter.get_supported_directions()}")

        # Create sample files first
        example_create_sample_files()

        # Run examples (commented out as they require actual files)
        print("\n📝 To run conversion examples:")
        print("1. Create some .docx files in ./documents/")
        print("2. Or use the sample .md file created in ./markdown/")
        print("3. Uncomment the example calls below")

        # Uncomment these to run actual conversions:
        # example_single_file_conversion()
        # example_directory_conversion()
        # example_template_conversion()

    except Exception as e:
        print(f"❌ Error initializing converter: {e}")
        print("Make sure pandoc is installed on your system")


if __name__ == "__main__":
    main()
