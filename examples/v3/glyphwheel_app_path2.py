#!/usr/bin/env python3
"""
🌟 GLYPHWHEEL PATH 2: TWO-STAGE AUTONOMOUS INTELLIGENCE 🌟
Emergency Stabilization + Optimization Passes Architecture
"""

import json
import random
import math
import time
import webbrowser
import threading
import os
from typing import Dict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
import socketserver

class DetailedLogger:
    def __init__(self):
        self.detailed_logs = []
        self.glyph_history = {}
        
        # Set up file logging
        self.log_directory = "logs"
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
            
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = os.path.join(self.log_directory, f"glyphwheel_path2_{timestamp}.log")
        
        # Write session header
        with open(self.log_filename, 'w') as f:
            f.write(f"# Glyphwheel Path 2 Session Log - Started: {datetime.now().isoformat()}\n")
            f.write("# Format: [timestamp] EVENT_TYPE: data\n\n")
        
    def log_detailed(self, event_type: str, data: dict):
        """Log detailed system events for analysis"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # milliseconds
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data
        }
        self.detailed_logs.append(log_entry)
        
        # Keep last 500 detailed logs in memory
        if len(self.detailed_logs) > 500:
            self.detailed_logs.pop(0)
            
        # Format log line for both console and file
        log_line = f"[{timestamp}] {event_type}: {data}"
        print(log_line)
        
        # Write to file (skip Unicode errors)
        try:
            with open(self.log_filename, 'a', encoding='utf-8', errors='replace') as f:
                f.write(log_line + "\n")
                f.flush()
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
        
    def log_glyph_change(self, glyph_name: str, old_gsi: float, new_gsi: float, cause: str):
        """Track individual glyph GSI changes"""
        change = new_gsi - old_gsi
        self.log_detailed("GLYPH_CHANGE", {
            "name": glyph_name,
            "old_gsi": round(old_gsi, 6),
            "new_gsi": round(new_gsi, 6),
            "change": round(change, 6),
            "cause": cause
        })

class TwoStageDecisionMaker:
    """PATH 2: Two-stage autonomous intelligence - Emergency + Optimization"""
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.decision_history = []
        
        # Entropy thresholds for emergency detection
        self.emergency_thresholds = {
            'critical': 0.40,
            'emergency': 0.25,
            'high_concern': 0.15,
            'moderate_concern': 0.10,
            'low_concern': 0.05
        }
        
        # Hysteresis for emergency threshold
        self.emergency_hysteresis = 0.02
        
        # Available actions for both stages
        self.available_actions = {
            # Emergency Stage Actions
            'emergency_recovery': {'priority': 5, 'description': 'Emergency recovery for critical entropy levels'},
            'recovery_cycle': {'priority': 4, 'description': 'Standard recovery cycle for stabilization'},
            'gentle_stabilization': {'priority': 3, 'description': 'Light stabilization for minor issues'},
            
            # Optimization Stage Actions  
            'optimization_stress_test': {'priority': 6, 'description': 'Stress test with connection formation for optimization'},
            'connection_building': {'priority': 2, 'description': 'Focus on building connections between stable glyphs'},
            
            # Monitoring Actions
            'wait_and_monitor': {'priority': 1, 'description': 'Continue monitoring without intervention'},
            'ignore_threshold': {'priority': 0, 'description': 'Accept current state as acceptable'}
        }
        
        # State tracking
        self.last_intervention_time = 0
        self.consecutive_same_decisions = 0
        self.last_decision = None
        self.system_state = "unknown"
        
    def evaluate_situation(self, entropy_level, entropy_threshold, idle_duration):
        """PATH 2: Two-stage evaluation - Emergency or Optimization"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Classify current system state
        system_state = self._classify_system_state(entropy_level)
        coherence = self.engine.calculate_system_coherence()
        
        # Gather comprehensive context
        context = {
            'entropy_level': entropy_level,
            'system_state': system_state,
            'entropy_threshold': entropy_threshold,
            'idle_duration_minutes': idle_duration / 60,
            'current_coherence': coherence,
            'glyph_count': len(self.engine.glyphs),
            'total_connections': sum(len(g.connections) for g in self.engine.glyphs.values()),
            'imperfect_glyphs': self._count_imperfect_glyphs(),
            'unconnected_glyphs': self._count_unconnected_glyphs(),
            'time_since_last_intervention': self._time_since_last_intervention(),
            'recent_decision_pattern': self._analyze_recent_decisions(),
            'consecutive_same_decisions': self.consecutive_same_decisions
        }
        
        logger.log_detailed("PATH2_DECISION_EVALUATION_START", {
            "entropy_situation": {
                "level": entropy_level,
                "threshold": entropy_threshold,
                "system_state": system_state
            },
            "context": context
        })
        
        # Choose strategy based on system state
        if system_state in ['critical', 'emergency', 'unstable']:
            chosen_action, reasoning = self._emergency_stage_decision(context)
        elif system_state == 'stable_but_suboptimal':
            chosen_action, reasoning = self._optimization_stage_decision(context)
        else:  # stable_and_optimal
            chosen_action, reasoning = self._maintenance_stage_decision(context)
        
        # Update decision tracking
        self._track_decision(chosen_action)
        
        # Log decision result
        decision_record = {
            "timestamp": timestamp,
            "system_state": system_state,
            "stage": self._get_decision_stage(system_state),
            "context": context,
            "chosen_action": chosen_action,
            "reasoning": reasoning,
            "decision_confidence": self._calculate_confidence(chosen_action, system_state)
        }
        
        self.decision_history.append(decision_record)
        if len(self.decision_history) > 100:
            self.decision_history.pop(0)
            
        logger.log_detailed("PATH2_AUTONOMOUS_DECISION_MADE", decision_record)
        
        return chosen_action, reasoning
        
    def _classify_system_state(self, entropy_level):
        """Classify the current system state for decision-making"""
        coherence = self.engine.calculate_system_coherence()
        imperfect_glyphs = self._count_imperfect_glyphs()
        unconnected_glyphs = self._count_unconnected_glyphs()
        
        # Emergency conditions
        if entropy_level > self.emergency_thresholds['critical']:
            return 'critical'
        elif entropy_level > self.emergency_thresholds['emergency']:
            return 'emergency'
        elif entropy_level > self.emergency_thresholds['high_concern']:
            return 'unstable'
        
        # Stable conditions - check for optimization needs
        elif entropy_level <= self.emergency_thresholds['low_concern']:
            if imperfect_glyphs == 0 and unconnected_glyphs == 0 and coherence > 0.99:
                return 'stable_and_optimal'
            else:
                return 'stable_but_suboptimal'
        else:
            # Moderate entropy levels
            if coherence > 0.90 and imperfect_glyphs <= 2:
                return 'stable_but_suboptimal'
            else:
                return 'unstable'
    
    def _emergency_stage_decision(self, context):
        """Stage 1: Emergency stabilization decisions"""
        entropy = context['entropy_level']
        coherence = context['current_coherence']
        
        # For extreme entropy, override hysteresis
        if entropy > 0.30:
            if entropy > 0.50:
                return 'emergency_recovery', f"Critical entropy {entropy:.3f} requires emergency intervention"
            else:
                return 'recovery_cycle', f"High entropy {entropy:.3f} requires immediate stabilization"
        
        # Apply hysteresis for moderate entropy levels
        effective_threshold = self._calculate_emergency_threshold()
        if entropy > effective_threshold:
            if coherence < 0.8:
                return 'recovery_cycle', f"Entropy {entropy:.3f} with low coherence {coherence:.3f} needs recovery"
            else:
                return 'gentle_stabilization', f"Entropy {entropy:.3f} with good coherence {coherence:.3f} needs gentle intervention"
        
        # Shouldn't reach here in emergency stage, but safety fallback
        return 'wait_and_monitor', f"Emergency stage fallback - monitoring entropy {entropy:.3f}"
    
    def _optimization_stage_decision(self, context):
        """Stage 2: Optimization decisions for stable but suboptimal systems"""
        imperfect_glyphs = context['imperfect_glyphs']
        unconnected_glyphs = context['unconnected_glyphs']
        coherence = context['current_coherence']
        time_since_intervention = context['time_since_last_intervention']
        
        # Score optimization actions
        scores = {}
        
        # Optimization stress test - best when system is stable and needs improvement
        if coherence > 0.85 and time_since_intervention > 120:  # 2 minutes cooldown
            optimization_score = 70
            if imperfect_glyphs > 0:
                optimization_score += min(20, imperfect_glyphs * 5)  # Bonus for glyphs needing improvement
            if unconnected_glyphs > 0:
                optimization_score += min(15, unconnected_glyphs * 3)  # Bonus for connection needs
            scores['optimization_stress_test'] = optimization_score
        else:
            scores['optimization_stress_test'] = 20
        
        # Connection building - good when glyphs are perfect but unconnected
        if unconnected_glyphs > 0 and imperfect_glyphs == 0:
            scores['connection_building'] = 60 + min(20, unconnected_glyphs * 4)
        else:
            scores['connection_building'] = 30
        
        # Gentle stabilization - for fine-tuning nearly perfect glyphs
        if imperfect_glyphs > 0 and coherence > 0.95:
            scores['gentle_stabilization'] = 50 + min(15, imperfect_glyphs * 3)
        else:
            scores['gentle_stabilization'] = 25
        
        # Wait and monitor - when recent interventions or minimal issues
        wait_score = 45
        if time_since_intervention < 300:  # Recent intervention
            wait_score += 20
        if imperfect_glyphs <= 1 and unconnected_glyphs <= 1:
            wait_score += 15
        scores['wait_and_monitor'] = wait_score
        
        # Apply repetition penalty
        repetition_penalty = min(30, context['consecutive_same_decisions'] * 8)
        if self.last_decision in scores:
            scores[self.last_decision] = max(10, scores[self.last_decision] - repetition_penalty)
        
        # Select best action
        best_action = max(scores.keys(), key=lambda a: scores[a])
        best_score = scores[best_action]
        
        reasoning = f"Optimization stage: {best_action} (score: {best_score}) - {imperfect_glyphs} imperfect glyphs, {unconnected_glyphs} unconnected"
        
        return best_action, reasoning
    
    def _maintenance_stage_decision(self, context):
        """Stage 3: Maintenance decisions for optimal systems"""
        time_since_intervention = context['time_since_last_intervention']
        
        # In optimal state, mostly just monitor
        if time_since_intervention > 600:  # 10 minutes since last intervention
            # Occasionally do light maintenance
            if random.random() < 0.1:  # 10% chance
                return 'gentle_stabilization', "Periodic maintenance of optimal system"
        
        return 'wait_and_monitor', "System optimal - maintaining surveillance"
    
    def _calculate_emergency_threshold(self):
        """Calculate effective emergency threshold with hysteresis"""
        base_threshold = self.emergency_thresholds['high_concern']  # 0.15
        
        # Check recent emergency interventions
        recent_interventions = [d for d in self.decision_history[-5:] 
                              if d['chosen_action'] in ['emergency_recovery', 'recovery_cycle']]
        
        if recent_interventions:
            return base_threshold + self.emergency_hysteresis
        else:
            return base_threshold
    
    def _count_imperfect_glyphs(self):
        """Count glyphs with GSI < 1.0"""
        return sum(1 for glyph in self.engine.glyphs.values() 
                  if glyph.gsi < 0.999 and glyph.glyph_type not in ["anchor", "consent"])
    
    def _count_unconnected_glyphs(self):
        """Count glyphs with no connections"""
        return sum(1 for glyph in self.engine.glyphs.values() 
                  if len(glyph.connections) == 0 and glyph.glyph_type not in ["anchor"])
    
    def _get_decision_stage(self, system_state):
        """Get which decision stage was used"""
        if system_state in ['critical', 'emergency', 'unstable']:
            return 'emergency'
        elif system_state == 'stable_but_suboptimal':
            return 'optimization'
        else:
            return 'maintenance'
    
    def _calculate_confidence(self, chosen_action, system_state):
        """Calculate confidence in decision"""
        if system_state in ['critical', 'emergency']:
            return 95  # High confidence in emergency decisions
        elif chosen_action == 'optimization_stress_test':
            return 85  # Good confidence in optimization
        elif chosen_action == 'wait_and_monitor':
            return 90  # High confidence in monitoring stable systems
        else:
            return 75  # Standard confidence
    
    def _track_decision(self, chosen_action):
        """Track decision patterns to prevent loops"""
        if chosen_action == self.last_decision:
            self.consecutive_same_decisions += 1
        else:
            self.consecutive_same_decisions = 1
            
        self.last_decision = chosen_action
        
    def _time_since_last_intervention(self):
        """Calculate time since last intervention"""
        return max(0, time.time() - self.last_intervention_time)
        
    def _analyze_recent_decisions(self):
        """Analyze pattern in recent decisions"""
        if not self.decision_history:
            return "no_history"
            
        recent = self.decision_history[-5:]
        actions = [d['chosen_action'] for d in recent]
        
        if len(set(actions)) == 1:
            return f"consistent_{actions[0]}"
        elif actions.count('optimization_stress_test') >= 2:
            return "frequent_optimization"
        elif actions.count('recovery_cycle') >= 3:
            return "repeated_recovery"
        else:
            return "mixed_responses"

