import time
import traceback
from html import unescape

from modules.utility import print_execution_time
from modules.olx import OLX

import pandas as pd

def main():
    df = pd.read_excel('files/olx_data.xlsx', sheet_name='Cars')
    df['Description'] = df['Description'].apply(unescape)
    cars = df.to_dict(orient='records')
    
    df = pd.read_excel('files/olx_data.xlsx', sheet_name='Accounts')
    accounts = df.to_dict(orient='records')

    for account in accounts:
        olx = OLX()
        if olx.login(account['username'], account['password']):
            for index, car in enumerate(cars):
                olx.post_item(car)
                if index == 0:
                    olx.uncheck_view_profile()
        

if __name__ == '__main__':
    start_time = time.time()
    
    try:
        main()
    except Exception:
        traceback.print_exc()
    finally:
        print_execution_time(start_time)
        

