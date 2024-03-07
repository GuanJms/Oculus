import os
import glob

from data_process_module.traded_quote_data_manager import TradedQuoteDataManager


def update_expiration_dict(file_path: str, func_params: dict):
    root, _, _, _, file_name = split_path(file_path)
    date = func_params.get('quote_date', None)
    root_expirations = func_params.get('root_expirations')
    expiration_params = root_expirations.get(root, None)
    min_expiration = expiration_params.get('min_expiration', None)
    max_expiration = expiration_params.get('max_expiration', None)
    expiration_dict = func_params.get('expiration_dict')
    expiration_dates = expiration_dict.get(root, [])
    try:
        extension = file_name.split('.')[-1]
        if extension == 'csv':
            exp_date_quote_date = file_name.split('.')[0]
            parts = exp_date_quote_date.split('_')
            exp_date = int(parts[0])
            quote_date = int(parts[1])
            if quote_date == date:
                if min_expiration is not None and min_expiration > exp_date:
                    return
                if max_expiration is not None and max_expiration < exp_date:
                    return
                expiration_dates.append(exp_date)
                expiration_dict[root] = expiration_dates
    except Exception as e:
        return


def walk_in_process(path, folders, func, func_params, condition_params):
    if len(folders) == 0:
        for file_path in glob.glob(os.path.join(path, '*.csv')):
            func(file_path, func_params)
    else:
        for root_path, dirs, files in os.walk(path):
            if folders[0] in dirs:
                if folders[0] in condition_params:
                    prev_dir = root_path.split('/')[-1]
                    if prev_dir not in condition_params[folders[0]]: # folder[0] is the next target folder
                        continue
                walk_in_process(os.path.join(root_path, folders[0]), folders[1:], func, func_params, condition_params)
                # folder[1:] is the rest of the folders


def split_path(path: str):
    # path would be like /Users/jamesguan/Project/TemptDataHouse/SPX/raw_traded_quote/2024/01/20240719_20240126.csv
    parts = path.split('/')
    file_name = parts[-1]
    month = parts[-2]
    year = parts[-3]
    quote_type_folder = parts[-4]
    root = parts[-5]
    return root, quote_type_folder, year, month, file_name



root_system = "/Users/jamesguan/Project/TemptDataHouse"
quote_folder_name = "raw_traded_quote"

# walk through the root system to find the quote folder
date = 20240105
min_expiration = 20240105
max_expiration = 20240110
roots = ['SPY', 'SPX']
root_expirations = {
    'SPY': {
        'min_expiration': 20240105,
        'max_expiration': 20240307
    },
    'SPX': {'min_expiration': 20240105,
            'max_expiration': 20240110}
}
year = str(date)[:4]
month = str(date)[4:6]
expiration_dict = dict(zip(roots, [] * len(roots)))

func = update_expiration_dict
func_params = dict(date=date, root_expirations=root_expirations, expiration_dict=expiration_dict)
condition_params = {quote_folder_name: roots}
walk_in_process(root_system, [quote_folder_name, year, month], func, func_params, condition_params)

traded_quote_data_manager = TradedQuoteDataManager(config_file_path='config.json')
traded_quote_data_manager2 = TradedQuoteDataManager(config_file_path='config.json')
print(id(traded_quote_data_manager), id(traded_quote_data_manager2))

