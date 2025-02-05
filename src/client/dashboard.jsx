import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import { Bus } from 'lucide-react';
import { getHomeAssistantConfig } from './utils/homeAssistant';

const SERVER_IP = process.env.TRANSPORT_API_URL || "https://transport-api.dzarlax.dev";

const formatMinutes = (seconds) => {
  const minutes = Math.ceil(seconds / 60);
  return `${minutes}min`;
};

const BusStation = React.memo(({ name, distance, stopId, vehicles, city }) => {
  vehicles = vehicles || [];
  
  const groupedVehicles = useMemo(() => {
    return vehicles.reduce((acc, vehicle) => {
      const directionKey = `${stopId}-${vehicle.lineNumber}-${vehicle.lineName || 'unknown'}-${vehicle.stationName || ''}`;
      if (!acc[directionKey]) {
        acc[directionKey] = {
          lineNumber: vehicle.lineNumber,
          lineName: vehicle.lineName,
          stationName: vehicle.stationName,
          arrivals: [],
        };
      }
      acc[directionKey].arrivals.push({
        secondsLeft: vehicle.secondsLeft,
        stationsBetween: vehicle.stationsBetween,
      });
      return acc;
    }, {});
  }, [vehicles, stopId]);

  const sortedGroups = Object.values(groupedVehicles).sort(
    (a, b) => parseInt(a.lineNumber) - parseInt(b.lineNumber)
  );

  return (
    <div className="station-card" role="region" aria-label={`Bus station ${name}`}>
      <div className="station-header">
        <div className="station-title">
          <Bus className="station-icon" aria-hidden="true" />
          <span>{name}</span>
          <small>#{stopId}</small>
        </div>
        <span className="station-distance">{distance}</span>
      </div>
      {sortedGroups.length > 0 ? (
        <div className="station-lines">
          {sortedGroups.map((group, groupIndex) => (
            <div key={groupIndex} className="line-info">
              <div className="line-header">
                <span className="line-number">{group.lineNumber}</span>
                {group.lineName && <span className="line-name">{group.lineName}</span>}
                {group.stationName && <span className="line-destination">→ {group.stationName}</span>}
              </div>
              <div className="arrival-times">
                {group.arrivals
                  .sort((a, b) => a.secondsLeft - b.secondsLeft)
                  .map((arrival, arrivalIndex) => (
                    <span key={arrivalIndex} className="arrival-time">
                      {formatMinutes(arrival.secondsLeft)}
                      {arrival.stationsBetween > 0 && ` (${arrival.stationsBetween})`}
                    </span>
                  ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-arrivals">Нет прибытий</div>
      )}
    </div>
  );
});

const HaTransportCard = ({ config }) => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStations = useCallback(async () => {
    try {
      if (!config?.latitude || !config?.longitude) {
        throw new Error('Missing coordinates configuration');
      }
      const response = await fetch(
        `${SERVER_IP}/api/v1/nearest?lat=${config.latitude}&lon=${config.longitude}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setStations(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching stations:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [config]);

  useEffect(() => {
    let mounted = true;
    const fetchData = async () => {
      if (mounted) {
        await fetchStations();
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [fetchStations]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="transport-card">
      {stations.map((station) => (
        <BusStation key={station.id} {...station} />
      ))}
    </div>
  );
};

class CityDashboardPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.config = null;
    this._root = null;
  }

  async connectedCallback() {
    try {
      this.config = await getHomeAssistantConfig();
      const container = document.createElement('div');
      container.style.cssText = `
        height: 100%;
        padding: 16px;
        background: var(--primary-background-color);
        color: var(--primary-text-color);
      `;
      this.shadowRoot.appendChild(container);
      this._root = createRoot(container);
      this._root.render(<HaTransportCard config={this.config} />);
    } catch (error) {
      console.error('Failed to initialize dashboard:', error);
    }
  }

  disconnectedCallback() {
    if (this._root) {
      this._root.unmount();
      this._root = null;
    }
  }
}

// Register the custom element
customElements.define('city-dashboard-panel', CityDashboardPanel);

// Home Assistant panel registration
window.customPanels = window.customPanels || [];

const panelConfig = {
  component_name: "city-dashboard-panel",
  icon: "mdi:bus",
  name: "city_dashboard",
  title: "City Transport",
  url_path: "city-dashboard",
  require_admin: false
};

window.customPanels.push(panelConfig);

// Register with Home Assistant
if (window.loadCustomPanel) {
  window.loadCustomPanel(panelConfig);
}