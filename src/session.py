

class Session:

    def __init__(self):
        self._options = dict(
            leverage=None,
            profit_trashold=None,
            loss_trashold=None,
            pair="",
            exchange="",
            key="",
            secret="",
            passphrase="",
            api=None
        )

    def update(self, options):
        self._options.update(options)

    def __getitem__(self, item):
        return self._options[item]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __getattr__(self, item):
        try:
            return self._options[item]
        except KeyError:
            raise AttributeError(item)

    def get(self):
        return self._options
