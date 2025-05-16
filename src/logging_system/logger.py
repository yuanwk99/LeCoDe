# logging_system/logger.py

import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs",conversation_id="None"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        # Configure logging
        self.logger = logging.getLogger("LegalConsultationLogger")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        # Create a file handler for each conversation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = os.path.join(self.log_dir, f"conversation_{conversation_id}_{timestamp}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, speaker, message):
        self.logger.info(f"{speaker}: {message}")
