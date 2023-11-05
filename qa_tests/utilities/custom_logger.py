import inspect
import logging


def customLogger(logLevel=logging.DEBUG):
    # Gets the name of the class or method from where this method is called
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)
    # By default, log all the messages
    logger.setLevel(logging.DEBUG)

    # mode='a' will append to the existing log, for over-writing logs use mode='w'
    fileHandler = logging.FileHandler("automation.log", mode='w')
    fileHandler.setLevel(logLevel)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger
