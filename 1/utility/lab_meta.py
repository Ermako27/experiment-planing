from abc import ABCMeta
from PyQt5.sip import wrappertype as pyqtWrapperType


class LabMeta(pyqtWrapperType, ABCMeta):
    pass
