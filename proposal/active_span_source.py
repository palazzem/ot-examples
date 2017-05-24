import asyncio
import threading


class BaseActiveSpanSource(object):
    """BaseActiveSpanSource is the interface for a pluggable class that
    defines the source for the ActiveSpan. It must be used as a base class
    to implement the right behavior in the vendors specific implementation.
    """
    def make_active(self, span):
        raise NotImplementedError

    def active_span(self, span):
        raise NotImplementedError


class NoopActiveSpanSource(BaseActiveSpanSource):
    """ActiveSpanSource provides the logic to get and set the current
    ActiveSpan. This is a cheap noop implementation that must be implemented
    by Tracer developers.
    """
    def make_active(self, span):
        return None

    def active_span(self):
        return None


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

        # get the current running Task and set a new Span
        task = asyncio.Task.current_task(loop=loop)
        setattr(task, '__active_span', span)

    def active_span(self, loop=None):
        # implementation detail
        # retrieves the current running loop if not provided
        loop = loop or asyncio.get_event_loop()

        # get the current running Task for this loop and return the ActiveSpan
        task = asyncio.Task.current_task(loop=loop)
        return getattr(task, '__active_span', None)
