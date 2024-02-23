import time

from modules.utility import print_execution_time
from modules.selenium_wrapper import SeleniumWrapper


def main():

    spider = SeleniumWrapper()

    spider.setup_driver(headless=False)

    spider.get_page('https://www.google.com/')
    spider.element_send_keys(text='Who is lionel messi?',
                                selector='textarea[name="q"]',
                                )

    print('Chrome is opened and the search is done.')

    input('Exit? Press ENTER: ')
    
    del spider
    

if __name__ == '__main__':
    start_time = time.time()

    main()

    print_execution_time(start_time)
