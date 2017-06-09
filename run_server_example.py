import asyncio

from ext import tracer
from ext.active_span_source import AsyncioActiveSpanSource

from examples import server


if __name__ == '__main__':
    # start a fake web server with a complex interaction
    tracer._active_span_source = AsyncioActiveSpanSource()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(server.run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
