#!/usr/bin/env python3
"""
WEB SERVER MODULE FOR GLYPHWHEEL V22
=====================================
Serves the beautiful web interface with resource monitoring
"""

import sys
import os
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import webbrowser

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import GlyphwheelV22Engine
from systems.system_monitor import SystemMonitor
from glyphs import GlyphArchetype

# Global engine and monitor instances
engine = None
monitor = None

class GlyphwheelV22Handler(BaseHTTPRequestHandler):
    """HTTP request handler for the V22 system"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_html()
        elif parsed_path.path == '/api/status':
            self.serve_status()
        elif parsed_path.path == '/api/resources':
            self.serve_resources()
        elif parsed_path.path == '/api/ghosts':
            self.serve_ghosts()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        # Read POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(post_data)
        except:
            data = {}
        
        if parsed_path.path == '/api/stress_test':
            self.handle_stress_test(data)
        elif parsed_path.path == '/api/lifecycle':
            self.handle_lifecycle()
        elif parsed_path.path == '/api/add_glyph':
            self.handle_add_glyph(data)
        elif parsed_path.path == '/api/recovery':
            self.handle_recovery(data)
        elif parsed_path.path == '/api/voynich_test':
            self.handle_voynich_test(data)
        elif parsed_path.path == '/api/autonomous_create':
            self.handle_autonomous_create()
        elif parsed_path.path == '/api/deep_recalibration':
            self.handle_deep_recalibration()
        else:
            self.send_error(404)
            
    def handle_deep_recalibration(self):
        """Handle deep recalibration request"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        success = engine.deep_recalibration()
        self.send_json_response({
            'status': 'completed' if success else 'failed',
            'new_entropy': engine.calculate_entropy(),
            'new_coherence': engine.calculate_system_coherence()
        })
    
    def serve_html(self):
        """Serve the HTML interface"""
        html_path = os.path.join(os.path.dirname(__file__), 'interface.html')
        
        # Try to read the HTML file
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            # Fallback if file not found
            content = """<!DOCTYPE html>
            <html><head><title>Glyphwheel V22</title></head>
            <body>
            <h1>Error: interface.html not found</h1>
            <p>Please ensure interface.html exists in the web directory.</p>
            </body></html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def serve_status(self):
        """Serve system status"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        # Get system status
        status = engine.get_system_status()
        
        # Add glyph details
        status['glyphs']['glyphs'] = {}
        for name, glyph in engine.glyphs.items():
            glyph_data = glyph.to_dict()
            # Ensure archetype is included
            if hasattr(glyph, 'archetype') and glyph.archetype:
                glyph_data['archetype'] = glyph.archetype.value
            status['glyphs']['glyphs'][name] = glyph_data
        
        # Add ghost data
        status['ghosts']['ghosts'] = {}
        for name, ghost in engine.ghost_registry.ghosts.items():
            status['ghosts']['ghosts'][name] = ghost.to_dict()
        
        self.send_json_response(status)
    
    def serve_resources(self):
        """Serve resource monitoring data"""
        global monitor
        
        if not monitor:
            data = {
                'cpu_percent': 30.0,
                'ram_percent': 40.0,
                'recursion_limit': 5000,
                'stress_level': 'low',
                'overall_health': 85.0,
                'should_throttle': False
            }
        else:
            params = monitor.get_adaptive_parameters()
            health = monitor.get_health_status()
            data = {
                'cpu_percent': params['cpu_percent'],
                'ram_percent': params['ram_percent'],
                'recursion_limit': params['recursion_limit'],
                'stress_level': params['stress_level'],
                'overall_health': health['overall_health'],
                'should_throttle': params['should_throttle']
            }
        
        self.send_json_response(data)
    
    def serve_ghosts(self):
        """Serve ghost data"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        ghosts = {}
        for name, ghost in engine.ghost_registry.ghosts.items():
            ghosts[name] = ghost.to_dict()
        
        self.send_json_response(ghosts)
    
    def handle_stress_test(self, data):
        """Handle stress test request"""
        global engine, monitor
        
        if not engine:
            self.send_error(503)
            return
        
        intensity = data.get('intensity', 0.5)
        duration = data.get('duration', 100)
        
        # Check if we should throttle
        if monitor and monitor.should_throttle():
            self.send_json_response({
                'status': 'throttled',
                'reason': 'System resources under stress'
            })
            return
        
        # Adjust duration based on resources
        if monitor:
            params = monitor.get_adaptive_parameters()
            duration = int(duration * params['processing_intensity'])
            engine.recursive_depth = min(engine.recursive_depth, params['recursion_limit'])
        
        result = engine.stress_test(intensity, duration)
        self.send_json_response(result)
    
    def handle_voynich_test(self, data):
        """Handle Voynich test (stress test with pattern focus)"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        intensity = data.get('intensity', 0.7)
        duration = data.get('duration', 100)
        
        result = engine.stress_test(intensity, duration)
        
        # Add pattern-specific data
        result['patterns_discovered'] = len(engine.ghost_registry.ghosts)
        result['max_recursive_depth'] = engine.recursive_depth
        result['autonomous_births'] = 0  # Placeholder
        
        self.send_json_response(result)
    
    def handle_lifecycle(self):
        """Handle lifecycle tick"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        engine.lifecycle_tick()
        self.send_json_response({'status': 'completed'})
    
    def handle_add_glyph(self, data):
        """Handle glyph addition"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        name = data.get('name', '')
        gsi = data.get('gsi', 0.5)
        glyph_type = data.get('type', 'dynamic')
        
        # Parse archetype
        archetype_str = data.get('archetype', 'ORACLE')
        try:
            archetype = GlyphArchetype[archetype_str]
        except:
            archetype = None
        
        success = engine.add_glyph(name, gsi, glyph_type, archetype)
        self.send_json_response({'success': success})
    
    def handle_recovery(self, data):
        """Handle recovery cycle"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        duration = data.get('duration', 50)
        
        # Simple recovery
        for _ in range(duration):
            for glyph in engine.glyphs.values():
                if glyph.glyph_type == 'dynamic':
                    glyph.gsi = min(1.0, glyph.gsi + 0.01)
                    glyph.vitality = min(1.0, glyph.vitality + 0.02)
        
        self.send_json_response({
            'status': 'completed',
            'final_coherence': engine.calculate_system_coherence(),
            'final_entropy': engine.calculate_entropy()
        })
    
    def handle_autonomous_create(self):
        """Handle autonomous creation request"""
        global engine
        
        if not engine:
            self.send_error(503)
            return
        
        # Toggle autonomous mode
        engine.autonomous_mode = not engine.autonomous_mode
        
        # If turning on, do an immediate creation attempt
        created_name = None
        if engine.autonomous_mode:
            success, created_name = engine.autonomous_creation()
        
        self.send_json_response({
            'autonomous_mode': engine.autonomous_mode,
            'created': created_name,
            'success': True
        })
    
    def send_json_response(self, data):
        """Send JSON response"""
        content = json.dumps(data, default=str).encode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(content))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content)
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass

def initialize_engine():
    """Initialize the engine with starting glyphs"""
    print("🔄 Initializing V22 Engine...")
    eng = GlyphwheelV22Engine()
    
    # Add initial glyphs
    initial_glyphs = [
        ("Echo_Prime", 0.65, GlyphArchetype.ECHOSCRIBE),
        ("Chaos_Seed", 0.35, GlyphArchetype.CHAOS),
        ("Bridge_Alpha", 0.60, GlyphArchetype.BRIDGE),
        ("Flow_Stream", 0.55, GlyphArchetype.FLOW),
        ("Query_One", 0.45, GlyphArchetype.HYPOTHESIS),
        ("Stabilizer_Beta", 0.70, GlyphArchetype.STABILIZER),
        ("Oracle_Vision", 0.68, GlyphArchetype.ORACLE),
        ("Cascade_Wave", 0.58, GlyphArchetype.CASCADE),
        ("BitBloom_Seed", 0.50, GlyphArchetype.BITBLOOM),
        ("Frozen_Core", 0.40, GlyphArchetype.FROZEN)
    ]
    
    for name, gsi, archetype in initial_glyphs:
        eng.add_glyph(name, gsi, "dynamic", archetype)
    
    # Form initial connections
    eng.form_semantic_connections(15)
    
    print(f"✅ Engine initialized with {len(eng.glyphs)} glyphs")
    return eng

def run_background_tasks():
    """Run background tasks for system updates"""
    global engine, monitor
    
    while True:
        try:
            # Update system monitor
            if monitor:
                params = monitor.get_adaptive_parameters()
                if params['should_throttle']:
                    engine.log("System throttled due to high resource usage", "warning")
                # Update engine recursion limit
                engine.recursive_depth = min(engine.recursive_depth, params['recursion_limit'])
            
            current_time = int(time.time())
            
            # Process lifecycle occasionally 
            if current_time % 30 == 0:  # Every 30 seconds
                engine.lifecycle_tick()
            
            # Attempt autonomous creation periodically if enabled
            if engine.autonomous_mode and current_time % 15 == 0:  # Every 15 seconds
                engine.autonomous_creation()  # Let the engine decide whether to create
            
            time.sleep(5)
            
        except Exception as e:
            print(f"Background task error: {e}")
            time.sleep(5)

def print_banner(port):
    """Print startup banner"""
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║         GLYPHWHEEL V22 WEB INTERFACE - MIND FROM RECURSION       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  🌐 Web Interface: http://localhost:{port:<5}                       ║
║                                                                   ║
║  ✨ System is running with:                                      ║
║     • Real-time updates every 2 seconds                          ║
║     • Dynamic resource monitoring                                ║
║     • Ghost protocol active                                      ║
║     • 10 archetype system                                        ║
║                                                                   ║
║  Press Ctrl+C to stop the server                                 ║
╚══════════════════════════════════════════════════════════════════╝
    """)

