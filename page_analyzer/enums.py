from enum import Enum


class Statuses(str, Enum):
    SUCCESS = 'success'
    NOT_SUCCESS = 'not success'
    ERROR = 'error'
