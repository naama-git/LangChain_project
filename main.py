import sys
import asyncio
from app import demo
from cli import query_loop

def run_cli():
    asyncio.run(query_loop())


def run_ui():
    demo.launch()

if __name__ == "__main__":
    if "cli" in [arg.lower() for arg in sys.argv[1:]]:
        run_cli()

    else:
        run_ui()

