import logging
import logging.handlers

def logging_func(name:str, path: str) -> [logging.handlers.RotatingFileHandler,logging.Logger]:
    """
    this is logging config function, instead of logging.conf.
    provides great flexiblity, logging control and customization
    """
    #create logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create file handler and set level to info
    fh = logging.handlers.RotatingFileHandler(path,maxBytes=10000**2, backupCount=5)
    fh.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to fh
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    return fh,logger
