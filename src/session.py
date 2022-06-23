

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
            passpharase=""
        )

    def update(self, options):
        self._options.update(options)
