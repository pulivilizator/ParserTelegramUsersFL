import time
from utilits.duplicate_remover import duplicate_remover
from members_parser import *


if __name__ == '__main__':
    start_app()
    duplicate_remover()
    print('Сбор данных завершен')
    while True: time.sleep(5000)