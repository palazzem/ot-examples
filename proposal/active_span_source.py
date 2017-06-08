class BaseActiveSpanSource(object):
    """BaseActiveSpanSource is the interface for a pluggable class that
    defines the source for the ActiveSpan. It must be used as a base class
    to implement the right behavior in the vendors specific implementation.
    """
    def make_active(self, span):
        raise NotImplementedError

    def active_span(self, span):
        raise NotImplementedError

    def deactivate(self, span):
        raise NotImplementedError


class NoopActiveSpanSource(BaseActiveSpanSource):
    """ActiveSpanSource provides the logic to get and set the current
    ActiveSpan. This is a cheap noop implementation that is used when
    a specific implementation is not enabled.
    """
    def make_active(self, span):
        return None

    def active_span(self):
        return None

    def deactivate(self, span):
        return None
