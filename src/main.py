from libs.logger import logger

def initialize_database():
    try:
        logger.info("Initializing database...")
        # Database initialization logic goes here
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"An error occurred during database initialization: {e}")

def initialize_application():
    try:
        logger.info('================================================================================================')
        logger.info("Initializing application...")
        initialize_database()
        # Initialization logic goes here
        logger.info("Application initialized successfully.")
        logger.info('================================================================================================')
    except Exception as e:
        logger.error(f"An error occurred during initialization: {e}")


def start_application(app_name: str):
    try:
        initialize_application()
        logger.info(f"Application {app_name.upper()} started successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    application_name = 'telegram-bot'
    start_application(application_name)