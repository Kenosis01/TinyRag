"""
Minimal code parser for extracting functions from various programming languages
"""

import re
import os
from typing import List, Dict, Tuple
from pathlib import Path


class CodeParser:
    """Minimal code parser supporting multiple languages"""
    
    # Language patterns for function extraction
    PATTERNS = {
        'python': [
            r'(?:^|\n)((?:async\s+)?def\s+\w+\([^)]*\):[^\n]*(?:\n(?:    |\t)[^\n]*)*)',
            r'(?:^|\n)(class\s+\w+[^:]*:[^\n]*(?:\n(?:    |\t)[^\n]*)*)'
        ],
        'javascript': [
            r'(?:^|\n)((?:async\s+)?function\s+\w+\([^)]*\)\s*\{[^}]*\})',
            r'(?:^|\n)((?:const|let|var)\s+\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\})',
            r'(?:^|\n)(class\s+\w+[^{]*\{[^}]*\})'
        ],
        'java': [
            r'(?:^|\n)(\s*(?:public|private|protected)?\s*(?:static)?\s*\w+\s+\w+\([^)]*\)\s*\{[^}]*\})',
            r'(?:^|\n)((?:public|private|protected)?\s*class\s+\w+[^{]*\{[^}]*\})'
        ],
        'cpp': [
            r'(?:^|\n)(\w+\s+\w+\([^)]*\)\s*\{[^}]*\})',
            r'(?:^|\n)(class\s+\w+[^{]*\{[^}]*\})'
        ],
        'c': [
            r'(?:^|\n)(\w+\s+\w+\([^)]*\)\s*\{[^}]*\})'
        ],
        'go': [
            r'(?:^|\n)(func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\([^)]*\)[^{]*\{[^}]*\})',
            r'(?:^|\n)(type\s+\w+\s+struct\s*\{[^}]*\})'
        ],
        'rust': [
            r'(?:^|\n)((?:pub\s+)?fn\s+\w+[^{]*\{[^}]*\})',
            r'(?:^|\n)((?:pub\s+)?struct\s+\w+[^{]*\{[^}]*\})'
        ],
        'php': [
            r'(?:^|\n)((?:public|private|protected)?\s*function\s+\w+\([^)]*\)[^{]*\{[^}]*\})',
            r'(?:^|\n)(class\s+\w+[^{]*\{[^}]*\})'
        ]
    }
    
    # File extensions mapping
    EXTENSIONS = {
        '.py': 'python', '.js': 'javascript', '.ts': 'javascript',
        '.java': 'java', '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp',
        '.c': 'c', '.h': 'c', '.go': 'go', '.rs': 'rust', '.php': 'php'
    }
    
    @classmethod
    def detect_language(cls, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        return cls.EXTENSIONS.get(ext, 'unknown')
    
    @classmethod
    def extract_functions(cls, code: str, language: str) -> List[Dict[str, str]]:
        """Extract functions from code"""
        if language not in cls.PATTERNS:
            return [{'type': 'code', 'name': 'unknown', 'content': code[:500]}]
        
        functions = []
        patterns = cls.PATTERNS[language]
        
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.MULTILINE | re.DOTALL)
            for match in matches:
                func_code = match.group(1).strip()
                if len(func_code) > 10:  # Skip very short matches
                    # Extract function name
                    name_match = re.search(r'(?:def|function|class|func|fn|type)\s+(\w+)', func_code)
                    name = name_match.group(1) if name_match else 'anonymous'
                    
                    # Determine type
                    func_type = 'class' if any(kw in func_code[:20] for kw in ['class', 'struct', 'type']) else 'function'
                    
                    functions.append({
                        'type': func_type,
                        'name': name,
                        'content': func_code,
                        'language': language
                    })
        
        # If no functions found, return the whole code as a chunk
        if not functions:
            functions.append({
                'type': 'code',
                'name': 'main',
                'content': code[:1000],  # Limit size
                'language': language
            })
        
        return functions
    
    @classmethod
    def parse_file(cls, file_path: str) -> List[Dict[str, str]]:
        """Parse a code file and extract functions"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            language = cls.detect_language(file_path)
            functions = cls.extract_functions(code, language)
            
            # Add file info to each function
            for func in functions:
                func['file'] = file_path
                func['full_name'] = f"{Path(file_path).name}::{func['name']}"
            
            return functions
        except Exception as e:
            return [{
                'type': 'error',
                'name': 'parse_error',
                'content': f"Error parsing {file_path}: {str(e)}",
                'file': file_path,
                'language': 'unknown'
            }]
    
    @classmethod
    def is_code_file(cls, file_path: str) -> bool:
        """Check if file is a supported code file"""
        ext = Path(file_path).suffix.lower()
        return ext in cls.EXTENSIONS
    
    @classmethod
    def scan_directory(cls, directory: str, recursive: bool = True) -> List[str]:
        """Scan directory for code files"""
        code_files = []
        path = Path(directory)
        
        if not path.exists():
            return []
        
        pattern = "**/*" if recursive else "*"
        for file_path in path.glob(pattern):
            if file_path.is_file() and cls.is_code_file(str(file_path)):
                # Skip common non-source directories
                if not any(skip in str(file_path) for skip in [
                    'node_modules', '.git', '__pycache__', '.venv', 'venv',
                    'build', 'dist', '.pytest_cache', 'target'
                ]):
                    code_files.append(str(file_path))
        
        return code_files