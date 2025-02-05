import React, { useState, useEffect, useCallback } from 'react';
import { createRoot } from 'react-dom/client';
import { Bus } from 'lucide-react';
import { getHomeAssistantConfig } from './utils/homeAssistant';

const SERVER_IP = "https://transport-api.dzarlax.dev";

const formatMinutes = (seconds) => {
  const minutes = Math.ceil(seconds / 60);
  return `${minutes}min`;
};

const BusStation = React.memo(({ name, distance, stopId, vehicles = [], city }) => {
  const groupedVehicles = vehicles.reduce((acc, vehicle) => {
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

  const sortedGroups = Object.values(groupedVehicles).sort(
    (a, b) => parseInt(a.lineNumber) - parseInt(b.lineNumber)
  );

  return (
    <div className="station-card">
      <div className="station-header">
        <div className="station-title">
          <Bus className="station-icon" />
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
                <span className="line-number">
                  {group.lineNumber}
                </span>
                {group.lineName && (
                  <span className="line-name">{group.lineName}</span>
                )}
                {group.stationName && (
                  <span className="line-destination">→ {group.stationName}</span>
                )}
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
      const { latitude, longitude } = config;
      const response = await fetch(
        `${SERVER_IP}/api/v1/nearest?lat=${latitude}&lon=${longitude}`
      );
      const data = await response.json();
      setStations(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [config]);

  useEffect(() => {
    fetchStations();
    const interval = setInterval(fetchStations, 30000);
    return () => clearInterval(interval);
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
  }

  async connectedCallback() {
    this.config = await getHomeAssistantConfig();
    const container = document.createElement('div');
    container.style.cssText = `
      height: 100%;
      padding: 16px;
      background: var(--primary-background-color);
      color: var(--primary-text-color);
    `;
    this.shadowRoot.appendChild(container);
    const root = createRoot(container);
    root.render(<HaTransportCard config={this.config} />);
  }
}

if (!customElements.get('city-dashboard-panel')) {
  customElements.define('city-dashboard-panel', CityDashboardPanel);
}

const registerPanel = () => {
  const ha = customElements.get('home-assistant');
  if (ha) {
    ha.registerPanel("beograd_transport", {
      name: "Belgrade transport",
      icon: "mdi:bus",
      url_path: "beograd_transport",
      component_name: "city-dashboard-panel"
    });
  }
};

registerPanel();