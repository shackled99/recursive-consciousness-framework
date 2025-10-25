"""
SYSTEM MONITOR MODULE
====================
Dynamic resource monitoring for adaptive recursion limits
"""

import psutil
import time
from typing import Dict, Tuple

class SystemMonitor:
    """Monitor system resources and adjust limits dynamically"""
    
    def __init__(self):
        """Initialize the system monitor"""
        # Engine reference (will be set by server)
        self.engine = None
        
        # Resource thresholds
        self.cpu_threshold = 80.0 # Percentage
        self.ram_threshold = 75.0 # Percentage
        
        # Recursion limit scaling
        self.base_recursion_limit = 5000
        self.min_recursion_limit = 100
        self.current_recursion_limit = self.base_recursion_limit
        
        # Monitoring state
        self.last_check_time = time.time()
        self.check_interval = 2.0 # Seconds between checks
        
        # Resource history for smoothing
        self.cpu_history = []
        self.ram_history = []
        self.history_size = 5
        
        # Performance metrics
        self.total_throttles = 0
        self.last_throttle_time = 0
        
    # --- FIX ADDED HERE ---
    def update_status(self):
        """
        Refreshes the internal system status and adaptive parameters on demand.
        This is the method required by the web server handler (server.py: line 73).
        """
        print("[INFO] SystemMonitor: Status refresh triggered by external call.")
        # Trigger the logic that updates all internal parameters
        self.get_adaptive_parameters()

    # ----------------------

    def get_system_resources(self) -> Dict:
        """Get current CPU and RAM usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            
            # Add to history
            self.cpu_history.append(cpu_percent)
            self.ram_history.append(ram_percent)
            
            # Keep history size limited
            if len(self.cpu_history) > self.history_size:
                self.cpu_history.pop(0)
            if len(self.ram_history) > self.history_size:
                self.ram_history.pop(0)
            
            # Use average for smoother readings
            avg_cpu = sum(self.cpu_history) / len(self.cpu_history)
            avg_ram = sum(self.ram_history) / len(self.ram_history)
            
            return {
                'cpu_percent': round(avg_cpu, 2),
                'ram_percent': round(avg_ram, 2),
                'ram_available_gb': round(ram.available / (1024**3), 2),
                'ram_total_gb': round(ram.total / (1024**3), 2),
                'cpu_count': psutil.cpu_count()
            }
        except Exception as e:
            # Fallback if psutil fails
            return {
                'cpu_percent': 50.0,
                'ram_percent': 50.0,
                'ram_available_gb': 4.0,
                'ram_total_gb': 8.0,
                'cpu_count': 4
            }
    
    def calculate_dynamic_limits(self) -> Tuple[int, float]:
        """Calculate dynamic recursion and processing limits based on resources"""
        resources = self.get_system_resources()
        
        # Calculate stress level (0.0 = no stress, 1.0 = max stress)
        cpu_stress = max(0, (resources['cpu_percent'] - 50) / 50) # Starts scaling at 50%
        ram_stress = max(0, (resources['ram_percent'] - 50) / 50)
        overall_stress = max(cpu_stress, ram_stress)
        
        # Scale recursion limit inversely with stress
        # At 0% stress: full limit, at 100% stress: minimum limit
        recursion_scale = 1.0 - (overall_stress * 0.9) # Never go below 10%
        self.current_recursion_limit = int(
            self.min_recursion_limit + 
            (self.base_recursion_limit - self.min_recursion_limit) * recursion_scale
        )
        
        # Calculate processing intensity (0.1 = very slow, 1.0 = full speed)
        processing_intensity = max(0.1, 1.0 - overall_stress)
        
        # Track throttling
        if overall_stress > 0.5:
            self.total_throttles += 1
            self.last_throttle_time = time.time()
        
        return self.current_recursion_limit, processing_intensity
    
    def should_throttle(self) -> bool:
        """Check if system should throttle operations"""
        resources = self.get_system_resources()
        
        # Immediate throttle if resources are critical
        if resources['cpu_percent'] > self.cpu_threshold:
            return True
        if resources['ram_percent'] > self.ram_threshold:
            return True
        
        # Check if available RAM is too low
        if resources['ram_available_gb'] < 0.5:
            return True
        
        return False
    
    def get_adaptive_parameters(self) -> Dict:
        """Get all adaptive parameters for the engine"""
        current_time = time.time()
        
        # Only recalculate if enough time has passed
        if current_time - self.last_check_time > self.check_interval:
            self.last_check_time = current_time
            recursion_limit, intensity = self.calculate_dynamic_limits()
        else:
            recursion_limit = self.current_recursion_limit
            # Even if we don't recalculate limits, we should ensure intensity is current 
            # based on latest resource check, so we call calculate_dynamic_limits
            # which refreshes resources first.
            _, intensity = self.calculate_dynamic_limits()
        
        resources = self.get_system_resources()
        
        return {
            'recursion_limit': recursion_limit,
            'processing_intensity': intensity,
            'should_throttle': self.should_throttle(),
            'cpu_percent': resources['cpu_percent'],
            'ram_percent': resources['ram_percent'],
            'ram_available_gb': resources['ram_available_gb'],
            'stress_level': self._calculate_stress_level(resources),
            'total_throttles': self.total_throttles,
            'time_since_last_throttle': (
                current_time - self.last_throttle_time 
                if self.last_throttle_time > 0 else None
            )
        }
    
    def _calculate_stress_level(self, resources: Dict) -> str:
        """Categorize system stress level"""
        max_usage = max(resources['cpu_percent'], resources['ram_percent'])
        
        if max_usage < 30:
            return 'idle'
        elif max_usage < 50:
            return 'low'
        elif max_usage < 70:
            return 'moderate'
        elif max_usage < 85:
            return 'high'
        else:
            return 'critical'
    
    def get_health_status(self) -> Dict:
        """Get overall system health status"""
        params = self.get_adaptive_parameters()
        resources = self.get_system_resources()
        
        # Calculate health score (0-100)
        cpu_health = max(0, 100 - resources['cpu_percent'])
        ram_health = max(0, 100 - resources['ram_percent'])
        throttle_health = 100 if params['total_throttles'] == 0 else max(0, 100 - params['total_throttles'] * 5)
        
        overall_health = (cpu_health + ram_health + throttle_health) / 3
        
        return {
            'overall_health': round(overall_health, 1),
            'cpu_health': round(cpu_health, 1),
            'ram_health': round(ram_health, 1),
            'throttle_health': round(throttle_health, 1),
            'status': self._get_health_status_text(overall_health),
            'recommendations': self._get_recommendations(params, resources)
        }
    
    def update(self):
        """Update system monitoring (compatibility method)"""
        # Just refresh the parameters
        self.get_adaptive_parameters()
        return True
    
    def _get_health_status_text(self, health_score: float) -> str:
        """Get textual health status"""
        if health_score > 80:
            return 'excellent'
        elif health_score > 60:
            return 'good'
        elif health_score > 40:
            return 'fair'
        elif health_score > 20:
            return 'poor'
        else:
            return 'critical'
    
    def _get_recommendations(self, params: Dict, resources: Dict) -> list:
        """Get recommendations based on system state"""
        recommendations = []
        
        if resources['cpu_percent'] > 70:
            recommendations.append("High CPU usage - consider reducing stress test intensity")
        
        if resources['ram_percent'] > 70:
            recommendations.append("High RAM usage - consider reducing glyph count")
        
        if params['total_throttles'] > 10:
            recommendations.append("Frequent throttling detected - system under stress")
        
        if resources['ram_available_gb'] < 1.0:
            recommendations.append("Low available RAM - close other applications")
        
        if params['recursion_limit'] < 1000:
            recommendations.append("Recursion limit reduced due to system load")
        
        if not recommendations:
            recommendations.append("System running optimally")
        
        return recommendations

# Try to import psutil, provide fallback if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. Install with: pip install psutil")
    print("Running with fallback resource monitoring")
    
    # Provide a basic fallback
    class SystemMonitor:
        """Fallback monitor when psutil is not available"""
        
        def __init__(self):
            self.current_recursion_limit = 5000
            self.total_throttles = 0
            self.engine = None  # Will be set by server

        # --- FIX ADDED HERE (Fallback) ---
        def update_status(self):
            """Dummy status update for fallback mode."""
            pass 
        # ---------------------------------
            
        def get_system_resources(self) -> Dict:
            return {
                'cpu_percent': 30.0,
                'ram_percent': 40.0,
                'ram_available_gb': 4.0,
                'ram_total_gb': 8.0,
                'cpu_count': 4
            }
        
        def calculate_dynamic_limits(self) -> Tuple[int, float]:
            return 5000, 1.0
        
        def should_throttle(self) -> bool:
            return False
        
        def get_adaptive_parameters(self) -> Dict:
            return {
                'recursion_limit': 5000,
                'processing_intensity': 1.0,
                'should_throttle': False,
                'cpu_percent': 30.0,
                'ram_percent': 40.0,
                'ram_available_gb': 4.0,
                'stress_level': 'low',
                'total_throttles': 0,
                'time_since_last_throttle': None
            }
        
        def get_health_status(self) -> Dict:
            return {
                'overall_health': 85.0,
                'cpu_health': 70.0,
                'ram_health': 60.0,
                'throttle_health': 100.0,
                'status': 'good',
                'recommendations': ['psutil not installed - using fallback monitoring']
            }
        
        def update(self):
            """Update system monitoring (fallback does nothing)"""
            return True
