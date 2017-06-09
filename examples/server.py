"""
A python program that encapsulates a range of cases OpenTracing must support:

    - simple tracing of operations where developers can trace standard things
      without paying too much attention to how tracing works (a.k.a. high level API)
    - complex asynchronous executions
"""
import asyncio

from ext import tracer
from ext.active_span_source import AsyncioActiveSpanSource


async def coro_db_1():
    with tracer.start_active_span("cache.query") as cache_span:
        # make a cache call before asking to db_1
        await asyncio.sleep(0.01)

        # suppose we always get a cache miss, now we query the DB
        with tracer.start_active_span("db.query_1") as db_span:
            await asyncio.sleep(0.2)
            return 1


async def coro_db_2():
    with tracer.start_active_span("db.query_2") as span:
        await asyncio.sleep(0.1)
        return 2


async def notification_email():
    # this notification is a background Task that doesn't become the active Span
    request_span = tracer.active_span_source.active_span
    with tracer.start_manual_span("notification.enqueue", child_of=request_span):
        await asyncio.sleep(0.8)


def get_data():
    # THIS FUNCTION ILLUSTRATES COMPLEX ASYNC BEHAVIOUR WHERE DEVELOPERS NEED MORE MANUAL CONTROL

    # kick off a background job that we will not block on (e.g. send an email)
    asyncio.ensure_future(notification_email())

    # start two pieces of data concurrently (i.e. query two databases)
    return asyncio.gather(*[coro_db_1(), coro_db_2()])


async def handle_request():
    # THIS FUNCTION ILLUSTRATES A POTENTIAL HIGH LEVEL API WHERE CONTEXT IS PROPOGATED
    # AUTOMATICALLY DEVELOPERS ONLY INTERACT WITH THE TRACER
    with tracer.start_active_span("web.request") as span:
        span.set_tag("url", "/home")
        data = await get_data()

        with tracer.start_active_span("template.render"):
            # fake template rendering
            return "%s" % (data)


async def run():
    loop = asyncio.get_event_loop()

    while True:
        # pretend the top level loop is a web server spawning requests or something
        await loop.create_task(handle_request())
        # yield to not block the async loop
        await asyncio.sleep(1)
