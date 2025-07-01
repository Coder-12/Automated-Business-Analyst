import logging

def setup_logger():
    # Clear old log first
    with open("business_analyst_app.log", "w"):
        pass

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename='business_analyst_app.log',  # or stream=sys.stdout
        filemode='a'
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging started fresh.")
