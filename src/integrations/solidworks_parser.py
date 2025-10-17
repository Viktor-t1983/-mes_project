import json
import os
from typing import Dict, List

class SolidWorksParser:
    """Парсинг BOM из SolidWorks (ожидается JSON-файл)"""
    
    @staticmethod
    def parse_bom_file(file_path: str) -> Dict:
        """
        Ожидаемый формат файла от SolidWorks:
        {
          "part_number": "ASM-001",
          "components": [
            {"part": "PART-001", "qty": 2, "material": "Steel"},
            {"part": "PART-002", "qty": 1, "material": "Aluminum"}
          ]
        }
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"BOM file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Валидация
            if "part_number" not in data or "components" not in data:
                raise ValueError("Invalid BOM structure")
            
            return data
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in BOM file")
        except Exception as e:
            raise ValueError(f"BOM parsing failed: {str(e)}")
