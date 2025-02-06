# Serbian Transport Integration

Home Assistant integration for Serbian public transport information.

## Features
- Real-time bus arrival information
- Nearest stops discovery
- Custom Lovelace card

## Installation
1. Add this repository to HACS
2. Install "Serbian Transport" from HACS
3. Restart Home Assistant
4. Add integration through HA Settings -> Devices & Services

## Usage
After installation, you can use the custom card in your Lovelace UI:

```yaml
type: 'custom:transport-card'
entity: sensor.transport_stations_count
```

## Troubleshooting

If the custom card doesn't appear in your Lovelace dashboard, you may need to add it manually as a resource:

1. Go to Configuration -> Lovelace Dashboards -> Resources
2. Click the "+" button to add a new resource
3. Enter the following URL: `/hacsfiles/transport-card/transport-card.js`
4. Select "JavaScript Module" as the resource type
5. Click "Create"
6. Refresh your browser

## Repository

This integration is part of the [City Dashboard](https://github.com/dzarlax/city-dashboard) project.