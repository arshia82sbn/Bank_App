import logging
import threading

class LogManager:
    _instance = None
    _lock = threading.Lock()  # for thread-safety
    _initialized = False

    def __new__(cls):
        #check here and make sure to work
        if cls._instance is None:
            with cls._lock:  # lock for make sure to protect the create more log in thread
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if LogManager._initialized:
            return
        with LogManager._lock:  # lock it for make sure to run once 
            if LogManager._initialized:
                return
            LogManager._initialized = True

            # تنظیم لاگر
            self.logger = logging.getLogger("BankApp")
            self.logger.setLevel(logging.DEBUG)  # DEBUG level for most of the Level
            if not self.logger.handlers:  # protecting of increasing more and repeated handler 
                # set the format of the log
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

                # # File Handler with encoding
                # file_handler = logging.FileHandler(
                #     'bank_system.log',
                #     encoding='utf-8'
                # )
                # file_handler.setFormatter(formatter)
                # file_handler.setLevel(logging.DEBUG)  #set the all of the loggs in the consol

                # Console Handler with encoding
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.INFO)  # only about info and oth

                # self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def get_logger():
    return LogManager().get_logger()