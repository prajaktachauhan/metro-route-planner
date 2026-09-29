"""Entry point:  python main.py"""

import logging
import sys

from metro_planner.logger_setup import setup_logging
from metro_planner.planner import run_cli

logger = logging.getLogger("main")


def main():
    setup_logging()
    try:
        run_cli()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting Metro Route Planner. Goodbye!")
        return 0
    except Exception:  # last-resort guard so users never see a raw traceback
        logger.exception("Unexpected error")
        print("\nSomething went wrong. Details were saved to logs/metro_planner.log")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
