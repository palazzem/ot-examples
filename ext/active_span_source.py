import asyncio
import threading
import gevent.local

from proposal.active_span_source import BaseActiveSpanSource


class ThreadActiveSpanSource(BaseActiveSpanSource):
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


class AsyncioActiveSpanSource(BaseActiveSpanSource):
    """This is a simplified implementation to make the asyncio examples
    work as expected. It uses the current Task instance as a carrier
    for of the current ActiveSpan available in this execution.

    Here we store the `active_span` but it could be anything else that
    is used by Tracer developers.
    """
    def make_active(self, span, loop=None):
        # implementation detail
        # retrieves the current running loop if not provided
        loop = loop or asyncio.get_event_loop()

        # get the current active span and set the ancestor active Span
        to_restore = self.active_span(loop=loop)
        setattr(span, '_to_restore', to_restore)

        # get the current running Task and set a new Span
        task = asyncio.Task.current_task(loop=loop)
        setattr(task, '__active_span', span)

        # explicitly set the flag for automatic deactivation
        span._deactivate_on_finish = True

    def active_span(self, loop=None):
        # implementation detail
        # retrieves the current running loop if not provided
        loop = loop or asyncio.get_event_loop()

        # get the current running Task for this loop and return the ActiveSpan
        task = asyncio.Task.current_task(loop=loop)
        return getattr(task, '__active_span', None)

    def deactivate(self, span, loop=None):
        # implementation detail
        # retrieves the current running loop if not provided
        loop = loop or asyncio.get_event_loop()

        # get the current active span and ignore if the current active branch
        # is not the one we're trying to deactivate
        active = self.active_span(loop=loop)
        if span is not active:
            return

        # get span to restore
        to_restore = getattr(span, '_to_restore', None)

        # restore it
        task = asyncio.Task.current_task(loop=loop)
        setattr(task, '__active_span', to_restore)

class GeventActiveSpanSource(BaseActiveSpanSource):
    """This is a simplified implementation to make the gevent examples
    work as expected. It uses a greenlet local storage to keep track of
    the current ActiveSpan available in this execution.

    Here we store the `active_span` but it could be anything else that
    is used by Tracer developers.
    """
    def __init__(self):
        self._locals = gevent.local.local()

    def make_active(self, span):
        # implementation detail
        setattr(self._locals, 'active_span', span)

    def active_span(self):
        # implementation detail
        return getattr(self._locals, 'active_span', None)
