import time


def price_float(price: str) -> float:
    if not price.strip():
        return 0
    return round(float(price.replace('€', '').replace('.', '').replace(',', '.').strip()), 2)


def print_execution_time(start_time: float) -> None:
    print('\nExecution time: {} min'.format(
        round((time.time() - start_time)/60, 2)))
