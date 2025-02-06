import { LitElement, html, css } from 'https://cdn.jsdelivr.net/gh/lit/dist@2/core/lit-core.min.js';

export class TransportCard extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      _config: { state: true }
    };
  }

  static styles = css`
    :host {
      display: block;
    }
    ha-card {
      background: var(--card-background-color, var(--ha-card-background, white));
      border-radius: var(--ha-card-border-radius, 12px);
      box-shadow: var(--ha-card-box-shadow, 0 2px 4px rgba(0,0,0,0.1));
      color: var(--primary-text-color);
    }
    .card {
      padding: 16px;
    }
    .title {
      font-size: 1.4em;
      font-weight: 500;
      margin-bottom: 16px;
      color: var(--primary-text-color);
    }
    .stop-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .stop-item {
      background: var(--primary-background-color);
      border-radius: 8px;
      padding: 16px;
      border: 1px solid var(--divider-color, rgba(0,0,0,0.12));
    }
    .stop-name {
      font-size: 1.1em;
      font-weight: 500;
      margin-bottom: 8px;
      color: var(--primary-text-color);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .stop-id {
      font-size: 0.8em;
      color: var(--secondary-text-color);
      font-weight: normal;
    }
    .distance {
      font-size: 0.9em;
      color: var(--secondary-text-color);
      margin-bottom: 12px;
    }
    .transport-groups {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }
    .transport-group {
      background: var(--card-background-color);
      border-radius: 6px;
      padding: 12px;
      flex: 1;
      min-width: 200px;
    }
    .group-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      font-weight: 500;
    }
    .line-number {
      background: var(--primary-color);
      color: var(--primary-text-color);
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.9em;
    }
    .arrival-time {
      color: var(--primary-color);
      font-weight: 500;
    }
    .line-name {
      font-size: 0.9em;
      color: var(--secondary-text-color);
    }
      .arrivals-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }

    .arrival-time {
      color: var(--primary-color);
      font-weight: 500;
      cursor: help;
    }

    .transport-group {
      background: var(--card-background-color);
      border-radius: 6px;
      padding: 8px 12px;
      flex: 1;
    }
  `;

  setConfig(config) {
    if (!config.entity) throw new Error("Parameter 'entity' is required!");
    this._config = config;
  }

  groupVehiclesByLine(vehicles) {
    return vehicles?.reduce((groups, vehicle) => {
      const key = vehicle.lineNumber;
      if (!groups[key]) {
        groups[key] = {
          lineNumber: key,
          lineName: vehicle.lineName,
          arrivals: []
        };
      }
      groups[key].arrivals.push({
        seconds: vehicle.secondsLeft,
        stations: vehicle.stationsBetween
      });
      return groups;
    }, {}) ?? {};
  }
  
  renderArrivalTimes(arrivals) {
    const sortedArrivals = arrivals.sort((a, b) => a.seconds - b.seconds);
    return html`
      <div class="arrivals-list">
        ${sortedArrivals.map(({ seconds, stations }, index) => html`
          ${index > 0 ? ', ' : ''}
          <span class="arrival-time" title="${stations} stops away">
            ${Math.ceil(seconds/60)}${stations ? `(${stations})` : ''}
          </span>
        `)}
      </div>
    `;
  }
  
  renderStop(stop) {
    const groups = this.groupVehiclesByLine(stop.vehicles);
  
    return html`
      <div class="stop-item">
        <div class="stop-name">
          <ha-icon icon="mdi:bus-stop"></ha-icon>
          ${stop.name} 
          <span class="stop-id">#${stop.stopId}</span>
        </div>
        <div class="transport-groups">
          ${Object.values(groups).length > 0
            ? Object.values(groups).map(group => html`
                <div class="transport-group">
                  <div class="group-header">
                    <span class="line-number">${group.lineNumber}</span>
                    <span class="line-name">${group.lineName}</span>
                  </div>
                  ${this.renderArrivalTimes(group.arrivals)}
                </div>
              `)
            : html`<div class="no-data">No transport data available</div>`
          }
        </div>
      </div>
    `;
  }

  render() {
    if (!this._config || !this.hass) {
      return html`
        <ha-card>
          <div class="card">
            <div>Invalid configuration</div>
          </div>
        </ha-card>
      `;
    }

    const attr = this.hass.states[this._config.entity]?.attributes ?? {};
    const stops = attr.stations ?? [];

    return html`
      <ha-card>
        <div class="card">
          <div class="title">
            <ha-icon icon="mdi:bus"></ha-icon>
            ${this._config.title || 'Transport Stations'}
          </div>
          <div class="stop-list">
            ${stops.length > 0
              ? stops.map(stop => this.renderStop(stop))
              : html`<div>No stops available</div>`
            }
          </div>
        </div>
      </ha-card>
    `;
  }
}

customElements.define('transport-card', TransportCard);