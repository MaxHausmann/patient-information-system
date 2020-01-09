"""
Special exceptions for common failures of this software
"""

class NotFoundException(Exception):
    """Basic class for things that can't be found """
    pass

class UserNotFoundException(NotFoundException):
    """User was not found in database."""
    pass

class PatientNotFoundException(NotFoundException):
    """Patient was not found in database."""
    pass

class PatientConnectionFailedException(Exception):
    """Patient could not be connected with helper."""
    pass

class UserConnectionFailedException(Exception):
    """User could not be connected with helper."""
    pass

class PatientDiagnosticsIncomplete(Exception):
    """Patient diagnostics could not be saved, because it is incomplete."""
    pass

class TableNotImplementedException(Exception):
    """Table name was not statically set."""
    pass

class PatientStatusInvalid(Exception):
    """Patient status is not valid."""
    pass