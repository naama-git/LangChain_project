import sys
import asyncio
import subprocess
from app import demo

def run_cli():
    from agent import query_loop
    asyncio.run(query_loop())


def run_ui():
    demo.launch()

if __name__ == "__main__":
    if "cli" in [arg.lower() for arg in sys.argv[1:]]:
        run_cli()

    else:
        run_ui()

