#!/usr/bin/env python3
"""
CoTrip backend startup script - Simple version
"""

import sys
import os
import subprocess

def main():
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)

    # Install dependencies if needed
    if not os.path.exists('venv'):
        print('Installing dependencies...')
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'fastapi', 'uvicorn', 'sqlalchemy', 'passlib', 'python-multipart'])

    # Start server
    print('Starting CoTrip backend server on port 8080...')
    print('API will be available at: http://localhost:8080')
    print('API docs will be available at: http://localhost:8080/docs')
    print('Press Ctrl+C to stop the server')

    subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8080'])

if __name__ == '__main__':
    main()
