"""
Project lifecycle scripts defined in pyproject.toml
"""
import subprocess

def tests():
    """
    Run all unittests. Equivalent to:
    `poetry run coverage run --omit */site-packages/*,tests/* -m pytest tests/`
    """
    subprocess.run(
        ['coverage', 'run', '--omit', '*/site-packages/*,tests/*', '-m', 'pytest', 'tests/']
    )

