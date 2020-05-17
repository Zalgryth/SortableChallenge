from json import JSONEncoder


class DefaultEncoder(JSONEncoder):
    """Encodes plain data objects using the built-in Python dictionary."""

    def default(self, o):
        return o.__dict__
