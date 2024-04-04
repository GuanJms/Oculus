def csv_iter_generator(file_name: str):
    with open(file_name, "r") as file:
        for line in file:
            # get rid of the newline character
            line = line.strip()
            yield line.split(",")

class CSVReader:
    def __init__(self, file_name: str):
        self.empty = False
        self.peek = None
        self.generator = csv_iter_generator(file_name)
        try:
            self.peek = next(self.generator)
        except StopIteration:
            self.empty = True

    def __iter__(self):
        return self

    def __next__(self):
        """
        Return the self.peek element, or raise StopIteration
        if empty
        """
        if self.empty:
            raise StopIteration()
        to_return = self.peek
        try:
            self.peek = next(self.generator)
        except StopIteration:
            self.peek = None
            self.empty = True
        return to_return

    def is_empty(self):
        return self.empty


def split_path(path: str):
    # path would be like /Users/jamesguan/Project/TemptDataHouse/SPX/raw_traded_quote/2024/01/20240719_20240126.csv
    parts = path.split('/')
    file_name = parts[-1]
    month = parts[-2]
    year = parts[-3]
    quote_type_folder = parts[-4]
    root = parts[-5]
    return root, quote_type_folder, year, month, file_name
