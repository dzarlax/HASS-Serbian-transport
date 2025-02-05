const registerPanel = () => {
  const ha = customElements.get('home-assistant');
  if (ha) {
    ha.registerPanel(
      "beograd_transport",
      {
        name: "Belgrade transport",
        icon: "mdi:bus",
        url_path: "beograd_transport",
        component_name: "city-dashboard-panel"  // Match the custom element name
      }
    );
  }
};

// Import panel component
import('./ha-panel.jsx')
  .then(() => {
    console.log('Panel component loaded');
    registerPanel();
  })
  .catch(err => {
    console.error('Failed to load panel:', err);
  });