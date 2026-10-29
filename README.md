# Unofficial Mapy.com MCP Server

An unofficial [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for the [Mapy.com REST API](https://api.mapy.com/) (`mapy.cz` / `mapy.com`).

This project has no affiliation with Mapy.com or its owners (Seznam.cz, a.s.). Please make sure you follow the [Mapy.com API Terms and Conditions](https://developer.mapy.com/en/terms-and-conditions/).

## Features & Tools

- **`maps_geocode`** – Geocode an address, place name, or point of interest (`query`, optional `lang`, `limit`, `type`, locality filters).
- **`maps_reverse_geocode`** – Reverse geocode coordinates (`lat`, `lon`) into structured address details.
- **`maps_route`** – Plan routes from `start` to `end` with optional `waypoints` and `avoid_toll`. Supported route types:
  - Driving: `car_fast`, `car_fast_traffic`, `car_short`
  - Cycling: `bike_road` (road bike), `bike_mountain` (mountain bike)
  - Walking / Hiking: `foot_fast`, `foot_hiking`

## Prerequisites – Mapy.com API Key

1. Sign in at [developer.mapy.com](https://developer.mapy.com/) and create a project to get a free API key.
2. Provide the key via the `API_KEY` environment variable (or in a local `.env` file).

## Usage with MCP Clients (Claude Desktop, Antigravity, Cursor)

### Option 1: Run directly from GitHub via `uvx`

```json
{
  "mcpServers": {
    "mapy-com": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/lukestrcz/unofficial_mapy_com_mcp",
        "unofficial-mapy-com-mcp"
      ],
      "env": {
        "API_KEY": "YOUR_MAPY_COM_API_KEY"
      }
    }
  }
}
```

### Option 2: Local virtual environment (`.venv`)

```bash
git clone https://github.com/lukestrcz/unofficial_mapy_com_mcp.git
cd unofficial_mapy_com_mcp
python3 -m venv .venv
.venv/bin/pip install -e .
```

```json
{
  "mcpServers": {
    "mapy-com": {
      "command": "/path/to/unofficial_mapy_com_mcp/.venv/bin/unofficial-mapy-com-mcp",
      "args": [],
      "env": {
        "API_KEY": "YOUR_MAPY_COM_API_KEY"
      }
    }
  }
}
```

## Credits & Fork Changes

This repository is a maintained fork of [07pepa/unofficial_mapy_com_mcp](https://github.com/07pepa/unofficial_mapy_com_mcp) by [@07pepa](https://github.com/07pepa).

Fixes included in this fork:
- **Standard `stdio` transport:** Switched `entry_point()` from legacy `run_sse_async()` to `run_stdio_async()` required by modern MCP hosts (Claude Desktop, Antigravity, Cursor).
- **Waypoint routing fix:** Updated `RouteRequest.waypoints` to use `RouteCoordinates` (`lon,lat` string serializer) instead of raw `Coordinates`, fixing Pydantic v2 serialization errors when routing via waypoints.
- **Packaging & dependencies:** Added missing `pydantic-settings` dependency and pinned `mcp<2.0.0` for compatibility with `fastmcp==2.14.1`.

## Developing

### Pre-requisites
- `just` (https://github.com/casey/just)
- `uv` (https://docs.astral.sh/uv/getting-started/installation/)
- `docker` (https://www.docker.com/)
- `act` (https://github.com/nektos/act)
