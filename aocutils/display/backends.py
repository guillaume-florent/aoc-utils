# coding: utf-8

r"""backends.py module

Graphical backends presence testing

"""


def available_backends():
    r"""List of available backends

    Returns
    -------
    list[str]
        List of available backends

    """
    backends = list()
    try:
        import wx
        backends.append("wx")
    except ImportError:
        pass
        # logger.warning("No wx backend")
    try:
        import PySide
        backends.append("qt-pyside")
    except ImportError:
        pass
        # logger.warning("No PySide backend")
    try:
        import PyQt4
        backends.append("qt-pyqt4")
    except ImportError:
        pass
        # logger.warning("No PyQt4 backend")
    try:
        import PyQt5
        backends.append("qt-pyqt5")
    except ImportError:
        pass
        # logger.warning("No PyQt5 backend")

    return backends
