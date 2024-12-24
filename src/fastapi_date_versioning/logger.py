import sys
import logging


def _create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a StreamHandler to output to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


logger = _create_logger()
