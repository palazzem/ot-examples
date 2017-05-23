"""Helpers that are used in examples. In the current state, we may not require
to put these classes and functions as part of the main proposal.
"""
import threading

from proposal import Tracer, tracer


class TracedThread(threading.Thread):
    """Helper class OpenTracing-aware, that continues the propagation of
    the current ActiveSpan in a new thread using an internal wrapper.
    """
    def __init__(self, *args, **kwargs):
        # implementation detail
        # get the ActiveSpan when we're in the "parent" thread
        self._active_span = tracer.active_span_source.active_span()
        super(TracedThread, self).__init__(*args, **kwargs)

    def run(self):
        # implementation detail
        # set the ActiveSpan in this thread and remove the local reference
        tracer.active_span_source.make_active(self._active_span)
        del self._active_span
        super(TracedThread, self).run()


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
