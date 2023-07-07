class TemperatureDisplay extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
        <div id="temperature">Loading...</div>
    `;

        this.websocket = new WebSocket('ws://temperature');
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.shadowRoot.getElementById('temperature').innerText = data.temperature;
        };
    }
}
customElements.define('temperature-display', TemperatureDisplay);

class LiquidHeight extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
        <div id="liquidHeight">Loading...</div>
      `;

        this.websocket = new WebSocket('ws://liquid-height');
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.shadowRoot.getElementById('liquidHeight').innerText = data.height;
        };
    }
}
customElements.define('liquid-height', LiquidHeight);

class VideoFeed extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
        <video id="videoFeed" autoplay></video>
      `;

        this.websocket = new WebSocket('ws://video-feed');
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.shadowRoot.getElementById('videoFeed').srcObject = data.stream;
        };
    }
}
customElements.define('video-feed', VideoFeed);
