import threading


class BaseActiveSpanSource(object):
    """BaseActiveSpanSource is the interface for a pluggable class that
    defines the source for the ActiveSpan. It must be used as a base class
    to implement the right behavior in the vendors specific implementation.
    """
    def make_active(self, span):
        raise NotImplementedError

    def active_span(self, span):
        raise NotImplementedError


class NoopActiveSpanSource(BaseActiveSpanSource):
    """ActiveSpanSource provides the logic to get and set the current
    ActiveSpan. This is a cheap noop implementation that must be implemented
    by Tracer developers.
    """
    def make_active(self, span):
        return None

    def active_span(self):
        return None


class ThreadActiveSpanSource():
    """This is a simplified implementation to make the multi-threading
    examples work as expected. It uses a thread local storage to keep
    track of the current ActiveSpan available in this thread execution.

    Here we store the `active_span` but it could be anything else that
    is used by Tracer developers.
    """
    def __init__(self):
        self._locals = threading.local()

    def make_active(self, span):
        # implementation detail
        setattr(self._locals, 'active_span', span)

    def active_span(self):
        # implementation detail
        return getattr(self._locals, 'active_span', None)
