from configs import Configs
from typing import Type


class Singleton:
    def __call__(cls_, *args, **kwargs):
        if not cls_.has_instance():
            cls_.instance = super(Singleton, cls_).__call__(*args, **kwargs)
        return cls_.instance

    def has_instance(cls_):
        return hasattr(cls_, "instance")


class Facade(metaclass=Singleton):
    def __init__(self):
        self.secrets: Type[Configs] = Configs()
