from proposal import Tracer


class TracerImplementation(Tracer):
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
