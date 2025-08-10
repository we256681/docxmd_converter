#!/usr/bin/env python3
"""
Главный запускатор DocxMD Converter
"""

import sys
from pathlib import Path

# Добавляем путь к scripts для запуска системы
scripts_path = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_path))

from run_system import main

if __name__ == "__main__":
    main()