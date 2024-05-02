from global_component_id_generator import GlobalComponentIDGenerator


class QB_test:
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))

    @property
    def id(self):
        return self._id

class QB_Factory:
    qb_list = []

    @classmethod
    def create_quote_board(cls):
        qb_test = QB_test()
        cls.qb_list.append(qb_test)
        return qb_test

    @classmethod
    def delete_quote_board(cls, quote_board: QB_test):
        cls.qb_list.remove(quote_board)

    @classmethod
    def delete_all_quote_boards(cls):
        for quote_board in cls.qb_list:
            cls.delete_quote_board(quote_board)

class QB_deletor:

    @classmethod
    def delete_quote_board_list(cls, quote_board_list: list[QB_test]):
        for quote_board in quote_board_list:
            QB_Factory.delete_quote_board(quote_board)


from weakref import WeakValueDictionary, WeakSet

class QB_test_manager:
    def __init__(self):
        self._quote_board_dict: WeakValueDictionary[int, WeakSet] = WeakValueDictionary()

    def create_quote_board(self):
        for root_id in range(10):
            for _ in range(10):
                quote_board = QB_Factory.create_quote_board()
                if root_id not in self._quote_board_dict:
                    self._quote_board_dict[root_id] = WeakSet([quote_board])
                else:
                    self._quote_board_dict[root_id].add(quote_board)
    def get_quote_board_dict(self):
        return self._quote_board_dict
