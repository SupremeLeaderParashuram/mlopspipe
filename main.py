#!/usr/bin/env python3
"""
ML Pipeline — launch the GUI.
Usage: python main.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gui.app import main
if __name__ == "__main__":
    main()
