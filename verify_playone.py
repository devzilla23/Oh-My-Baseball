import subprocess, sys
subprocess.run([sys.executable, '-m', 'pytest', '-q', 'tests/test_playone.py'], check=True)
