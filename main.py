"""Entry point: draw the 20 November 2026 front page.

Runs draw.py, which writes entry.png into $MAKEFUN_OUTPUT_DIR
(or ./out when the variable is unset).
"""

import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    runpy.run_path(os.path.join(HERE, "draw.py"), run_name="__main__")
