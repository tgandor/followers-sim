class Settings:
    """
    Settings for the Followers application.
    """

    @property
    def number_of_people(self):
        return 20

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

# TODO: make modifiable from GUI
_default = Settings()


def get():
    return _default