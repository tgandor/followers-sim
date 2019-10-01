class Settings:
    """
    Settings for the Followers application.
    """
    _jitter = False

    @property
    def jitter(self):
        return self._jitter

    @jitter.setter
    def jitter(self, value):
        self._jitter = bool(value)

    @property
    def number_of_people(self):
        return 32

    @property
    def canvas_size(self):
        return 600

    @property
    def dot_size(self):
        return 10

    @property
    def person_speed(self):
        return 0.003

    @property
    def target_distance_min(self):
        return 0.05

    @property
    def min_distance_to_other(self):
        return 0.015


# TODO: make more properties modifiable from GUI?
_default = Settings()


def get():
    return _default
