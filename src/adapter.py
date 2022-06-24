import pdb


class BaseAdapter:
    def __init__(self):
        pass

    def position_details(self):
        pass

    def close_position(self):
        pass

    def create_order(self):
        pass

    def account_balance(self):
        pass

    def order_details(self):
        pass

    def open_order_details(self):
        pass


class Adapter(BaseAdapter):
    methods = [
        "position_details",
        "close_position",
        "create_order",
        "account_balance",
        "order_details"

    ]

    def __init__(self, api):
        BaseAdapter.__init__(self)
        self._api = api
        for attr in dir(self._api):
            obj = getattr(self._api, attr)
            if hasattr(obj, "mark") and getattr(obj, "mark") in dir(self):
                self.__dict__.update({obj.mark: obj})

    def position_details_marker(fnc):
        def wrapper():
            fnc.mark = "position_details"
            return fnc
        return wrapper()

    def close_position_marker(fnc):
        def wrapper():
            fnc.mark = "close_position"
            return fnc
        return wrapper()

    def create_order_marker(fnc):
        def wrapper():
            fnc.mark = "create_order"
            return fnc
        return wrapper()

    def account_balance_marker(fnc):
        def wrapper():
            fnc.mark = "account_balance"
            return fnc
        return wrapper()

    def order_details_marker(fnc):
        def wrapper():
            fnc.mark = "order_details"
            return fnc
        return wrapper()

    def open_order_details_marker(fnc):
        def wrapper():
            fnc.mark = "open_order_details"
            return fnc
        return wrapper()

    def __getattr__(self, attr: str):
        return getattr(self._api, attr)
