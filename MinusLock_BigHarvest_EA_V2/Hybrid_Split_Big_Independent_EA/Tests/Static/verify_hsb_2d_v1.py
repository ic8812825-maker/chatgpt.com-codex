#!/usr/bin/env python3
"""Compatibility entry point; canonical implementation is R1."""
import runpy
runpy.run_path(__file__.replace('verify_hsb_2d_v1.py','verify_hsb_2d_v1_r1.py'),run_name='__main__')
