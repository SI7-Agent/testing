import logging


class MyLogger:
    log_name = 'logs.log'
    msg_form = '%(asctime)s - %(message)s'
    dt_form = '%d-%b-%y %H:%M:%S'
    level = logging.INFO
    logging.basicConfig(filename=log_name, format=msg_form,
                        datefmt=dt_form, level=level)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def critical(msg):
        logging.critical(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)
