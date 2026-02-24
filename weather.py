from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("weather")

# CONSTANTS
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any]:
	"""Make a request to the NWS API with proper error handling."""
	headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
	async with httpx.AsyncClient() as client:
		try: 
			response = await client.get(url, headers=headers, timeout=30)
			response.raise_for_status()
			return response.json()		
		except Exception as e:
			return None

def format_alert(feature: dict) -> str:
	"""Format an alert feature into a readable string."""
	props = feature.get("properties", {})
	return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available.')}
Instruction: {props.get('instruction', 'No specific instructions provided.')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
	"""Get active weather alerts for a US state.

	Args:
		state (str): two-letter US state code (e.g., 'CA' for California).
	"""
	url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
	data = await make_nws_request(url)
	if not data or "features" not in data:
		return f"Unable to fetch alerts or no alerts found for {state}."
	
	if not data["features"]:
		return f"No active alerts found for {state}."
	
	alerts = [format_alert(feature) for feature in data["features"]]
	return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
	"""Get the weather forecast for a location.

	Args:
		latitude: Latitude of the location.
		longitude: Longitude of the location.
	"""
	# First get the forecast grid endpoint
	points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
	points_data = await make_nws_request(points_url)

	if not points_data:
		return "Unable to fetch forecast data for this location."

	# Get the forecast URL from the points response
	forecast_url = points_data.get("properties", {}).get("forecast")
	forecast_data = await make_nws_request(forecast_url)

	if not forecast_data:
		return "Unable to fetch detailed forecast."

	# Format the periods into a readable forecast
	periods = forecast_data.get("properties", {}).get("periods", [])
	forecasts = []
	for period in periods[:5]: # only show next 5 periods
		forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
		forecasts.append(forecast)

	return "\n---\n".join(forecasts)

def main():
	# Initialize the MCP server and run it
	mcp.run(transport="stdio")

if __name__ == "__main__":
	main()