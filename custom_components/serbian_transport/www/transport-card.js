// Use CDN imports for Lit
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
    .card {
      padding: 16px;
    }
    .title {
      font-size: 1.2em;
      margin-bottom: 8px;
    }
    .stop-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stop-item {
      background: var(--ha-card-background, white);
      border-radius: 8px;
      padding: 8px;
      box-shadow: var(--ha-card-box-shadow, none);
    }
    .stop-name {
      font-weight: bold;
    }
    .small-text {
      font-size: 0.9em;
      color: var(--secondary-text-color);
    }
  `;

  setConfig(config) {
    if (!config.entity) {
      throw new Error("Parameter 'entity' is required!");
    }
    this._config = config;
  }

  get entityState() {
    if (!this._config || !this.hass) return null;
    return this.hass.states[this._config.entity];
  }

  render() {
    if (!this._config || !this.entityState) {
      return html`
        <ha-card>
          <div class="card">
            <div>No data or invalid configuration</div>
          </div>
        </ha-card>
      `;
    }

    const attr = this.entityState.attributes;
    const stops = attr.stations || [];

    return html`
      <ha-card>
        <div class="card">
          <div class="title">
            ${this._config.title || 'Transport Stations'}
          </div>
          <div class="stop-list">
            ${stops.length > 0
              ? stops.map((stop) => this.renderStop(stop))
              : html`<div>No stops available</div>`
            }
          </div>
        </div>
      </ha-card>
    `;
  }

  renderStop(stop) {
    return html`
      <div class="stop-item">
        <div class="stop-name">${stop.name} (#${stop.stopId})</div>
        <div class="small-text">${stop.distance}</div>
        ${stop.vehicles && stop.vehicles.length
          ? html`
              <ul>
                ${stop.vehicles.map((v) => html`
                  <li>
                    Line: ${v.lineNumber} –
                    Arriving in ~${Math.ceil(v.secondsLeft/60)} min
                  </li>
                `)}
              </ul>
            `
          : html`<div class="small-text">No transport data available</div>`}
      </div>
    `;
  }
}

// Register the element
customElements.define('transport-card', TransportCard);

console.info('Transport card has been registered');