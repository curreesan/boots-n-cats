import logging


def configure_logging() -> None:
    """
    Called once at startup (see main.py). Configures the root logger for
    the whole app — anywhere else in the codebase can call
    `logging.getLogger(__name__)` and get sensible output without
    configuring anything itself.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
