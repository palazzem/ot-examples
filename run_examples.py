from ext import tracer
from ext.active_span_source import (
    AsyncioActiveSpanSource,
    ThreadActiveSpanSource,
    GeventActiveSpanSource,
    TornadoActiveSpanSource,
)

from tornado.ioloop import IOLoop
from examples import asyncio, multi_threaded, gevent, tornado


if __name__ == '__main__':
    # asyncio examples
    tracer._active_span_source = AsyncioActiveSpanSource()
    asyncio.coroutine_continue_propagation()
    asyncio.coroutine_with_callbacks()

    # multi-threaded examples
    tracer._active_span_source = ThreadActiveSpanSource()
    multi_threaded.main_thread_instrumented_only()
    multi_threaded.main_thread_instrumented_children_continue()
    multi_threaded.main_thread_instrumented_children_not_continue()
    multi_threaded.main_thread_not_instrumented_children()

    # gevent examples
    tracer._active_span_source = GeventActiveSpanSource()
    gevent.main_greenlet_instrumented_only()
    gevent.main_greenlet_instrumented_children_continue()
    gevent.main_greenlet_instrumented_children_not_continue()
    gevent.main_greenlet_not_instrumented_children()

    # tornado (starts / stops the loop for each call)
    tracer._active_span_source = TornadoActiveSpanSource()
    IOLoop.current().run_sync(tornado.coroutines_propagation)
    IOLoop.current().run_sync(tornado.coroutines_without_propagation)
    IOLoop.current().run_sync(tornado.coroutine_with_a_callback)
    IOLoop.current().run_sync(tornado.tornado_plain_callback)
    IOLoop.current().run_sync(tornado.tornado_spawn_callback)
