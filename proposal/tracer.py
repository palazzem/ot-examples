from opentracing.tracer import Tracer as OTBaseTracer

from .active_span_source import NoopActiveSpanSource


class TracerProposal(OTBaseTracer):
    """Tracer class that provides some extensions to the Python OpenTracing
    API. This class includes all methods that may be added to the OT Tracer
    class, so that the proposed interface is public accessible.
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
        """The body of the method is an implementation detail"""
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


class TracerExample(TracerProposal):
    """Tracer class example that is not part of the proposal. The purpose
    of this class is to list some implementation details tha may be needed
    when developing a real tracer.
    """
    def record(self, span):
        """This method has been taken from the `basictracer-python`,
        adding a over-simplified interaction when the ActiveSpan is finished
        and then recorded.

        This code is not a working solution, but it's here only to give the
        idea that Frameworks and Applications developers should not take
        care of choosing the right ActiveSpan.

        In general, when a Span is finished, its parent must be reactivated
        automatically. This consideration is valid only for synchronous
        applications, and it will not work when using executions models (i.e.
        async) where the finishing order is not guaranteed. In that case,
        another Span will be reactivated according to the ActiveSpanSource
        specific implementation.
        """
        # Deactivate the current ActiveSpan, using the specific ActiveSpanSource
        # implementation to choose the proper way to reactivate the right parent.
        self.active_span_source.make_active(span._parent)
        self.recorder.record_span(span)
