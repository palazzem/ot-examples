"""Helpers that are used in examples. In the current state, we may not require
to put these classes and functions as part of the main proposal.
"""
import threading

from proposal import tracer


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
