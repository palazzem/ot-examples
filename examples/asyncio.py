"""Context propagation examples when dealing with single-threaded
asyncio loops. It uses the Python 3.5+ syntax for simplicity.
"""
import asyncio

from ext import tracer
from ext.active_span_source import AsyncioActiveSpanSource


# use a specific ActiveSpanSource implementation
tracer._active_span_source = AsyncioActiveSpanSource()


def coroutine_continue_propagation():
    """The asyncio loop executes two chained coroutines; the second
    traced coroutine is a child of the first coroutine even if a
    cooperative yield happens.
    """
    async def do_async_work():
        # executed in the main thread
        with tracer.start_active(operation_name='some_work'):
            # do some IO-bound work
            pass

    async def execute_job():
        # executed in the main thread
        with tracer.start_active(operation_name='execute_job'):
            await do_async_work()
            # ...do more work in this loop...

    loop = asyncio.get_event_loop()
    future = loop.create_task(execute_job())
    loop.run_until_complete(future)


def coroutine_with_callbacks():
    """The asyncio loop executes two chained coroutines with the
    second one that expects a success callback (that is also a
    coroutine). The callback that may be scheduled later because of
    two cooperative yields, retrieves the right ActiveSpan, setting
    a tag and finishing the Span.
    """
    async def success():
        span = tracer.active_span_source.active_span()
        assert span is not None
        span.set_tag('result', 'success')
        span.finish()

    async def do_async_work(cb_success):
        # executed in the main thread; do some IO-bound work
        span = tracer.start_active(operation_name='some_work')
        is_success = True
        if is_success:
            await cb_success()

        # ...do more work that is not traced in some_work span...

    async def execute_job():
        # executed in the main thread
        with tracer.start_active(operation_name='execute_job'):
            await do_async_work(success)
            # ...do more work in this loop...

    loop = asyncio.get_event_loop()
    future = loop.create_task(execute_job())
    loop.run_until_complete(future)
