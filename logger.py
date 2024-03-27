import logging

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Adjust this to the minimum severity level you want to log

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Add console handler again
logger.addHandler(console_handler)

# Example usage
logger.info('Starting the logger')
