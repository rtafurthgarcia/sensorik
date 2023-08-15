class TemperatureDisplay extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <div id="temperature">Loading...</div>
        `;

        this.websocket = new WebSocket(`ws://${location.host}/temperature`);
        this.websocket.onmessage = (event) => {
            console.log(event.data);
            this.shadowRoot.getElementById('temperature').innerText = `${event.data}°c`;
            this.shadowRoot.getElementById('temperature').classList.remove("error");
        };
        this.websocket.onerror = () => {
            this.shadowRoot.getElementById('temperature').innerText = "ERROR";
            this.shadowRoot.getElementById('temperature').classList.add("error");
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

        this.websocket = new WebSocket(`ws://${location.host}/liquid-height`);
        this.websocket.onmessage = (event) => {
            this.shadowRoot.getElementById('liquidHeight').innerText = `${event.data}%`;
            this.shadowRoot.getElementById('liquidHeight').classList.remove("error");
        };
        this.websocket.onerror = () => {
            this.shadowRoot.getElementById('liquidHeight').innerText = "ERROR";
            this.shadowRoot.getElementById('liquidHeight').classList.add("error");
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

        this.websocket = new WebSocket(`ws://${location.host}/video-feed`);
        this.websocket.onmessage = (event) => {
            this.shadowRoot.getElementById('videoFeed').srcObject = event.data;
            this.shadowRoot.getElementById('videoFeed').classList.remove("error");
        };
        this.websocket.onerror = () => {
            this.shadowRoot.getElementById('videoFeed').innerText = "ERROR";
            this.shadowRoot.getElementById('videoFeed').classList.add("error");
        };
    }
}
customElements.define('video-feed', VideoFeed);
