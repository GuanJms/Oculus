def get_stock_quote_path(**kwargs):
    if 'root' not in kwargs:
        raise ValueError('Root is required')
    if 'date' not in kwargs:
        raise ValueError('Date is required')

    data_server_path = ConfigurationManager.get_path_config()


def get_stock_traded_quote_path():
    return None


def get_option_quote_path():
    return None


def get_option_traded_quote_path():
    return None