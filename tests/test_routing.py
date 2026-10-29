import re

import pytest
from fastmcp.exceptions import ClientError
from inline_snapshot import snapshot
from mcp.types import TextContent

from unofficial_mapy_com_mcp.models.mapy.common.types import Coordinates
from unofficial_mapy_com_mcp.models.mapy.route.request import RouteRequest
from unofficial_mapy_com_mcp.models.requests import ApiRouteRequest


def test_route_request_waypoints_serialization():
    api_req = ApiRouteRequest(
        start=Coordinates(lon=14.4000936, lat=50.0898689),
        end=Coordinates(lon=16.6085958, lat=49.1948039),
        route_type='car_fast_traffic',
        avoid_toll=False,
        waypoints=[Coordinates(lon=15.5, lat=49.5)],
    )
    route_req = RouteRequest.from_api_model(api_req)
    assert route_req.model_dump() == {
        'start': '14.4000936,50.0898689',
        'end': '16.6085958,49.1948039',
        'routeType': 'car_fast_traffic',
        'waypoints': ['15.5,49.5'],
        'avoid_toll': False,
    }


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_routing(mcp_client):
    async with mcp_client:
        request = ApiRouteRequest(
            start=Coordinates(lon=14.4000936, lat=50.0898689),
            end=Coordinates(lon=16.6085958, lat=49.1948039),
            route_type='car_fast_traffic',
            avoid_toll=False,
            waypoints=None,
        )

        result = await mcp_client.call_tool('maps_route', arguments={'query': request.model_dump()})
        assert result == snapshot([TextContent(type='text', text='{"length": 211731, "duration": 7311}')])


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_routing_not_reachable(mcp_client):
    async with mcp_client:
        request = ApiRouteRequest(
            start=Coordinates(lon=0, lat=0),
            end=Coordinates(lon=16.6085958, lat=49.1948039),
            route_type='car_fast_traffic',
            avoid_toll=False,
            waypoints=None,
        )
        with pytest.raises(ClientError):
            await mcp_client.call_tool('maps_route', arguments={'query': request.model_dump()})


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_routing_different_continent(mcp_client):
    async with mcp_client:
        request = ApiRouteRequest(
            start=Coordinates(lon=0, lat=0),
            end=Coordinates(lon=16.6085958, lat=49.1948039),
            route_type='car_fast_traffic',
            avoid_toll=False,
            waypoints=None,
        )
        with pytest.raises(
            ClientError,
            match='The route point is outside the available route network for the selected type of transport.',
        ):
            await mcp_client.call_tool('maps_route', arguments={'query': request.model_dump()})


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_unknown_error_codes(mcp_client):
    async with mcp_client:
        request = ApiRouteRequest(
            start=Coordinates(lon=0, lat=0),
            end=Coordinates(lon=16.6085958, lat=49.1948039),
            route_type='car_fast_traffic',
            avoid_toll=False,
            waypoints=None,
        )
        with pytest.raises(
            ClientError,
            match=re.escape('Error executing tool maps_route: Encountered following errors:\n* no monee\n* ovrloded'),
        ):
            await mcp_client.call_tool('maps_route', arguments={'query': request.model_dump()})
