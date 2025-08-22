from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tinyrag",
    version="0.3.0",
    author="TinyRag Team",
    author_email="transformtrails@gmail.com",
    description="A minimal Python library for Retrieval-Augmented Generation with codebase indexing and multiple vector store backends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kenosis01/TinyRag",
    project_urls={
        "Bug Tracker": "https://github.com/Kenosis01/TinyRag/issues",
        "Documentation": "https://github.com/Kenosis01/TinyRag#readme",
        "Source Code": "https://github.com/Kenosis01/TinyRag",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sentence-transformers",
        "requests",
        "numpy",
        "faiss-cpu",
        "scikit-learn",
        "chromadb",
        "PyPDF2",
        "python-docx",
    ],
    extras_require={
        "faiss": ["faiss-cpu>=1.7.0"],
        "chroma": ["chromadb>=0.4.0"],
        "pickle": ["scikit-learn>=1.0.0"],
        "docs": ["PyPDF2>=3.0.0", "python-docx>=0.8.11"],
        "all": [
            "faiss-cpu>=1.7.0",
            "chromadb>=0.4.0", 
            "scikit-learn>=1.0.0",
            "PyPDF2>=3.0.0",
            "python-docx>=0.8.11"
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
            "twine>=3.0",
            "build>=0.7"
        ],
    },
    keywords=[
        "rag", "retrieval", "augmented", "generation", "vector", "database", 
        "embeddings", "similarity", "search", "nlp", "ai", "machine-learning",
        "codebase", "code-indexing", "function-search", "code-analysis"
    ],
    include_package_data=True,
    zip_safe=False,
)