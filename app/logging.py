import logging

logger = logging.getLogger('task-logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#log in console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

#log in file
file_handler = logging.FileHandler('task-logger.log', encoding='utf-8')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)