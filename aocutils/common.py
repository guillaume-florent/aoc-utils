# coding: utf-8

r"""functions and classes common to all modules"""


class AssertIsDone(object):
    r"""Raises an assertion error when IsDone() returns False,
    with the error specified in error_statement

    This is a context manager.
    
    Parameters
    ----------
    to_check : object
        The object to check. Must have an IsDone() function.
    error_statement: str
        Error explanation

    """
    def __init__(self, to_check, error_statement):
        self.to_check = to_check
        self.error_statement = error_statement

    def __enter__(self, ):
        if self.to_check.IsDone():
            pass
        else:
            msg = self.error_statement
            logger.error(msg)
            raise AssertionError(msg)

    def __exit__(self, assertion_type, value, traceback):
        pass
