# log_config.py
import logging.config
import os
import sys

#read from yaml file configuration for logging
import yaml

#check file exists in pwd or in %appdata%/bike_log_log_config.yaml, if nothing exists create new one with defualt values
class LogConfig:
    def __init__(self):
        self.config_file = "log_config.yaml"
        self.configured = False
        self.default_config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s-[%(levelname)s]-%(message)s",
                    "datefmt": "%d-%m-%y-%H:%M:%S"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "default",
                    "filename": "log.txt"
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "file"]
            }
        }
        
    def read_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                config = yaml.safe_load(file)
                return config
        else:
            with open(self.config_file, "w") as file:
                yaml.dump(self.default_config, file)
                return self.default_config

    #return logger object with configuration
    def get_logger(self):
        if not self.configured:
            config = self.read_config()
            logging.config.dictConfig(config)
            self.configured = True
        return logging.getLogger()
    
    #function that either just sends message to terminal, logs to file, logs to file as a warning, as an error depending on user flags
    def log(self, logger, message, to_terminal=True, to_file=False, warning=False, error=False):
        if to_terminal:
            print(message)
        if to_file:
            if warning:
                logger.warning(message)
            elif error:
                logger.error(message)
            else:
                logger.info(message)
    
    #version information
    def version(self):
        return "0.1"
    