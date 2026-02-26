#!/usr/bin/env python3
"""
PWA Engine for GNOME Web - Python WebExtension
Manages PWA installation, service workers, and offline capabilities
"""

import json
import mimetypes
import os
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import webbrowser
import tempfile
import shutil

class PWAEngine:
    def __init__(self, extension_dir="pwa_engine"):
        self.extension_dir = Path(extension_dir)
        self.extension_dir.mkdir(exist_ok=True)
        
        # PWA metadata
        self.pwa_data = {
            "name": "PWA Engine Demo",
            "short_name": "PWAEngine",
            "description": "Python-powered PWA Engine for GNOME Web",
            "start_url": "/pwa/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#2196F3",
            "icons": [
                {"src": "data:image/svg+xml;base64,...", "sizes": "192x192", "type": "image/png"}
            ]
        }
        
        self.server_port = 8080
        self.server_thread = None
        self.setup_extension()
    
    def setup_extension(self):
        """Create GNOME WebExtension structure"""
        
        # manifest.json
        manifest = {
            "manifest_version": 2,
            "name": "PWA Engine",
            "version": "1.0",
            "description": "Progressive Web App Engine",
            "permissions": ["activeTab", "storage", "tabs"],
            
            "browser_action": {
                "default_popup": "popup.html",
                "default_title": "PWA Engine"
            },
            
            "background": {
                "scripts": ["background.js"],
                "persistent": False
            },
            
            "content_scripts": [{
                "matches": ["<all_urls>"],
                "js": ["content.js"],
                "css": ["pwa.css"]
            }],
            
            "web_accessible_resources": [
                "pwa.html", "sw.js", "manifest.json", "pwa.css"
            ]
        }
        
        # Write extension files
        files = {
            "manifest.json": json.dumps(manifest, indent=2),
            "popup.html": self._popup_html(),
            "background.js": self._background_js(),
            "content.js": self._content_js(),
            "pwa.html": self._pwa_html(),
            "sw.js": self._service_worker_js(),
            "pwa.css": self._pwa_css(),
            "pwa.js": self._pwa_js()
        }
        
        for filename, content in files.items():
            (self.extension_dir / filename).write_text(content)
    
    def _popup_html(self):
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="pwa.css">
</head>
<body>
    <div class="pwa-popup">
        <h3>🧑‍💻 PWA Engine</h3>
        <button id="install-btn">Install PWA</button>
        <button id="manage-btn">Manage PWAs</button>
        <div id="status"></div>
    </div>
    <script src="pwa.js"></script>
</body>
</html>'''
    
    def _background_js(self):
        return '''// Background script for PWA management
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "installPWA") {
        chrome.tabs.create({url: chrome.runtime.getURL("pwa.html")});
    }
    sendResponse({success: true});
});'''
    
    def _content_js(self):
        return '''// Content script - injects PWA detection
