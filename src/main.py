from libs.logger import logger

def initialize_application():
    try:
        logger.info("Initializing application...")
        # Initialization logic goes here
        logger.info("Application initialized successfully.")
    except Exception as e:
        logger.error(f"An error occurred during initialization: {e}")


def start_application():
    try:
        initialize_application()
        logger.info("Application started successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    start_application()