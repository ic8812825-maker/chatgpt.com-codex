#!/usr/bin/env python3
"""Current-stage entry point for the accepted immutable R7 compatibility gate."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('verify_hsb_2d_v1_r7_current_compat.py')),run_name='__main__')
