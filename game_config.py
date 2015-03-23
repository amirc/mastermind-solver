class GameConfig:
    def __init__(self, slots, options):
        self._options = options
        self._slots = slots

    @property
    def options(self):
        return self._options

    @property
    def slots(self):
        return self._slots
