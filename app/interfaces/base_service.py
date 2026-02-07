from abc import ABC


class BaseService(ABC):
    def __init__(self, session):
        self.session = session
