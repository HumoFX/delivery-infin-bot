import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
# Logger for Handling all errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)