(function() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        console.log("PWA Engine: Service Worker support detected");
        window.postMessage({type: "PWA_ENGINE_READY"}, "*");
    }
    
    // Auto-detect PWA candidates
    if (document.querySelector('link[rel="manifest"]')) {
        window.postMessage({type: "PWA_DETECTED", url: window.location.href}, "*");
    }
})();'''
    
    def _pwa_html(self):
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PWA Engine</title>
    <link rel="manifest" href="manifest.json">
    <link rel="stylesheet" href="pwa.css">
</head>
<body>
    <div class="app-container">
        <header>
            <h1>🚀 PWA Engine</h1>
            <p>Python-powered Progressive Web App</p>
        </header>
        
        <main>
            <div class="stats">
                <div class="stat-card">
                    <span>Status</span>
                    <span id="status">Online</span>
                </div>
                <div class="stat-card">
                    <span>Storage</span>
                    <span id="storage">--</span>
                </div>
            </div>
            
            <div class="actions">
                <button id="cache-btn">Cache Resources</button>
                <button id="offline-btn">Test Offline</button>
            </div>
        </main>
    </div>
    
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('./sw.js')
                .then(reg => console.log('SW registered', reg))
                .catch(err => console.log('SW failed', err));
        }
    </script>
    <script src="pwa.js"></script>
</body>
</html>'''
    
    def _service_worker_js(self):
        return '''// Service Worker for PWA Engine
const CACHE_NAME = 'pwa-engine-v1';
const urlsToCache = [
    './',
    './pwa.html',
    './pwa.css',
    './pwa.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});'''
    
    def _pwa_css(self):
        return '''/* PWA Engine Styles */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: white;
}

.app-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}

header h1 { font-size: 2.5em; margin-bottom: 10px; }
header p { opacity: 0.9; font-size: 1.1em; }

.stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.stat-card span:first-child { font-size: 0.9em; opacity: 0.8; display: block; }
.stat-card span:last-child { font-size: 1.8em; font-weight: bold; }

.actions button {
    display: block;
    width: 100%;
    padding: 15px;
    margin: 10px 0;
    background: rgba(255,255,255,0.2);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1em;
    cursor: pointer;
    backdrop-filter: blur(10px);
    transition: all 0.3s;
}

.actions button:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }

.pwa-popup {
    width: 300px;
    padding: 20px;
    background: white;
    border-radius: 12px;
}

.pwa-popup h3 { margin-bottom: 15px; color: #333; }
.pwa-popup button { 
    width: 100%; 
    padding: 10px; 
    margin: 5px 0; 
    border: none; 
    background: #2196F3; 
    color: white; 
    border-radius: 6px;
    cursor: pointer;
}'''
    
    def _pwa_js(self):
        return '''// PWA Engine JavaScript
document.addEventListener('DOMContentLoaded', () => {
    // Update storage info
    if (navigator.storage && navigator.storage.estimate) {
        navigator.storage.estimate().then(estimate => {
            document.getElementById('storage').textContent = 
                (estimate.usage/1024/1024).toFixed(1) + 'MB';
        });
    }
    
    // Cache button
    document.getElementById('cache-btn')?.addEventListener('click', () => {
        if ('caches' in window) {
            caches.open('pwa-engine-v1').then(cache => {
                cache.addAll(['./pwa.html', './pwa.css']);
                document.getElementById('status').textContent = '✅ Cached!';
            });
        }
    });
    
    // Offline test
    document.getElementById('offline-btn')?.addEventListener('click', () => {
        document.getElementById('status').textContent = '🧪 Testing offline...';
    });
    
    // Install button (popup)
    document.getElementById('install-btn')?.addEventListener('click', () => {
        if (window.deferredPrompt) {
            window.deferredPrompt.prompt();
            window.deferredPrompt.userChoice.then(choice => {
                if (choice.outcome === 'accepted') {
                    document.getElementById('status').textContent = '✅ Installed!';
                }
            });
        }
    });
});

// Handle PWA install prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
});'''
    
    def start_dev_server(self):
        """Start local dev server for testing"""
        os.chdir(self.extension_dir)
        webbrowser.open(f'http://localhost:{self.server_port}')
        
        class PWAServer(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/manifest.json':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(self.server.pwa_data, indent=2).encode())
                else:
                    super().do_GET()
        
        PWAServer.server = self
        self.server_thread = threading.Thread(
            target=HTTPServer(('localhost', self.server_port), PWAServer).serve_forever
        )
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"🌐 Dev server running at http://localhost:{self.server_port}")
        print(f"📁 Extension ready in: {self.extension_dir.absolute()}")
    
    def install_instructions(self):
        print("
" + "="*60)
        print("🚀 INSTALL INSTRUCTIONS")
        print("="*60)
        print("1. Open GNOME Web (Epiphany)")
        print("2. Go to chrome://extensions/")
        print("3. Enable 'Developer mode'")
        print("4. Click 'Load unpacked' → select this folder")
        print("5. Click the PWA Engine icon → 'Install PWA'")
        print("="*60)

def main():
    engine = PWAEngine()
    engine.start_dev_server()
    engine.install_instructions()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("
👋 PWA Engine stopped")

if __name__ == "__main__":
    main()
