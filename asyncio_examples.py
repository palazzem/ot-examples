"""Context propagation examples when dealing with single-threaded
asyncio loops. It uses the Python 3.5+ syntax for simplicity.

TODO: provide a better description for each example describing
the exact use case.
"""
import asyncio

from proposal import tracer, helpers
from proposal.active_span_source import NoopActiveSpanSource


# set the NoopActiveSpanSource for those examples
# TODO: move it somewhere else
tracer._active_span_source = NoopActiveSpanSource()


def coroutine_continue_propagation():
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
    def success():
        span = tracer.active_span_source.active_span()
        if span:
            span.set_tag('result', 'success')
            span.finish()

    def failure():
        span = tracer.active_span_source.active_span()
        if span:
            span.set_tag('result', 'failure')
            span.finish()

    async def do_async_work(cb_success, cb_failure):
        # executed in the main thread; do some IO-bound work
        span = tracer.start_active(operation_name='some_work')
        is_success = True
        if is_success:
            cb_success()
        else:
            cb_failure()

        # ...do more work that is not traced in some_work span...

    async def execute_job():
        # executed in the main thread
        with tracer.start_active(operation_name='execute_job'):
            await do_async_work(success, failure)
            # ...do more work in this loop...

    loop = asyncio.get_event_loop()
    future = loop.create_task(execute_job())
    loop.run_until_complete(future)


if __name__ == '__main__':
    coroutine_continue_propagation()
    coroutine_with_callbacks()
