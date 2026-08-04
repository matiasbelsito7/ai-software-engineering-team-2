"""
Document loaders.
"""

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.loaders.git import GitLoader
from ai_team.rag.loaders.markdown import MarkdownLoader
from ai_team.rag.loaders.pdf import PDFLoader
from ai_team.rag.loaders.python import PythonLoader
from ai_team.rag.loaders.repository import RepositoryLoader
from ai_team.rag.loaders.text import TextLoader

__all__ = [
    "BaseDocumentLoader",
    "MarkdownLoader",
    "PDFLoader",
    "TextLoader",
    "PythonLoader",
    "GitLoader",
    "RepositoryLoader",
]