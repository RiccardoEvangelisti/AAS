class Config:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.__dict__[key] = Config(value)
            else:
                self.__dict__[key] = value

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError(f"'Config' object has no attribute '{name}'")
