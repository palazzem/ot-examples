from opentracing.tracer import Tracer as OTBaseTracer

from .active_span_source import NoopActiveSpanSource


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
