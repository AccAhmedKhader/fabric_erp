#!/usr/bin/env python
"""
Allow running the repository validator directly from the tools package.

Usage:
    python -m tools
"""

from .repository_validator import main

if __name__ == '__main__':
    main()