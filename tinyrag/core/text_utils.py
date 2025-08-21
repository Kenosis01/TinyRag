"""
Text extraction and chunking utilities
"""

import os
from typing import List, Union
from pathlib import Path


def extract_text(data: Union[str, Path]) -> str:
    """Extract text from file path or return raw string"""
    if isinstance(data, (str, Path)) and os.path.isfile(data):
        file_path = Path(data)
        extension = file_path.suffix.lower()
        
        if extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif extension == '.pdf':
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                raise ImportError("PyPDF2 required for PDF support. Install with: pip install PyPDF2")
        
        elif extension == '.docx':
            try:
                from docx import Document
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                raise ImportError("python-docx required for DOCX support. Install with: pip install python-docx")
        
        else:
            # Try to read as plain text for other formats
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
    
    # Return as raw string if not a file path
    return str(data)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence or word boundary
        if end < len(text):
            # Look for sentence boundary
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start:
                end = sentence_end + 1
            else:
                # Look for word boundary
                word_end = text.rfind(' ', start, end)
                if word_end > start:
                    end = word_end
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks