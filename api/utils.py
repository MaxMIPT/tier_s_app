from fastapi import Request
from temporalio.client import Client


async def get_temporal_client(
        request: Request
) -> Client:
    return request.app.state.temporal_client
