from opentracing.span import Span as OTBaseTracer


class Span(OTBaseTracer):
    """Span class that provides some extensions to the Python OpenTracing API.
    This class includes all methods that may be added to the OT Span class,
    so that the proposed interface is public accessible
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ends context manager and calls finish() on the span.
        If exception has occurred during execution, it is automatically added
        as a tag to the span.

        Note: this method extends the current context manager
        """
        if exc_type:
            self.log_kv({
                'python.exception.type': exc_type,
                'python.exception.val': exc_val,
                'python.exception.tb': exc_tb,
                })

        # when the context manager is closed, we deactivate the current
        # active Span before calling the finish()
        self._tracer.active_span_source.deactivate(self)
        self.finish()