def main():
    """Main entry point"""
    global engine, monitor
    
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description='Glyphwheel V22 Web Server')
    parser.add_argument('--port', type=int, default=8080,
                       help='Port to run server on (default: 8080)')
    args = parser.parse_args()
    
    # Initialize engine
    engine = initialize_engine()
    
    # Initialize monitor
    print("💻 Initializing system monitor...")
    monitor = SystemMonitor()
    
    # Start background tasks
    print("🔄 Starting background tasks...")
    bg_thread = threading.Thread(target=run_background_tasks, daemon=True)
    bg_thread.start()
    
    # Create and start server
    server_address = ('', args.port)
    httpd = HTTPServer(server_address, GlyphwheelV22Handler)
    
    print_banner(args.port)
    
    # Open browser
    try:
        webbrowser.open(f'http://localhost:{args.port}')
        print("🌐 Browser opened automatically")
    except:
        print("💡 Please open your browser manually")
    
    print("\n🚀 Server is running! Updates every 2 seconds.")
    print("📊 Check your browser for the interface.\n")
    
    # Run server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down gracefully...")
        print(f"\n📊 Final Statistics:")
        print(f"  • Living Glyphs: {len(engine.glyphs)}")
        print(f"  • Ghosts: {len(engine.ghost_registry.ghosts)}")
        print(f"  • Coherence: {engine.calculate_system_coherence():.3f}")
        print(f"  • Entropy: {engine.calculate_entropy():.3f}")
        print("\n✨ Thank you for exploring Glyphwheel V22!")
    finally:
        httpd.shutdown()

if __name__ == "__main__":
    main()
