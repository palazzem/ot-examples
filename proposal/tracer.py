from opentracing.tracer import Tracer as OTBaseTracer


class Tracer(OTBaseTracer):
    """Tracer class that provides some extension to the base OpenTracing
    API for Python. This class must define all new / updated API
    so that they can be used in some examples.

    Defined methods must be implemented as noop for the moment.
    """
    def __init__(self):
        # create the tracer as defined in OpenTracing `Tracer` class
        super(Tracer, self).__init__()
        # this class may be changed when the vendor specific
        # implementation is initialized
        self._active_span_source = NoopActiveSpanSource()

    @property
    def active_span_source(self):
        return self._active_span_source

    def start_active(self, operation_name, tags=None, start_time=None):
        # implementation detail
        # get the current Span (or None)
        parent_span = self.active_span_source.active_span()

        # create a new Span child (if a parent is available)
        span = self.start_span(
            operation_name=operation_name,
            child_of=parent_span,
            tags=tags,
            start_time=start_time,
        )

        # set it as active Span
        self.active_span_source.make_active(span)
        return span


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
