"""Context propagation examples when dealing with single-threaded
Tornado loops.
"""
from tornado import gen
from tornado.ioloop import IOLoop

from ext import tracer
from ext.tornado.stack_context import TracerStackContext


def coroutines_propagation():
    """The Tornado loop executes two chained coroutines; the second
    traced coroutine is a child of the first one even if a cooperative
    yield happens. The propagation happens when a `TracerStackContext`
    is used to provide a context-local storage.
    """
    @gen.coroutine
    def coroutine_child():
        active_span = tracer.active_span_source.active_span()
        assert active_span is not None
        with tracer.start_active(operation_name='coroutine_child'):
            pass

    @gen.coroutine
    def entrypoint():
        with tracer.start_active(operation_name='coroutine_parent') as span:
            coro = [coroutine_child() for i in range(5)]
            yield coro

    # because we're tracing our execution within a TracerStackContext,
    # the propagation is possible between coroutines. This is not a kind
    # of feature flag, but it's a functionality that must be provided
    # by the vendor or by the framework itself.
    with TracerStackContext():
        return entrypoint()


def coroutines_without_propagation():
    """The Tornado loop executes two chained coroutines; the second
    traced coroutine is a child of the first one but because we're
    outside of a `TracerStackContext` (or similar context-local storage)
    a context-local storage is not available.
    """
    @gen.coroutine
    def coroutine_child():
        active_span = tracer.active_span_source.active_span()
        assert active_span is None
        with tracer.start_active(operation_name='coroutine_child'):
            pass

    @gen.coroutine
    def entrypoint():
        with tracer.start_active(operation_name='coroutine_parent') as span:
            coro = [coroutine_child() for i in range(5)]
            yield coro

    # the propagation doesn't happen
    return entrypoint()
