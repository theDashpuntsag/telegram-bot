import logging
import colorlog
from logging.handlers import TimedRotatingFileHandler
from libs.date_formatter import DateFormatter
import os


class ErrorLineFormatter(colorlog.ColoredFormatter):
    """Custom formatter that adds line information only for ERROR and CRITICAL logs"""
    
    def format(self, record):
        # Check if this is an error or critical log
        if record.levelno >= logging.ERROR:
            # Use format with line information for errors
            self._style._fmt = '%(log_color)s%(asctime)s | %(module)s | line: %(lineno)d | %(levelname)s | %(message)s'
        else:
            # Use format without line information for other levels
            self._style._fmt = '%(log_color)s%(asctime)s | %(module)s | %(levelname)s | %(message)s'
        
        return super().format(record)


# Setting up log saving directory if it doesn't exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir);
 

# Start configuring the logger
logger = logging.getLogger('CUSTOM0-PYTHON-LOGGER');


# Set the log level based on the environment
log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper();
logger.setLevel(getattr(logging, log_level, logging.DEBUG));

# Creating a console handler
console_handler = logging.StreamHandler();
file_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, f"log-{DateFormatter.get_formatted_current_datetime()}.log"),
    when='midnight', 
    interval=1, 
    backupCount=60
)
file_handler.suffix = "%Y-%m-%d.log"
file_handler.extMatch = r"^\d{4}-\d{2}-\d{2}.log$"

# Setting handlers level
console_handler.setLevel(logging.DEBUG);
file_handler.setLevel(logging.DEBUG);

# Define log colors
log_colors = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}
# Create formatters with line information only for errors
color_formatter = ErrorLineFormatter(
    '%(log_color)s%(asctime)s | %(module)s | %(levelname)s | %(message)s',
    log_colors=log_colors,
    reset=True,
    style='%'
)

file_formatter = logging.Formatter(
    '%(name)s | %(asctime)s  | %(module)s | line: %(lineno)d | %(levelname)s |  %(message)s'
)
# Add formatters to handlers
console_handler.setFormatter(color_formatter)
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.propagate = False
logger.info("Logger setup complete and ready.")


for handler in logger.handlers:
    if isinstance(handler, TimedRotatingFileHandler):
        handler.flush()
        handler.close()