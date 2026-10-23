"""
Custom exceptions thrown by Open edX events tooling.
"""


class OpenEdxEventException(Exception):
    """
    Base class for Open edX Events exceptions.
    """

    def __init__(self, message=""):
        """
        Init method for OpenEdxEventException base class.

        Arguments:
            message (str): message describing why the exception was raised.
        """
        super().__init__()
        self.message = message

    def __str__(self):
        """
        Show string representation of OpenEdxEventException using its message.

        Returns:
            str: message describing why the exception was raised.
        """
        return self.message


class InstantiationError(OpenEdxEventException):
    """
    Describes errors that occur while instantiating events.

    This exception is raised when there's an error instantiating an Open edX
    event, it can be that a required argument for the event definition is
    missing.
    """

    def __init__(self, event_type="", message=""):
        """
        Init method for InstantiationError custom exception class.

        Arguments:
            event_type (str): name of the event raising the exception.
            message (str): message describing why the exception was raised.
        """
        super().__init__(
            message="InstantiationError {event_type}: {message}".format(
                event_type=event_type, message=message
            )
        )


class SenderValidationError(OpenEdxEventException):
    """
    Describes errors that occur while validating arguments of send methods.
    """

    def __init__(self, event_type="", message=""):
        """
        Init method for SenderValidationError custom exception class.

        Arguments:
            event_type (str): name of the event raising the exception.
            message (str): message describing why the exception was raised.
        """
        super().__init__(
            message="SenderValidationError {event_type}: {message}".format(
                event_type=event_type, message=message
            )
        )


class ProducerConfigurationError(OpenEdxEventException):
    """
    Describes errors that occurs while validating format of producer signal configuration.
    """

    def __init__(self, event_type="", message=""):
        """
        Init method for ProducerConfigurationError custom exception class.

        Arguments:
            event_type (str): name of the event raising the exception.
            message (str): message describing why the exception was raised.
        """
        super().__init__(
            message="ProducerConfigurationError {event_type}: {message}".format(
                event_type=event_type, message=message
            )
        )
