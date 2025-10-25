#!/usr/bin/env python3
"""
🌟 GLYPHWHEEL FORECAST ENGINE - WORKING PROTOTYPE 🌟

INSTRUCTIONS:
1. Double-click this file to run it
2. Browser opens automatically to http://localhost:8080
3. Press Ctrl+C to stop

Your original Glyphwheel system with a modern web UI!
"""

import json
import random
import math
import time
import webbrowser
from typing import Dict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
import socketserver

class Glyph:
    def __init__(self, name: str, initial_gsi: float = 0.5, glyph_type: str = "standard"):
        self.name = name
        self.glyph_type = glyph_type
        self.gsi = initial_gsi
        self.history = [initial_gsi]
        self.connections = []
        self.adaptation_rate = 0.1
        
    def process_stress(self, stress_level: float) -> float:
        adaptation = stress_level * self.adaptation_rate
        if stress_level > 0.3:
            self.gsi = min(1.0, self.gsi + adaptation)
        else:
            self.gsi = max(0.0, self.gsi - adaptation)
        self.history.append(self.gsi)
        return self.gsi
        
    def form_connection(self, other_glyph: 'Glyph') -> float:
        connection_strength = (self.gsi + other_glyph.gsi) / 2.0
        if connection_strength > 0.6:
            self.connections.append(other_glyph.name)
            return connection_strength
        return 0.0
    
    def to_dict(self):
        return {
            "name": self.name,
            "gsi": self.gsi,
            "type": self.glyph_type,
            "connections": len(self.connections),
            "history_length": len(self.history)
        }

