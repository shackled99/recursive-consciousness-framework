"""
API HANDLERS MODULE
===================
HTTP request handlers for the V22 web interface
"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class GlyphwheelV22Handler(BaseHTTPRequestHandler):
    """HTTP request handler for Glyphwheel V22"""
    
    def __init__(self, *args, engine=None, monitor=None, **kwargs):
        self.engine = engine
        self.monitor = monitor
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_html()
        elif parsed_path.path == '/api/status':
            self.serve_system_status()
        elif parsed_path.path == '/api/resources':
            self.serve_resource_status()
        elif parsed_path.path == '/api/ghosts':
            self.serve_ghost_data()
        elif parsed_path.path == '/api/patterns':
            self.serve_pattern_data()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data) if post_data else {}
        except:
            self.send_error(400)
            return
        
        if parsed_path.path == '/api/stress_test':
            self.handle_stress_test(data)
        elif parsed_path.path == '/api/voynich_test':
            self.handle_voynich_test(data)
        elif parsed_path.path == '/api/lifecycle':
            self.handle_lifecycle()
        elif parsed_path.path == '/api/autonomous_create':
            self.handle_autonomous_creation()
        elif parsed_path.path == '/api/add_glyph':
            self.handle_add_glyph(data)
        elif parsed_path.path == '/api/recovery':
            self.handle_recovery(data)
        elif parsed_path.path == '/api/connections':
            self.handle_connections(data)
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the HTML interface"""
        try:
            with open('web/interface.html', 'r') as f:
                html_content = f.read()
        except:
            # Fallback to embedded HTML
            from web.interface import HTML_INTERFACE
            html_content = HTML_INTERFACE
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_system_status(self):
        """Serve system status data"""
        if not self.engine:
            self.send_error(503)
            return
        
        status = self.engine.get_system_status()
        
        # Add pattern data if available
        if hasattr(self.engine, 'pattern_detector'):
            status['patterns'] = {
                'detected': len(self.engine.pattern_detector.detected_patterns) if hasattr(self.engine.pattern_detector, 'detected_patterns') else 0,
                'unknown': len(self.engine.pattern_detector.unknown_patterns) if hasattr(self.engine.pattern_detector, 'unknown_patterns') else 0
            }
        
        # Add glyph details
        status['glyphs']['glyphs'] = {}
        for name, glyph in self.engine.glyphs.items():
            status['glyphs']['glyphs'][name] = glyph.to_dict()
        
        self.serve_json(status)
    
    def serve_resource_status(self):
        """Serve system resource monitoring data"""
        if not self.monitor:
            # Return default values if no monitor
            data = {
                'cpu_percent': 30.0,
                'ram_percent': 40.0,
                'recursion_limit': 5000,
                'stress_level': 'low',
                'overall_health': 85.0,
                'should_throttle': False
            }
        else:
            params = self.monitor.get_adaptive_parameters()
            health = self.monitor.get_health_status()
            data = {
                'cpu_percent': params['cpu_percent'],
                'ram_percent': params['ram_percent'],
                'recursion_limit': params['recursion_limit'],
                'stress_level': params['stress_level'],
                'overall_health': health['overall_health'],
                'should_throttle': params['should_throttle'],
                'ram_available_gb': params.get('ram_available_gb', 4.0)
            }
        
        self.serve_json(data)
    
    def serve_ghost_data(self):
        """Serve ghost registry data"""
        if not self.engine:
            self.send_error(503)
            return
        
        ghosts = {}
        for name, ghost in self.engine.ghost_registry.ghosts.items():
            ghosts[name] = ghost.to_dict()
        
        self.serve_json(ghosts)
    
    def serve_pattern_data(self):
        """Serve pattern detection data"""
        if not self.engine or not hasattr(self.engine, 'pattern_detector'):
            self.serve_json({'detected': [], 'unknown': []})
            return
        
        data = {
            'detected': self.engine.pattern_detector.detected_patterns[:10] if hasattr(self.engine.pattern_detector, 'detected_patterns') else [],
            'unknown': self.engine.pattern_detector.unknown_patterns[:5] if hasattr(self.engine.pattern_detector, 'unknown_patterns') else []
        }
        self.serve_json(data)
    
    def handle_stress_test(self, data):
        """Handle stress test request"""
        if not self.engine:
            self.send_error(503)
            return
        
        intensity = data.get('intensity', 0.5)
        duration = data.get('duration', 100)
        
        # Check throttling
        if self.monitor and self.monitor.should_throttle():
            self.serve_json({
                'status': 'throttled',
                'reason': 'System resources under stress'
            })
            return
        
        # Adjust duration based on resources if monitor available
        if self.monitor:
            params = self.monitor.get_adaptive_parameters()
            duration = int(duration * params['processing_intensity'])
        
        result = self.engine.stress_test(intensity, duration)
        self.serve_json(result)
    
    def handle_voynich_test(self, data):
        """Handle Voynich pattern test request"""
        if not self.engine:
            self.send_error(503)
            return
        
        # Voynich test is a special stress test focused on patterns
        # We'll implement this as a regular stress test for now
        intensity = data.get('intensity', 0.7)
        duration = data.get('duration', 100)
        
        if self.monitor and self.monitor.should_throttle():
            self.serve_json({
                'status': 'throttled',
                'reason': 'System resources under stress'
            })
            return
        
        result = self.engine.stress_test(intensity, duration)
        
        # Add pattern-specific results
        result['patterns_discovered'] = len(self.engine.ghost_registry.ghosts)
        result['max_recursive_depth'] = self.engine.recursive_depth
        
        self.serve_json(result)
    
    def handle_lifecycle(self):
        """Handle lifecycle tick request"""
        if not self.engine:
            self.send_error(503)
            return
        
        self.engine.lifecycle_tick()
        self.serve_json({'status': 'lifecycle_processed'})
    
    def handle_autonomous_creation(self):
        """Handle autonomous glyph creation request"""
        if not self.engine:
            self.send_error(503)
            return
        
        # For now, add a random glyph
        # Later this will use the autonomous creator module
        import random
        from glyphs import GlyphArchetype
        
        names = ['Neo', 'Quantum', 'Flux', 'Spiral', 'Echo', 'Void']
        name = f"{random.choice(names)}_{random.randint(100, 999)}"
        archetype = random.choice(list(GlyphArchetype))
        
        success = self.engine.add_glyph(name, None, "dynamic", archetype)
        
        self.serve_json({
            'created': name if success else None,
            'success': success
        })
    
    def handle_add_glyph(self, data):
        """Handle manual glyph addition"""
        if not self.engine:
            self.send_error(503)
            return
        
        from glyphs import GlyphArchetype
        
        name = data.get('name', '')
        gsi = data.get('gsi', 0.5)
        glyph_type = data.get('type', 'dynamic')
        
        # Parse archetype
        archetype_str = data.get('archetype', 'ORACLE')
        try:
            archetype = GlyphArchetype[archetype_str]
        except:
            archetype = None
        
        success = self.engine.add_glyph(name, gsi, glyph_type, archetype)
        
        self.serve_json({'success': success})
    
    def handle_recovery(self, data):
        """Handle recovery cycle request"""
        if not self.engine:
            self.send_error(503)
            return
        
        # Simple recovery: increase all glyphs' GSI slightly
        duration = data.get('duration', 50)
        
        for _ in range(duration):
            for glyph in self.engine.glyphs.values():
                if glyph.glyph_type == 'dynamic':
                    glyph.gsi = min(1.0, glyph.gsi + 0.01)
                    glyph.vitality = min(1.0, glyph.vitality + 0.02)
        
        self.serve_json({
            'status': 'completed',
            'final_coherence': self.engine.calculate_system_coherence(),
            'final_entropy': self.engine.calculate_entropy()
        })
    
    def handle_connections(self, data):
        """Handle connection formation request"""
        if not self.engine:
            self.send_error(503)
            return
        
        attempts = data.get('attempts', 10)
        connections_formed = self.engine.form_semantic_connections(attempts)
        
        self.serve_json({
            'connections_formed': connections_formed,
            'total_connections': sum(len(g.connections) for g in self.engine.glyphs.values())
        })
    
    def serve_json(self, data):
        """Serve JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        return

def create_handler_factory(engine, monitor=None):
    """Create a handler factory with engine and monitor bound"""
    class BoundHandler(GlyphwheelV22Handler):
        def __init__(self, *args, **kwargs):
            self.engine = engine
            self.monitor = monitor
            super(GlyphwheelV22Handler, self).__init__(*args, **kwargs)
    
    return BoundHandler