class PathTwoIdleMonitor:
    """Enhanced idle monitor with two-stage decision implementation"""
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.is_running = False
        self.monitor_thread = None
        
        # Parameters
        self.decay_rate = 0.0001
        self.monitor_interval = 30  # seconds between checks
        
        # State tracking
        self.last_activity_time = time.time()
        self.idle_start_time = None
        
    def start_monitoring(self):
        """Start the background monitoring thread"""
        if not self.is_running:
            self.is_running = True
            self.idle_start_time = time.time()
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.log_detailed("PATH2_IDLE_MONITORING_STARTED", {
                "monitor_interval": self.monitor_interval,
                "decay_rate": self.decay_rate
            })
            
    def stop_monitoring(self):
        """Stop the background monitoring"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.log_detailed("PATH2_IDLE_MONITORING_STOPPED", {})
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                self._perform_path2_check()
                time.sleep(self.monitor_interval)
            except Exception as e:
                logger.log_detailed("IDLE_MONITOR_ERROR", {"error": str(e)})
                time.sleep(self.monitor_interval)
                
    def _perform_path2_check(self):
        """PATH 2: Enhanced idle checking with two-stage logic"""
        current_time = time.time()
        idle_duration = current_time - (self.idle_start_time or current_time)
        
        entropy = self.engine.calculate_entropy()
        coherence = self.engine.calculate_system_coherence()
        
        # Log periodic status regardless of entropy level
        if int(idle_duration) % 300 == 0 and idle_duration > 0:  # Every 5 minutes
            logger.log_detailed("PATH2_PERIODIC_STATUS", {
                "idle_duration_minutes": round(idle_duration / 60, 2),
                "system_entropy": round(entropy, 6),
                "system_coherence": round(coherence, 6),
                "imperfect_glyphs": self.engine.decision_maker._count_imperfect_glyphs(),
                "unconnected_glyphs": self.engine.decision_maker._count_unconnected_glyphs(),
                "system_state": self.engine.decision_maker._classify_system_state(entropy)
            })
        
        # Evaluate for any intervention (emergency OR optimization)
        system_state = self.engine.decision_maker._classify_system_state(entropy)
        
        # Act if system needs emergency OR optimization
        if (system_state in ['critical', 'emergency', 'unstable'] or 
            system_state == 'stable_but_suboptimal'):
            
            logger.log_detailed("PATH2_INTERVENTION_TRIGGER", {
                "entropy": entropy,
                "coherence": coherence,
                "system_state": system_state,
                "trigger_reason": "emergency" if system_state in ['critical', 'emergency', 'unstable'] else "optimization"
            })
            
            action, reasoning = self.engine.decision_maker.evaluate_situation(
                entropy, 0.15, idle_duration
            )
            
            self._execute_path2_action(action, reasoning, entropy, system_state)
            
    def _execute_path2_action(self, action, reasoning, entropy, system_state):
        """Execute PATH 2 actions with enhanced capabilities"""
        logger.log_detailed("PATH2_AUTONOMOUS_ACTION_EXECUTION", {
            "action": action,
            "reasoning": reasoning,
            "entropy_level": entropy,
            "system_state": system_state
        })
        
        if action == 'emergency_recovery':
            try:
                # More intensive recovery for emergencies
                result = self.engine.mandatory_recovery_cycle(50)  # Longer duration
                self.engine.decision_maker.last_intervention_time = time.time()
                logger.log_detailed("EMERGENCY_RECOVERY_COMPLETED", {"result": result})
            except Exception as e:
                logger.log_detailed("EMERGENCY_RECOVERY_FAILED", {"error": str(e)})
                
        elif action == 'recovery_cycle':
            try:
                result = self.engine.mandatory_recovery_cycle(30)
                self.engine.decision_maker.last_intervention_time = time.time()
                logger.log_detailed("AUTONOMOUS_RECOVERY_COMPLETED", {"result": result})
            except Exception as e:
                logger.log_detailed("AUTONOMOUS_RECOVERY_FAILED", {"error": str(e)})
                
        elif action == 'optimization_stress_test':
            # PATH 2: Enhanced stress test with connection focus
            try:
                result = self.engine.optimization_stress_test(0.6, 120)  # More intensive optimization
                self.engine.decision_maker.last_intervention_time = time.time()
                logger.log_detailed("OPTIMIZATION_STRESS_TEST_COMPLETED", {"result": result})
            except Exception as e:
                logger.log_detailed("OPTIMIZATION_STRESS_TEST_FAILED", {"error": str(e)})
                
        elif action == 'connection_building':
            try:
                self._perform_connection_building()
                self.engine.decision_maker.last_intervention_time = time.time()
            except Exception as e:
                logger.log_detailed("CONNECTION_BUILDING_FAILED", {"error": str(e)})
                
        elif action == 'gentle_stabilization':
            try:
                self._perform_gentle_stabilization()
                self.engine.decision_maker.last_intervention_time = time.time()
            except Exception as e:
                logger.log_detailed("GENTLE_STABILIZATION_FAILED", {"error": str(e)})
                
        # For 'wait_and_monitor' and 'ignore_threshold', no action needed
        
    def _perform_connection_building(self):
        """PATH 2: Dedicated connection building for optimization stage"""
        logger.log_detailed("CONNECTION_BUILDING_START", {})
        
        glyph_list = list(self.engine.glyphs.values())
        connections_formed = 0
        
        # Focus on unconnected glyphs
        unconnected = [g for g in glyph_list if len(g.connections) == 0]
        well_connected = [g for g in glyph_list if len(g.connections) > 3]
        
        for unconnected_glyph in unconnected:
            for connected_glyph in well_connected:
                connection_strength = unconnected_glyph.form_connection(connected_glyph)
                if connection_strength > 0:
                    connections_formed += 1
                    break  # One connection per unconnected glyph per cycle
        
        # Additional general connection attempts
        for _ in range(10):
            if len(glyph_list) >= 2:
                glyph1, glyph2 = random.sample(glyph_list, 2)
                connection_strength = glyph1.form_connection(glyph2)
                if connection_strength > 0:
                    connections_formed += 1
                    
        logger.log_detailed("CONNECTION_BUILDING_COMPLETED", {
            "connections_formed": connections_formed,
            "total_connections": sum(len(g.connections) for g in self.engine.glyphs.values())
        })
        
    def _perform_gentle_stabilization(self):
        """Gentle stabilization for fine-tuning"""
        logger.log_detailed("GENTLE_STABILIZATION_START", {})
        
        stabilized_glyphs = []
        for name, glyph in self.engine.glyphs.items():
            if glyph.glyph_type == 'dynamic' and glyph.gsi < 0.999:
                old_gsi = glyph.gsi
                # Gentle nudge toward perfection
                improvement = random.uniform(0.005, 0.02)
                glyph.gsi = min(1.0, glyph.gsi + improvement)
                
                if abs(glyph.gsi - old_gsi) > 0.001:
                    logger.log_glyph_change(name, old_gsi, glyph.gsi, "gentle_stabilization")
                    stabilized_glyphs.append(name)
                    
        logger.log_detailed("GENTLE_STABILIZATION_COMPLETED", {
            "stabilized_glyphs": stabilized_glyphs,
            "new_entropy": self.engine.calculate_entropy(),
            "new_coherence": self.engine.calculate_system_coherence()
        })

# Support for deep recalibration
def deep_recalibration(system_state):
    """Deep recalibration process to restore ConsentGlyph GSI"""
    logger.log_detailed("DEEP_RECALIBRATION_INITIATED", {"reason": "ethical_debt_resolution"})
    
    if 'ConsentGlyph' in system_state['glyphs']:
        consent_glyph = engine.glyphs['ConsentGlyph']
        old_gsi = consent_glyph.gsi
        
        consent_glyph.gsi = 1.0
        logger.log_glyph_change('ConsentGlyph', old_gsi, 1.0, 'deep_recalibration')
        
        coherence = engine.calculate_system_coherence()
        entropy = engine.calculate_entropy()
        
        logger.log_detailed("DEEP_RECALIBRATION_SUCCESS", {
            "old_consent_gsi": round(old_gsi, 6),
            "new_consent_gsi": 1.0,
            "gsi_change": round(1.0 - old_gsi, 6),
            "new_coherence": round(coherence, 6),
            "new_entropy": round(entropy, 6)
        })
        
        engine.log("Deep recalibration successful. Ethical debt resolved.", "success")
        
        return {
            "status": "success",
            "message": "Deep recalibration completed successfully",
            "consent_gsi_restored": True,
            "old_gsi": old_gsi,
            "new_gsi": 1.0,
            "system_coherence": coherence,
            "system_entropy": entropy
        }
    else:
        logger.log_detailed("DEEP_RECALIBRATION_FAILED", {"reason": "ConsentGlyph_not_found"})
        engine.log("ConsentGlyph not found in system state. Recalibration aborted.", "error")
        
        return {
            "status": "error",
            "message": "ConsentGlyph not found in system state",
            "consent_gsi_restored": False
        }

class Glyph:
    def __init__(self, name: str, initial_gsi: float = 0.5, glyph_type: str = "standard"):
        self.name = name
        self.glyph_type = glyph_type
        self.gsi = initial_gsi
        self.history = [initial_gsi]
        self.connections = []
        self.adaptation_rate = 0.1
        
        logger.log_detailed("GLYPH_CREATED", {
            "name": name,
            "initial_gsi": round(initial_gsi, 6),
            "type": glyph_type
        })
        
    def process_stress(self, stress_level: float) -> float:
        old_gsi = self.gsi
        adaptation = stress_level * self.adaptation_rate
        
        if stress_level > 0.3:
            self.gsi = min(1.0, self.gsi + adaptation)
        else:
            self.gsi = max(0.0, self.gsi - adaptation)
            
        self.history.append(self.gsi)
        
        if abs(self.gsi - old_gsi) > 0.001:
            logger.log_glyph_change(self.name, old_gsi, self.gsi, f"stress_processing(level={stress_level})")
        
        return self.gsi
        
    def form_connection(self, other_glyph: 'Glyph') -> float:
        connection_strength = (self.gsi + other_glyph.gsi) / 2.0
        if connection_strength > 0.6:
            if other_glyph.name not in self.connections:  # Avoid duplicate connections
                self.connections.append(other_glyph.name)
                logger.log_detailed("CONNECTION_FORMED", {
                    "glyph1": self.name,
                    "glyph2": other_glyph.name,
                    "connection_strength": round(connection_strength, 6)
                })
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
        self.log("PATH 2 System initialized successfully", "success")
        
        # PATH 2: Initialize two-stage systems
        self.decision_maker = TwoStageDecisionMaker(self)
        self.idle_monitor = PathTwoIdleMonitor(self)
        
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
        coherence = min(1.0, (avg_gsi * 0.7) + (connection_factor * 0.3))
        return coherence
        
    def calculate_entropy(self) -> float:
        if not self.glyphs:
            return 1.0
        gsi_values = [glyph.gsi for glyph in self.glyphs.values()]
        mean_gsi = sum(gsi_values) / len(gsi_values)
        variance = sum((gsi - mean_gsi) ** 2 for gsi in gsi_values) / len(gsi_values)
        entropy = min(1.0, math.sqrt(variance) * 2)
        return entropy

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

    def optimization_stress_test(self, stress_intensity: float = 0.6, duration: int = 120) -> Dict:
        """PATH 2: Enhanced stress test focused on optimization and connection building"""
        if not self.request_consent("optimization_stress_test"):
            return {"status": "aborted", "reason": "consent_denied"}

        self.log(f"Starting optimization stress test (intensity: {stress_intensity}, duration: {duration})", "info")
        
        initial_coherence = self.calculate_system_coherence()
        initial_entropy = self.calculate_entropy()
        initial_connections = sum(len(g.connections) for g in self.glyphs.values())
        
        for cycle in range(duration):
            # Focus on imperfect glyphs for stress
            eligible_glyphs = [name for name, glyph in self.glyphs.items() 
                             if glyph.glyph_type == "dynamic" and glyph.gsi < 0.999]
            
            if eligible_glyphs:
                stress_targets = random.sample(eligible_glyphs, min(2, len(eligible_glyphs)))
                for target_name in stress_targets:
                    self.glyphs[target_name].process_stress(stress_intensity)
            
            # More frequent connection attempts for optimization
            if cycle % 10 == 0:
                self._attempt_glyph_connections()
                
            # Special focus on connecting unconnected glyphs
            if cycle % 15 == 0:
                self._attempt_unconnected_integration()
            
            self.recursive_depth = min(3000, self.recursive_depth + 25)
            
        self.last_stress_test_time = time.time()
        final_coherence = self.calculate_system_coherence()
        final_entropy = self.calculate_entropy()
        final_connections = sum(len(g.connections) for g in self.glyphs.values())
        
        result = {
            "status": "completed",
            "optimization_type": "connection_focused",
            "antifragile_behavior": final_coherence > initial_coherence,
            "final_state": {
                "coherence": final_coherence,
                "entropy": final_entropy,
                "coherence_change": final_coherence - initial_coherence,
                "connections_added": final_connections - initial_connections,
                "recursive_depth_achieved": self.recursive_depth
            },
            "optimization_effectiveness": "complete" if final_entropy < 0.05 else "partial"
        }
        
        self.log(f"Optimization stress test completed - Connections added: {result['final_state']['connections_added']}", "success")
        return result

    def _attempt_unconnected_integration(self):
        """PATH 2: Special method to integrate unconnected glyphs"""
        glyph_list = list(self.glyphs.values())
        unconnected = [g for g in glyph_list if len(g.connections) == 0]
        well_connected = [g for g in glyph_list if len(g.connections) >= 3]
        
        for unconnected_glyph in unconnected:
            if well_connected:
                target = random.choice(well_connected)
                connection_strength = unconnected_glyph.form_connection(target)
                if connection_strength > 0:
                    self.log(f"Integrated unconnected glyph: {unconnected_glyph.name} ↔ {target.name}", "info")

    def _attempt_glyph_connections(self):
        glyph_list = list(self.glyphs.values())
        connection_attempts = min(5, len(glyph_list))
        
        for i in range(connection_attempts):
            if len(glyph_list) >= 2:
                glyph1, glyph2 = random.sample(glyph_list, 2)
                connection_strength = glyph1.form_connection(glyph2)
                if connection_strength > 0:
                    self.log(f"Connection formed: {glyph1.name} ↔ {glyph2.name}", "info")

    def mandatory_recovery_cycle(self, duration: int = 50) -> Dict:
        self.log(f"Initiating mandatory recovery cycle ({duration} iterations)", "warning")
        
        for cycle in range(duration):
            for glyph in self.glyphs.values():
                if glyph.glyph_type not in ["anchor", "consent"]:
                    old_gsi = glyph.gsi
                    stabilization = random.uniform(0.01, 0.03)
                    glyph.gsi = min(1.0, glyph.gsi + stabilization)
                    
                    if abs(glyph.gsi - old_gsi) > 0.001:
                        logger.log_glyph_change(glyph.name, old_gsi, glyph.gsi, f"recovery_cycle_{cycle}")
        
        result = {
            "final_state": {
                "coherence": self.calculate_system_coherence(),
                "entropy": self.calculate_entropy(),
                "recovery_effectiveness": "complete" if self.calculate_entropy() < 0.1 else "partial"
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
            "detailed_logs": logger.detailed_logs[-50:],
            "safety_flags": 0,
            "consent_active": "ConsentGlyph" in self.glyphs,
            "path2_stats": {
                "system_state": self.decision_maker._classify_system_state(self.calculate_entropy()),
                "imperfect_glyphs": self.decision_maker._count_imperfect_glyphs(),
                "unconnected_glyphs": self.decision_maker._count_unconnected_glyphs(),
                "consecutive_same_decisions": self.decision_maker.consecutive_same_decisions,
                "last_decision": self.decision_maker.last_decision,
                "time_since_last_intervention": self.decision_maker._time_since_last_intervention()
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Global instances
logger = DetailedLogger()
engine = GlyphwheelEngine()

# Import the full HTML interface from web_interface.py
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
        elif parsed_path.path == '/api/detailed_logs':
            self.serve_json({
                "logs": logger.detailed_logs[-100:],
                "total_logs": len(logger.detailed_logs)
            })
        elif parsed_path.path == '/api/idle_status':
            self.serve_json(self._get_idle_status())
        elif parsed_path.path == '/api/decision_history':
            self.serve_json({
                "recent_decisions": engine.decision_maker.decision_history[-10:],
                "total_decisions": len(engine.decision_maker.decision_history)
            })
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
        elif parsed_path.path == '/api/optimization_stress_test':
            # PATH 2: New endpoint for optimization stress tests
            intensity = data.get('intensity', 0.6)
            duration = data.get('duration', 120)
            result = engine.optimization_stress_test(intensity, duration)
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
        elif parsed_path.path == '/api/deep_recalibration':
            system_state = engine.get_system_status()
            result = deep_recalibration(system_state)
            self.serve_json(result)
        elif parsed_path.path == '/api/idle_control':
            action = data.get('action', '')
            if action == 'start':
                engine.idle_monitor.start_monitoring()
                self.serve_json({"status": "success", "message": "PATH 2 monitoring started"})
            elif action == 'stop':
                engine.idle_monitor.stop_monitoring()
                self.serve_json({"status": "success", "message": "Monitoring stopped"})
            else:
                self.serve_json({"status": "error", "message": "Invalid action"})
        else:
            self.send_error(404)
    
    def _get_idle_status(self):
        """Get current idle monitoring status"""
        if not engine.idle_monitor.is_running:
            return {"status": "stopped", "idle_duration": 0}
            
        current_time = time.time()
        idle_duration = current_time - (engine.idle_monitor.idle_start_time or current_time)
        
        return {
            "status": "running",
            "idle_duration_minutes": round(idle_duration / 60, 2),
            "decay_rate": engine.idle_monitor.decay_rate,
            "monitor_interval": engine.idle_monitor.monitor_interval,
            "system_state": engine.decision_maker._classify_system_state(engine.calculate_entropy())
        }
    
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
🚀 PATH 2: GLYPHWHEEL TWO-STAGE INTELLIGENCE! 🚀

Your ENHANCED Glyphwheel system is now live at:
👉 http://localhost:{port}

PATH 2 FEATURES:
🚨 Stage 1: Emergency Stabilization
   ✅ Critical/Emergency/Unstable state detection
   ✅ Rapid response with recovery cycles
   ✅ Override hysteresis for extreme entropy

🎯 Stage 2: Optimization Passes  
   ✅ Stable-but-suboptimal state detection
   ✅ Optimization stress tests with connection focus
   ✅ Connection building for unconnected glyphs
   ✅ Gentle stabilization for fine-tuning

🔧 Enhanced Decision Logic:
   ✅ System state classification (7 states)
   ✅ Context-aware intervention selection
   ✅ Anti-repetition with smart scoring
   ✅ Periodic status reports every 5 minutes

TWO-STAGE AUTONOMOUS INTELLIGENCE ACTIVE! 🎉

Press Ctrl+C to stop the server
""")
            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                print("💡 If browser didn't open, manually go to the URL above")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 PATH 2 Glyphwheel Engine shutting down gracefully...")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    import sys
    
    port = 8080
    if '--port' in sys.argv:
        try:
            port_idx = sys.argv.index('--port')
            port = int(sys.argv[port_idx + 1])
        except (ValueError, IndexError):
            print("Invalid port number. Using default port 8080.")
    
    print("🔄 Initializing PATH 2 Glyphwheel with Two-Stage Intelligence...")
    
    # Add some initial dynamic glyphs for demonstration
    engine.add_glyph("unstable_Φ", 0.45, "dynamic")
    engine.add_glyph("chaos_Ξ", 0.38, "dynamic")  
    engine.add_glyph("harmony_Ψ", 0.62, "dynamic")
    
    print("✅ PATH 2 system initialized - Emergency + Optimization intelligence!")
    print("🚀 Starting web server...")
    
    run_server(port)

if __name__ == "__main__":
    main()
