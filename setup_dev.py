#!/usr/bin/env python3
"""
Development setup script for DocxMD Converter.

This script helps with setting up the development environment
and installing the package in development mode.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"📦 {description}")

    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        if result.stdout.strip():
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Please use Python 3.8 or higher")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_pandoc():
    """Check if Pandoc is installed."""
    try:
        result = subprocess.run(
            ["pandoc", "--version"], capture_output=True, text=True, check=True
        )
        version_line = result.stdout.split("\n")[0]
        print(f"✅ {version_line} detected")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pandoc not found")
        print("   Please install Pandoc from https://pandoc.org/installing.html")
        return False


def setup_virtual_environment():
    """Setup virtual environment if it doesn't exist."""
    venv_path = Path("venv")

    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True

    print("📦 Creating virtual environment...")
    return run_command(f"{sys.executable} -m venv venv", "Creating virtual environment")


def install_package():
    """Install package in development mode."""
    # Determine pip command based on OS
    if os.name == "nt":  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"

    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -e .", "Installing package in development mode"),
        (f"{pip_cmd} install -e '.[dev]'", "Installing development dependencies"),
    ]

    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False

    return True


def run_tests():
    """Run the test suite."""
    # Determine python command for venv
    if os.name == "nt":  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"

    return run_command(f"{python_cmd} -m pytest tests/ -v", "Running tests")


def main():
    """Main setup function."""
    print("DocxMD Converter - Development Setup")
    print("=" * 40)

    # Check prerequisites
    if not check_python_version():
        return 1

    if not check_pandoc():
        print("\n⚠️  Warning: Pandoc is required for the converter to work")
        print("   You can continue setup, but install Pandoc before using the package")

    # Setup development environment
    print("\n📋 Setting up development environment...")

    if not setup_virtual_environment():
        print("❌ Failed to setup virtual environment")
        return 1

    if not install_package():
        print("❌ Failed to install package")
        return 1

    # Run tests
    print("\n🧪 Running tests...")
    if run_tests():
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed (this might be due to missing pandoc)")

    # Final instructions
    print("\n🎉 Setup completed!")
    print("\nTo activate the virtual environment:")
    if os.name == "nt":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")

    print("\nTo use the package:")
    print("   docxmd --help")
    print("   docxmd-gui")
    print("   python examples/basic_usage.py")

    print("\nTo run tests:")
    print("   pytest")

    return 0


if __name__ == "__main__":
    sys.exit(main())
