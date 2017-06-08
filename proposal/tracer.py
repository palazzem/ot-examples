from opentracing.tracer import Tracer as OTBaseTracer

from .active_span_source import NoopActiveSpanSource


class Tracer(OTBaseTracer):
    """Tracer class that provides some extensions to the Python OpenTracing
    API. This class includes all methods that may be added to the OT Tracer
    class, so that the proposed interface is public accessible.
    """
    def __init__(self, *args, **kwargs):
        # create the tracer as defined in OpenTracing `Tracer` class
        super(Tracer, self).__init__(*args, **kwargs)
        # this instance may be changed when the vendor specific
        # implementation is initialized
        self._active_span_source = NoopActiveSpanSource()

    @property
    def active_span_source(self):
        return self._active_span_source

    def start_manual_span(self,
                          operation_name=None,
                          child_of=None,
                          references=None,
                          tags=None,
                          start_time=None):
        """This method supersede the original start_span. When developers
        use that method, a new Span is created without changing the current
        Span stack.
        """
        return self._noop_span

    def start_active_span(self, operation_name, tags=None, start_time=None):
        """This is a simplified implementation to start a new Span
        that is marked as active.
        """
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
