import { LitElement, html, css } from 'https://cdn.jsdelivr.net/gh/lit/dist@2/core/lit-core.min.js';

// Transport Card v2.2.0 - Simplified version with animations, progress bars and visual UI configuration
export class TransportCard extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      _config: { state: true },
      _expanded: { state: true },
      _showNextDeparture: { state: true }
    };
  }

  constructor() {
    super();
    this._expanded = false;
    this._showNextDeparture = true;
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
      overflow: hidden;
    }
    
    /* Header styles */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    
    .controls {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    
    .expand-button {
      background: var(--secondary-background-color);
      border: none;
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 0.9em;
      cursor: pointer;
      color: var(--primary-text-color);
      transition: background-color 0.2s;
    }
    
    .expand-button:hover {
      background: var(--divider-color);
    }

    /* Animations and transitions */
    .transport-group {
      transition: all 0.3s ease;
    }

    .transport-group:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .stop-container {
      transition: all 0.3s ease;
    }

    .stop-container:hover {
      background: var(--secondary-background-color);
    }

    .arrival-time {
      transition: all 0.2s ease;
    }

    .arrival-time:hover {
      transform: scale(1.05);
    }

    /* Progress bars for arrival times */
    .arrival-progress {
      width: 100%;
      height: 3px;
      background: var(--divider-color);
      border-radius: 2px;
      overflow: hidden;
      margin-top: 2px;
    }

    .arrival-progress-fill {
      height: 100%;
      transition: width 1s ease;
      border-radius: 2px;
    }

    .arrival-progress-fill.urgent {
      background: linear-gradient(90deg, var(--error-color), var(--warning-color));
    }

    .arrival-progress-fill.soon {
      background: linear-gradient(90deg, var(--warning-color), var(--info-color));
    }

    .arrival-progress-fill.normal {
      background: linear-gradient(90deg, var(--success-color), var(--primary-color));
    }

    .arrival-progress-fill.late {
      background: linear-gradient(90deg, var(--primary-color), var(--secondary-text-color));
    }

    /* Arrival container */
    .arrival-container {
      display: flex;
      flex-direction: column;
      gap: 2px;
      margin-right: 8px;
      margin-bottom: 4px;
    }




    
    /* Next departure section */
    .next-departure {
      background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
      color: var(--text-primary-color);
      padding: 16px;
      margin: -16px -16px 16px -16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .next-departure-time {
      font-size: 1.5em;
      font-weight: bold;
    }
    
    .next-departure-info {
      text-align: right;
      font-size: 0.9em;
      opacity: 0.9;
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
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 12px;
      padding: 8px;
    }
    .stop-item {
      background: var(--card-background-color);
      border-radius: 8px;
      padding: 12px;
      border: 1px solid var(--divider-color);
    }
    .stop-name {
      font-size: 1em;
      font-weight: 500;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .stop-id {
      font-size: 0.8em;
      color: var(--secondary-text-color);
      margin-left: 4px;
    }
    .distance {
      font-size: 0.9em;
      color: var(--secondary-text-color);
      margin-bottom: 12px;
    }
    .transport-groups {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 8px;
    }

    .transport-group {
      background: var(--card-background-color);
      border-radius: 6px;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 4px;
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
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.9em;
      font-weight: 500;
    }
    .arrival-times {
      color: var(--primary-color);
      font-size: 0.9em;
    }
    .line-name {
      font-size: 0.9em;
      color: var(--secondary-text-color);
    }
    .arrivals-list {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .arrival-time {
      font-size: 0.9em;
      white-space: nowrap;
      padding: 2px 6px;
      border-radius: 4px;
      margin: 2px 0;
      display: inline-block;
    }
    
    /* Color coding for arrival times */
    .arrival-time.urgent {
      background: var(--error-color, #f44336);
      color: white;
    }
    
    .arrival-time.soon {
      background: var(--warning-color, #ff9800);
      color: white;
    }
    
    .arrival-time.normal {
      background: var(--success-color, #4caf50);
      color: white;
    }
    
    .arrival-time.late {
      background: var(--info-color, #2196f3);
      color: white;
    }

    .transport-group {
      background: var(--card-background-color);
      border-radius: 6px;
      padding: 8px 12px;
      flex: 1;
      border: 1px solid var(--divider-color);
      transition: box-shadow 0.2s;
    }
    
    .transport-group:hover {
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Station status indicators */
    .station-status {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      margin-right: 8px;
    }
    
    .station-status.online {
      background: var(--success-color, #4caf50);
    }
    
    .station-status.offline {
      background: var(--error-color, #f44336);
    }
    
    .station-status.unknown {
      background: var(--secondary-text-color);
    }
    
    /* Compact view styles */
    .compact .stop-list {
      grid-template-columns: 1fr;
      gap: 8px;
    }
    
    .compact .transport-groups {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 4px;
    }
    
    .compact .transport-group {
      padding: 6px 8px;
    }
    
    /* Loading state */
    .loading {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 32px;
      color: var(--secondary-text-color);
    }
    
    .loading ha-icon {
      animation: spin 1s linear infinite;
      margin-right: 8px;
    }
    
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    
    /* Additional styles for new elements */
    .station-count {
      font-size: 0.9em;
      color: var(--secondary-text-color);
      margin-left: 8px;
    }
    
    .no-data {
      text-align: center;
      padding: 32px;
      color: var(--secondary-text-color);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    
    .no-data ha-icon {
      font-size: 2em;
      opacity: 0.5;
    }
    
    .last-updated {
      text-align: center;
      font-size: 0.8em;
      color: var(--secondary-text-color);
      margin-top: 16px;
      padding-top: 8px;
      border-top: 1px solid var(--divider-color);
    }
  `;

  setConfig(config) {
    if (!config.entity) throw new Error("Parameter 'entity' is required!");
    this._config = {
      entity: config.entity,
      title: config.title || 'Transport Stations',
      show_next_departure: config.show_next_departure !== false,
      compact_view: config.compact_view || false,
      max_stations: config.max_stations || 10,
      refresh_interval: config.refresh_interval || 30,
      ...config
    };
    this._showNextDeparture = this._config.show_next_departure;
  }

  // Get arrival time color class based on minutes
  getArrivalTimeClass(minutes) {
    if (minutes <= 2) return 'urgent';
    if (minutes <= 5) return 'soon';
    if (minutes <= 15) return 'normal';
    return 'late';
  }



  // Get next departure time from all stations
  getNextDeparture(stations) {
    let minTime = null;
    let nextInfo = null;
    
    stations.forEach(station => {
      const vehicles = station.vehicles || [];
      vehicles.forEach(vehicle => {
        const seconds = vehicle.secondsLeft;
        if (seconds != null) {
          const minutes = Math.ceil(seconds / 60);
          if (minTime === null || minutes < minTime) {
            minTime = minutes;
            nextInfo = {
              minutes,
              line: vehicle.lineNumber,
              destination: vehicle.lineName,
              station: station.name
            };
          }
        }
      });
    });
    
    return nextInfo;
  }

  // Toggle expanded view
  toggleExpanded() {
    this._expanded = !this._expanded;
  }




  // Get progress bar width for arrival time
  getProgressBarWidth(minutes) {
    const maxMinutes = 30; // Max time for full bar
    const width = Math.max(0, Math.min(100, ((maxMinutes - minutes) / maxMinutes) * 100));
    return width;
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
      ${sortedArrivals.map(({ seconds, stations }) => {
        const minutes = Math.ceil(seconds / 60);
        const timeClass = this.getArrivalTimeClass(minutes);
        return html`
          <span class="arrival-time ${timeClass}" title="${stations} stops away">
            ${minutes} min${stations ? ` (${stations})` : ''}
          </span>
        `;
      })}
      </div>
    `;
  }

  // Render next departure section
  renderNextDeparture(nextDeparture) {
    if (!nextDeparture || !this._showNextDeparture) return '';
    
    return html`
      <div class="next-departure">
        <div>
          <div class="next-departure-time">${nextDeparture.minutes} min</div>
          <div>Next Departure</div>
        </div>
        <div class="next-departure-info">
          <div>${nextDeparture.line} - ${nextDeparture.destination}</div>
          <div>${nextDeparture.station}</div>
        </div>
      </div>
    `;
  }

  // Render controls
  renderControls() {
    return html`
      <div class="controls">
        <button 
          class="expand-button"
          @click=${this.toggleExpanded}
          title="${this._expanded ? 'Compact view' : 'Expanded view'}"
        >
          <ha-icon icon="${this._expanded ? 'mdi:chevron-up' : 'mdi:chevron-down'}"></ha-icon>
        </button>
      </div>
    `;
  }

  renderStop(stop) {
    const groups = this.groupVehiclesByLine(stop.vehicles);
    const hasData = stop.vehicles && stop.vehicles.length > 0;
    const statusClass = hasData ? 'online' : 'unknown';

    return html`
      <div class="stop-item">
        <div class="stop-name">
          <span class="station-status ${statusClass}"></span>
          <ha-icon icon="mdi:bus-stop" size="16"></ha-icon>
          ${stop.name} 
          <span class="stop-id">#${stop.stopId}</span>
        </div>
        ${stop.distance ? html`
          <div class="distance">📍 ${Math.round(stop.distance)}m</div>
        ` : ''}
        <div class="transport-groups">
          ${Object.values(groups).length > 0 ? Object.values(groups).map(group => html`
            <div class="transport-group">
              <div class="group-header">
                <span class="line-number">${group.lineNumber}</span>
                <span class="line-name">${group.lineName}</span>
              </div>
              <div class="arrivals-list">
                ${group.arrivals
                  .sort((a, b) => a.seconds - b.seconds)
                  .slice(0, this._expanded ? 5 : 3)
                  .map(({ seconds, stations }) => {
                    const minutes = Math.ceil(seconds / 60);
                    const timeClass = this.getArrivalTimeClass(minutes);
                    const progressWidth = this.getProgressBarWidth(minutes);
                    
                    return html`
                      <div class="arrival-container">
                        <span class="arrival-time ${timeClass}" title="${stations} stops">
                          ${minutes} min${stations ? ` (${stations})` : ''}
                        </span>
                        <div class="arrival-progress">
                          <div class="arrival-progress-fill ${timeClass}" style="width: ${progressWidth}%"></div>
                        </div>
                      </div>
                    `;
                  })}
              </div>
            </div>
          `) : html`
            <div class="no-data">No transport data</div>
          `}
        </div>
      </div>
    `;
  }

  render() {
    if (!this._config || !this.hass) {
      return html`
        <ha-card>
          <div class="card">
            <div class="loading">
              <ha-icon icon="mdi:cog"></ha-icon>
              Invalid configuration
            </div>
          </div>
        </ha-card>
      `;
    }

    const entityState = this.hass.states[this._config.entity];
    if (!entityState) {
      return html`
        <ha-card>
          <div class="card">
            <div class="loading">
              <ha-icon icon="mdi:alert"></ha-icon>
              Entity not found: ${this._config.entity}
            </div>
          </div>
        </ha-card>
      `;
    }

    const attr = entityState.attributes || {};
    const allStops = attr.stations || [];
    const isLoading = entityState.state === 'unavailable';
    
    if (isLoading) {
      return html`
        <ha-card>
          <div class="card">
            <div class="loading">
              <ha-icon icon="mdi:loading"></ha-icon>
              Loading transport data...
            </div>
          </div>
        </ha-card>
      `;
    }

    // Apply limit only
    const displayStops = allStops.slice(0, this._config.max_stations);
    const nextDeparture = this.getNextDeparture(allStops);
    
    const cardClass = this._config.compact_view || !this._expanded ? 'compact' : '';

    return html`
      <ha-card>
        ${this.renderNextDeparture(nextDeparture)}
        <div class="card ${cardClass}">
          <div class="header">
            <div class="title">
              <ha-icon icon="mdi:bus"></ha-icon>
              ${this._config.title}
              <span class="station-count">(${displayStops.length})</span>
            </div>
            ${this.renderControls()}
          </div>
          
          ${displayStops.length > 0 ? html`
            <div class="stop-list">
              ${displayStops.map(stop => this.renderStop(stop))}
            </div>
          ` : html`
            <div class="no-data">
              <ha-icon icon="mdi:bus-stop"></ha-icon>
              <div>No stops found</div>
            </div>
          `}
          
          ${attr.last_update_success !== undefined ? html`
            <div class="last-updated">
              Status: ${attr.last_update_success ? 'Updated successfully' : 'Update failed'}
            </div>
          ` : ''}
        </div>
      </ha-card>
    `;
  }

  static getConfigElement() {
    return document.createElement('transport-card-editor');
  }

  static getStubConfig() {
    return {
      entity: '',
      title: 'Serbian Transport',
      show_next_departure: true,
      compact_view: false,
      max_stations: 10,
      refresh_interval: 30
    };
  }
}

// Card Editor for UI Configuration
class TransportCardEditor extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      _config: { state: true },
      _entities: { state: true }
    };
  }

  constructor() {
    super();
    this._entities = [];
  }

  static styles = css`
    .card-config {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      padding: 16px;
    }

    .config-section {
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
    }

    .config-row {
      display: grid;
      grid-template-columns: 150px 1fr;
      gap: 12px;
      align-items: center;
      min-height: 40px;
    }

    .config-label {
      font-weight: 500;
      color: var(--primary-text-color);
    }

    .config-input {
      width: 100%;
    }

    ha-select,
    ha-textfield {
      width: 100%;
    }

    ha-switch {
      --mdc-theme-secondary: var(--switch-checked-color);
    }

    .section-header {
      font-size: 1.1em;
      font-weight: 600;
      color: var(--primary-color);
      margin-bottom: 8px;
      padding-bottom: 4px;
      border-bottom: 1px solid var(--divider-color);
    }

    .help-text {
      font-size: 0.9em;
      color: var(--secondary-text-color);
      margin-top: 4px;
    }
  `;

  setConfig(config) {
    this._config = { ...config };
  }

  updated(changedProperties) {
    if (changedProperties.has('hass') && this.hass) {
      this._entities = Object.keys(this.hass.states)
        .filter(entityId => entityId.startsWith('sensor.'))
        .sort();
    }
  }

  _valueChanged(ev) {
    const target = ev.target;
    const configKey = target.configKey;
    
    if (!configKey) return;

    let value = target.value;
    
    // Handle different input types
    if (target.type === 'number') {
      value = parseInt(value) || 0;
    } else if (target.hasAttribute('checked')) {
      value = target.checked;
    }

    // Create new config with updated value
    const newConfig = {
      ...this._config,
      [configKey]: value
    };

    // Fire config changed event
    this.dispatchEvent(new CustomEvent('config-changed', {
      detail: { config: newConfig },
      bubbles: true,
      composed: true
    }));
  }

  render() {
    if (!this.hass || !this._config) {
      return html`<div>Loading...</div>`;
    }

    return html`
      <div class="card-config">
        <!-- Entity Selection -->
        <div class="config-section">
          <div class="section-header">Entity Configuration</div>
          
          <div class="config-row">
            <label class="config-label">Entity</label>
            <ha-select
              .configKey=${'entity'}
              .value=${this._config.entity || ''}
              @selected=${this._valueChanged}
              @closed=${(ev) => ev.stopPropagation()}
            >
              ${this._entities.map(entity => html`
                <mwc-list-item .value=${entity}>
                  ${entity}
                </mwc-list-item>
              `)}
            </ha-select>
          </div>
          <div class="help-text">Select the Serbian Transport sensor entity</div>
        </div>

        <!-- Display Options -->
        <div class="config-section">
          <div class="section-header">Display Options</div>
          
          <div class="config-row">
            <label class="config-label">Title</label>
            <ha-textfield
              .configKey=${'title'}
              .value=${this._config.title || 'Serbian Transport'}
              @input=${this._valueChanged}
            ></ha-textfield>
          </div>

          <div class="config-row">
            <label class="config-label">Max Stations</label>
            <ha-textfield
              type="number"
              min="1"
              max="50"
              .configKey=${'max_stations'}
              .value=${this._config.max_stations || 10}
              @input=${this._valueChanged}
            ></ha-textfield>
          </div>
          <div class="help-text">Maximum number of stations to display (1-50)</div>

          <div class="config-row">
            <label class="config-label">Refresh Interval</label>
            <ha-textfield
              type="number"
              min="10"
              max="300"
              .configKey=${'refresh_interval'}
              .value=${this._config.refresh_interval || 30}
              @input=${this._valueChanged}
            ></ha-textfield>
          </div>
          <div class="help-text">Data refresh interval in seconds (10-300)</div>
        </div>

        <!-- Features -->
        <div class="config-section">
          <div class="section-header">Features</div>
          
          <div class="config-row">
            <label class="config-label">Show Next Departure</label>
            <ha-switch
              .configKey=${'show_next_departure'}
              .checked=${this._config.show_next_departure !== false}
              @change=${this._valueChanged}
            ></ha-switch>
          </div>
          <div class="help-text">Display the next departure information at the top</div>

          <div class="config-row">
            <label class="config-label">Compact View</label>
            <ha-switch
              .configKey=${'compact_view'}
              .checked=${this._config.compact_view === true}
              @change=${this._valueChanged}
            ></ha-switch>
          </div>
          <div class="help-text">Use compact layout by default</div>
        </div>
      </div>
    `;
  }
}

customElements.define('transport-card', TransportCard);
customElements.define('transport-card-editor', TransportCardEditor);

// Register the card info for Home Assistant UI
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'transport-card',
  name: 'Serbian Transport Card',
  description: 'Display Serbian public transport information with real-time arrivals',
  preview: false,
  documentationURL: 'https://github.com/dzarlax/HASS-Serbian-transport',
});