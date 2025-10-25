"""
WEB INTERFACE MODULE
====================
Wrapper for the HTML interface
"""

import os

# Load HTML interface from file
interface_path = os.path.join(os.path.dirname(__file__), 'interface.html')

try:
    with open(interface_path, 'r') as f:
        HTML_INTERFACE = f.read()
except:
    # Fallback HTML if file not found
    HTML_INTERFACE = '''<!DOCTYPE html>
    <html><head><title>Glyphwheel V22</title></head>
    <body><h1>Glyphwheel V22 - Interface Error</h1>
    <p>Could not load interface.html</p></body></html>'''

__all__ = ['HTML_INTERFACE']
