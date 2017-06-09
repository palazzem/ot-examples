from opentracing.span import Span as OTBaseSpan


class Span(OTBaseSpan):
    """Span class that provides some extensions to the Python OpenTracing API.
    This class includes all methods that may be added to the OT Span class,
    so that the proposed interface is public accessible
    """

    def __init__(self, tracer, context):
        self._tracer = tracer
        self._context = context
        self._deactivate_on_finish = False

    def finish(self, finish_time=None):
        """Indicates that the work represented by this span has completed or
        terminated. When the `Span` is finished, it must be deactivated from the
        ActiveSpanSource that generated it.
        With the exception of the `Span.context` property, the semantics of all
        other Span methods are undefined after `finish()` has been invoked.
        :param finish_time: an explicit Span finish timestamp as a unix
            timestamp per time.time()
        """
        if self._deactivate_on_finish:
            self._tracer.active_span_source.deactivate(self)
