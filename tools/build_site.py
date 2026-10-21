"""Build all generated static pages and hosting metadata."""
from pathlib import Path
import runpy

TOOLS = Path(__file__).resolve().parent
for script in ('make_index.py', 'make_projects.py', 'make_pages.py', 'make_metadata.py'):
    runpy.run_path(str(TOOLS / script), run_name='__main__')
