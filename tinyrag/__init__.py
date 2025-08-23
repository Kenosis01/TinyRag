"""
TinyRag - A minimal Retrieval-Augmented Generation library with structured responses and source citations
"""

from .core.provider import Provider
from .core.tinyrag import TinyRag
from .core.structured_response import StructuredResponse, Source, ResponseFormatter

__version__ = "0.2.0"
__all__ = ["Provider", "TinyRag", "StructuredResponse", "Source", "ResponseFormatter"]