import logging
logger = logging.getLogger('net_setting')
log_filename = "net_setting.log"
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='wb')
# logger.debug("efawefawf")