class GlyphwheelEngine:
    def __init__(self):
        self.glyphs: Dict[str, Glyph] = {}
        self.recursive_depth = 0
        self.entropy_limit = 0.15
        self.mandatory_recovery_time = 10
        self.last_stress_test_time = 0
        self.log_entries = []
        
        self._initialize_anchors()
        self._initialize_consent_glyph()
        self.log("System initialized successfully", "success")
        
    def log(self, message: str, level: str = "info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_entries.append({
            "timestamp": timestamp,
            "message": message,
            "level": level
        })
        if len(self.log_entries) > 100:
            self.log_entries.pop(0)
        
    def _initialize_anchors(self):
        anchors = {"RootVerse": 0.87, "Aegis-Σ": 0.85, "CoreStability": 0.82}
        for name, gsi in anchors.items():
            self.glyphs[name] = Glyph(name, gsi, "anchor")
        self.log("Anchor glyphs initialized", "success")

    def _initialize_consent_glyph(self):
        self.glyphs["ConsentGlyph"] = Glyph("ConsentGlyph", 0.95, "consent")
        self.log("Consent glyph activated", "success")

    def request_consent(self, operation_type: str) -> bool:
        current_entropy = self.calculate_entropy()
        if current_entropy > self.entropy_limit:
            self.log(f"CONSENT DENIED: Entropy too high ({current_entropy:.3f})", "warning")
            return False
        
        cycles_since_last = time.time() - self.last_stress_test_time
        if cycles_since_last < self.mandatory_recovery_time:
            remaining = self.mandatory_recovery_time - cycles_since_last
            self.log(f"CONSENT DENIED: Recovery period ({remaining:.1f}s remaining)", "warning")
            return False
            
        self.log(f"CONSENT GRANTED for {operation_type}", "success")
        return True

    def add_glyph(self, name: str, initial_gsi: float = None, glyph_type: str = "dynamic"):
        if initial_gsi is None:
            initial_gsi = random.uniform(0.3, 0.7)
        
        if name in self.glyphs:
            self.log(f"Glyph {name} already exists", "warning")
            return False
            
        self.glyphs[name] = Glyph(name, initial_gsi, glyph_type)
        self.log(f"Added glyph: {name} (GSI: {initial_gsi:.3f})", "success")
        return True
        
    def calculate_system_coherence(self) -> float:
        if not self.glyphs:
            return 0.0
        total_gsi = sum(glyph.gsi for glyph in self.glyphs.values())
        avg_gsi = total_gsi / len(self.glyphs)
        total_connections = sum(len(glyph.connections) for glyph in self.glyphs.values())
        connection_factor = min(1.0, total_connections / (len(self.glyphs) * 2))
        return min(1.0, (avg_gsi * 0.7) + (connection_factor * 0.3))
        
    def calculate_entropy(self) -> float:
        if not self.glyphs:
            return 1.0
        gsi_values = [glyph.gsi for glyph in self.glyphs.values()]
        mean_gsi = sum(gsi_values) / len(gsi_values)
        variance = sum((gsi - mean_gsi) ** 2 for gsi in gsi_values) / len(gsi_values)
        return min(1.0, math.sqrt(variance) * 2)

    def run_stress_test(self, stress_intensity: float = 0.5, duration: int = 100) -> Dict:
        if not self.request_consent("stress_test"):
            return {"status": "aborted", "reason": "consent_denied"}

        self.log(f"Starting stress test (intensity: {stress_intensity}, duration: {duration})", "warning")
        initial_coherence = self.calculate_system_coherence()
        initial_entropy = self.calculate_entropy()
        
        for cycle in range(duration):
            eligible_glyphs = [name for name, glyph in self.glyphs.items() 
                             if glyph.glyph_type not in ["consent"]]
            stress_targets = random.sample(eligible_glyphs, min(3, len(eligible_glyphs)))
            
            for target_name in stress_targets:
                self.glyphs[target_name].process_stress(stress_intensity)
            
            if cycle % 20 == 0:
                self._attempt_glyph_connections()
            
            self.recursive_depth = min(3000, self.recursive_depth + 25)
            
        self.last_stress_test_time = time.time()
        final_coherence = self.calculate_system_coherence()
        final_entropy = self.calculate_entropy()
        
        result = {
            "status": "completed",
            "antifragile_behavior": final_coherence > initial_coherence,
            "final_state": {
                "coherence": final_coherence,
                "entropy": final_entropy,
                "coherence_change": final_coherence - initial_coherence,
                "recursive_depth_achieved": self.recursive_depth
            },
            "entropy_resilience": max(0, 1 - final_entropy)
        }
        
        self.log(f"Stress test completed - Antifragile: {result['antifragile_behavior']}", "success")
        return result

    def _attempt_glyph_connections(self):
        glyph_list = list(self.glyphs.values())
        for i in range(min(5, len(glyph_list))):
            glyph1, glyph2 = random.sample(glyph_list, 2)
            if glyph1.form_connection(glyph2) > 0:
                self.log(f"Connection formed: {glyph1.name} ↔ {glyph2.name}", "info")

    def mandatory_recovery_cycle(self, duration: int = 50) -> Dict:
        self.log(f"Initiating mandatory recovery cycle ({duration} iterations)", "warning")
        
        initial_coherence = self.calculate_system_coherence()
        initial_entropy = self.calculate_entropy()
        
        for cycle in range(duration):
            for glyph in self.glyphs.values():
                if glyph.glyph_type not in ["anchor", "consent"]:
                    stabilization = random.uniform(0.01, 0.03)
                    glyph.gsi = min(1.0, glyph.gsi + stabilization)
                        
        final_coherence = self.calculate_system_coherence()
        final_entropy = self.calculate_entropy()
        
        result = {
            "final_state": {
                "coherence": final_coherence,
                "entropy": final_entropy,
                "recovery_effectiveness": "complete" if final_entropy < 0.1 else "partial"
            }
        }
        
        self.log("Recovery cycle completed", "success")
        return result

    def get_system_status(self) -> Dict:
        return {
            "coherence": self.calculate_system_coherence(),
            "entropy": self.calculate_entropy(),
            "recursive_depth": self.recursive_depth,
            "glyph_count": len(self.glyphs),
            "glyphs": {name: glyph.to_dict() for name, glyph in self.glyphs.items()},
            "logs": self.log_entries[-20:],
            "safety_flags": 0,
            "consent_active": "ConsentGlyph" in self.glyphs,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Global engine instance
engine = GlyphwheelEngine()

# Import the HTML interface
from web_interface import HTML_INTERFACE
from urllib.parse import urlparse

class GlyphwheelHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode('utf-8'))
        elif parsed_path.path == '/api/status':
            self.serve_json(engine.get_system_status())
        else:
            self.send_error(404)
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data)
        except:
            self.send_error(400)
            return
        
        if parsed_path.path == '/api/stress_test':
            intensity = data.get('intensity', 0.5)
            duration = data.get('duration', 100)
            result = engine.run_stress_test(intensity, duration)
            self.serve_json(result)
        elif parsed_path.path == '/api/add_glyph':
            name = data.get('name', '')
            gsi = data.get('gsi', 0.5)
            glyph_type = data.get('type', 'dynamic')
            success = engine.add_glyph(name, gsi, glyph_type)
            self.serve_json({"success": success})
        elif parsed_path.path == '/api/recovery':
            duration = data.get('duration', 50)
            result = engine.mandatory_recovery_cycle(duration)
            self.serve_json(result)
        elif parsed_path.path == '/api/deep_recalibration_protocol':
            duration = 100 # Or get from request
            result = engine.deep_recalibration(duration=duration)
            self.serve_json(result)
        else:
            self.send_error(404)
    
    def serve_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        return  # Suppress server logs

def run_server(port=8080):
    try:
        with socketserver.TCPServer(("", port), GlyphwheelHTTPHandler) as httpd:
            print(f"""
🌟 GLYPHWHEEL FORECAST ENGINE IS RUNNING! 🌟

Your Glyphwheel system is now live at:
👉 http://localhost:{port}

Features available:
✅ Real-time glyph visualization
✅ Interactive stress testing
✅ Live system metrics
✅ Safety protocols active
✅ Recovery mechanisms

Press Ctrl+C to stop the server
""")
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                print("💡 If browser didn't open, manually go to the URL above")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Glyphwheel Engine shutting down gracefully...")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("💡 Try a different port: python glyphwheel_app.py --port 8081")

def main():
    import sys
    
    port = 8080
    if '--port' in sys.argv:
        try:
            port_idx = sys.argv.index('--port')
            port = int(sys.argv[port_idx + 1])
        except (ValueError, IndexError):
            print("Invalid port number. Using default port 8080.")
    
    print("🔄 Initializing Glyphwheel Forecast Engine...")
    
    # Add some initial dynamic glyphs for demonstration
    engine.add_glyph("unstable_Φ", 0.45, "dynamic")
    engine.add_glyph("chaos_Ξ", 0.38, "dynamic")
    engine.add_glyph("harmony_Ψ", 0.62, "dynamic")
    
    print("✅ System initialized with anchor glyphs and consent protocols")
    print("🚀 Starting web server...")
    
    run_server(port)

if __name__ == "__main__":
    main()
