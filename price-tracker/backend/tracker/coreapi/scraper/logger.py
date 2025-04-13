import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("scraper/logs/scraper.log"),
            logging.StreamHandler()
        ]
    )
    
    # Return a logger that can be imported by other modules
    return logging.getLogger("pc_parts_scraper")

# Create a logger instance that can be imported
logger = setup_logger()