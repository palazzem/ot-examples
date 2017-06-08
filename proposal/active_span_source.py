class BaseActiveSpanSource(object):
    """BaseActiveSpanSource is the interface for a pluggable class that
    defines the source for the ActiveSpan. It must be used as a base class
    to implement the right behavior in the vendors specific implementation.
    """
    def make_active(self, span):
        """Makes the given `span` active, so that it can be used as a parent
        when calling the `start_active()` method of the Tracer. This method
        must keep track of the active Span stack, so that the previous one
        can be resumed when `span` is deactivated.
        """
        raise NotImplementedError

    def active_span(self):
        """Returns the current active Span depending on the specific
        implementation.
        """
        raise NotImplementedError

    def deactivate(self, span):
        """Deactivate the given `span`, restoring the previous active Span.
        This method must take in consideration that a Span may be deactivated
        when it's not really active. In that case, the current active stack
        must not be changed.
        """
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
