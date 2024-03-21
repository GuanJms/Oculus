import os
import glob


def walk_in_process(path, folders, func, func_params, condition_params):
    if len(folders) == 0:
        for file_path in glob.glob(os.path.join(path, '*.csv')):
            func(file_path, func_params)
    else:
        for root_path, dirs, files in os.walk(path):
            if folders[0] in dirs:
                if folders[0] in condition_params:
                    prev_dir = root_path.split('/')[-1]
                    if prev_dir not in condition_params[folders[0]]:  # folder[0] is the next target folder
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


def _update_expiration_dict(file_path: str, func_params: dict):
    root, _, _, _, file_name = split_path(file_path)
    date = func_params.get('quote_date', None)
    roots_expiration_dict = func_params.get('roots_expiration_dict')
    expiration_date_params = roots_expiration_dict.get(root, {})
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

                min_expiration_date = expiration_date_params.get('min_expiration_date', None)
                max_expiration_date = expiration_date_params.get('max_expiration_date', None)

                if min_expiration_date is not None and min_expiration_date > exp_date:
                    return
                if max_expiration_date is not None and max_expiration_date < exp_date:
                    return
                expiration_dates.append(exp_date)
                expiration_dict[root] = expiration_dates
    except Exception as e:
        return


def pathing_expirations(file_path: str, func_params: dict):
    """
    This function is used for quote board to get the expiration dates through pathing the market_data_system source.
    The expiration dates should be stored in the quote board during the initialization process.

    func_params = {root, quote_date, expirations: Optional[list], expiration_date_params: dict}
    expiration_date_params = {min_expiration_date: Optional[int], max_expiration_date: Optional[int]}
    """
    root, _, _, _, file_name = split_path(file_path)
    root = func_params.get('root', None)
    date = func_params.get('date', None)
    expiration_date_params = func_params.get('expiration_date_params', {})
    if root is None:
        raise ValueError('root must be specified in func_params')
    if date is None:
        raise ValueError('quote_date must be specified in func_params')
    expirations = expiration_date_params.get('expirations', [])
    expiration_date_params['expirations'] = expirations
    try:
        extension = file_name.split('.')[-1]
        if extension == 'csv':
            exp_date_quote_date = file_name.split('.')[0]
            parts = exp_date_quote_date.split('_')
            exp_date = int(parts[0])
            quote_date = int(parts[1])
            if quote_date == date:

                min_expiration_date = expiration_date_params.get('min_expiration_date', None)
                max_expiration_date = expiration_date_params.get('max_expiration_date', None)

                if min_expiration_date is not None and min_expiration_date > exp_date:
                    return
                if max_expiration_date is not None and max_expiration_date < exp_date:
                    return
                expirations.append(exp_date)
                expiration_date_params['expirations'] = expirations
    except Exception as e:
        return


def generate_path(root_system: str, root: str, date: int, expiration: int, quote_type_folder: str, extension: str):
    year = str(date)[:4]
    month = str(date)[4:6]
    expiration_date = str(expiration)
    date = str(date)
    file_name = f'{expiration_date}_{date}.{extension}'
    path = os.path.join(root_system, root, quote_type_folder, year, month, file_name)
    return path
