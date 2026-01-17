#!/usr/bin/env python3
"""
Test runner per eseguire tutti i test unitari.
"""

import pytest
import sys
import os

# Aggiungi il percorso del progetto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Esegui tutti i test unitari"""
    
    # Argomenti per pytest
    test_args = [
        'tests/',
        '-v',
        '--tb=short',
        '--color=yes',
        '--cov=src',
        '--cov-report=term-missing',
        '--cov-report=html'
    ]
    
    # Aggiungi argomenti personalizzati se forniti
    if len(sys.argv) > 1:
        test_args.extend(sys.argv[1:])
    
    print("🧪 Esecuzione test unitari...")
    print("=" * 50)
    
    # Esegui pytest
    exit_code = pytest.main(test_args)
    
    print("=" * 50)
    if exit_code == 0:
        print("✅ Tutti i test sono passati!")
    else:
        print("❌ Alcuni test sono falliti!")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(run_tests())