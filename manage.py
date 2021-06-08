#!/usr/bin/env python
"""
Django administration utility.
"""

import os
import sys

PWD = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_utils.test_settings')
    sys.path.append(PWD)
