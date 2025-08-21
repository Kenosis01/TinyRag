"""
TinyRag - A minimal Retrieval-Augmented Generation library
"""

from .core.provider import Provider
from .core.tinyrag import TinyRag

__version__ = "0.1.0"
__all__ = ["Provider", "TinyRag"]