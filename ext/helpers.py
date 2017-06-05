import gevent
import threading

from ext import tracer


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


class TracedGreenlet(gevent.Greenlet):
    """Helper class OpenTracing-aware, that ensures the context is propagated
    from a parent greenlet to a child when a new greenlet is initialized.
    """
    def __init__(self, *args, **kwargs):
        # get the current active span when we're in the "parent" greenlet
        self._active_span = tracer.active_span_source.active_span()

        # create the Greenlet as usual
        super(TracedGreenlet, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        # implementation detail: this method must not be overridden, but
        # it has been wrapped only to show that a TracedGreenlet can be
        # a specular implementation of a TracedThread
        tracer.active_span_source.make_active(self._active_span)
        del self._active_span
        super(TracedGreenlet, self).run()
