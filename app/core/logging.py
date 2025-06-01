import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger("uvicorn").setLevel(logging.INFO)

logger = logging.getLogger("app")

setup_logging()
