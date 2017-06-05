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


def coroutine_with_a_callback():
    """The Tornado loop executes a child coroutine that starts a new
    active Span. Later on, that Span is retrieved and finished from a
    callback that is called when the coroutine is done.
    """

    @gen.coroutine
    def coroutine():
        # starts a new active Span
        tracer.start_active(operation_name='coroutine_child')

    @gen.coroutine
    def entrypoint():

        # callback that closes the active Span
        def on_finish(f):
            active_span = tracer.active_span_source.active_span()
            assert active_span is not None
            active_span.finish()

        # creating a future from the coroutine function, and then adding
        # a callback that is executed when the future is done
        future = coroutine()
        future.add_done_callback(on_finish)
        yield future

    # the callback will be executed within the TracerStackContext
    with TracerStackContext():
        return entrypoint()


def tornado_plain_callback():
    """The tornado loop executes the entrypoint coroutine that starts
    a new active Span. Later on, a generic callback is added to the IOLoop
    that retrieves and closes the previous created Span.
    """
    @gen.engine
    def on_finish():
        # callback that closes the active Span
        active_span = tracer.active_span_source.active_span()
        assert active_span is not None
        active_span.finish()

    @gen.coroutine
    def entrypoint():
        # starts a new active Span immediately
        tracer.start_active(operation_name='coroutine')

        # we simply set a generic callback in the IOLoop; this one
        # will be executed as soon as the IOLoop is available and it's
        # not related to the current execution of entrypoint
        IOLoop.current().add_callback(on_finish)

    # the callback will be executed within the TracerStackContext
    with TracerStackContext():
        return entrypoint()


def tornado_spawn_callback():
    """The tornado loop executes the entrypoint coroutine that starts
    a new active Span. Later on, a callback that doesn't inherit the StackContext
    is added to the IOLoop. This callback doesn't inherit the active Span
    and it is meant to work in that way by design.
    """
    @gen.engine
    def on_finish():
        # this callback doesn't inherit the active Span from the
        # other coroutine
        active_span = tracer.active_span_source.active_span()
        assert active_span is None

    @gen.coroutine
    def entrypoint():
        # starts a new active Span immediately
        tracer.start_active(operation_name='coroutine')

        # we spawn a fire-and-forget callback that (by definition)
        # must not interfere with the caller coroutine
        IOLoop.current().spawn_callback(on_finish)

    with TracerStackContext():
        return entrypoint()
