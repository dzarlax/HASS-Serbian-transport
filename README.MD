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