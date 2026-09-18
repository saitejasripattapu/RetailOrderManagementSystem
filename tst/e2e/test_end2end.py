"""End-to-end tests launch main.py rather than importing application functions."""

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

