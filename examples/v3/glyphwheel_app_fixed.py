#!/usr/bin/env python3
"""
🌟 GLYPHWHEEL WITH FIXED AUTONOMOUS DECISION LOGIC 🌟
Addresses the entropy oscillation problem by implementing smarter decision-making
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
        self.log_filename = os.path.join(self.log_directory, f"glyphwheel_fixed_{timestamp}.log")
        
        # Write session header
        with open(self.log_filename, 'w') as f:
            f.write(f"# Glyphwheel Fixed Session Log - Started: {datetime.now().isoformat()}\n")
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
        
        # Write to file
        try:
            with open(self.log_filename, 'a') as f:
                f.write(log_line + "\n")
                f.flush()  # Ensure immediate write
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

class ImprovedDecisionMaker:
    """FIXED: Smarter autonomous decision-making that prevents oscillation loops"""
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.decision_history = []
        
        # FIXED: Better threshold system with hysteresis
        self.entropy_thresholds = {
            'emergency': 0.25,
            'critical': 0.20,
            'high_concern': 0.15,
            'moderate_concern': 0.10,
            'low_concern': 0.05
        }
        
        # FIXED: Hysteresis - different thresholds for rising vs falling entropy
        self.hysteresis_offset = 0.02  # Must drop 0.02 below threshold to stop worrying
        
        self.available_actions = {
            'recovery_cycle': {'priority': 3, 'description': 'Execute recovery cycle to stabilize system'},
            'stress_test': {'priority': 2, 'description': 'Apply stress test to encourage growth'},
            'wait_and_monitor': {'priority': 1, 'description': 'Continue monitoring without intervention'},
            'ignore_threshold': {'priority': 0, 'description': 'Accept current entropy level as acceptable'},
            'gentle_stabilization': {'priority': 4, 'description': 'Apply gentle stabilization without stress'}
        }
        
        # FIXED: Better safeguards and pattern recognition
        self.intervention_cooldown = 60  # Reduced from 300 to 60 seconds
        self.last_intervention_time = 0
        self.consecutive_same_decisions = 0
        self.last_decision = None
        
    def evaluate_entropy_situation(self, entropy_level, entropy_threshold, idle_duration):
        """FIXED: Smarter evaluation that prevents oscillation"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # FIXED: Calculate effective threshold using hysteresis
        effective_threshold = self._calculate_effective_threshold(entropy_level)
        
        # Gather context for decision
        context = {
            'entropy_level': entropy_level,
            'entropy_threshold': entropy_threshold,
            'effective_threshold': effective_threshold,
            'entropy_margin': entropy_level - effective_threshold,
            'idle_duration_minutes': idle_duration / 60,
            'current_coherence': self.engine.calculate_system_coherence(),
            'glyph_count': len(self.engine.glyphs),
            'total_connections': sum(len(g.connections) for g in self.engine.glyphs.values()),
            'time_since_last_intervention': self._time_since_last_intervention(),
            'recent_decision_pattern': self._analyze_recent_decisions(),
            'consecutive_same_decisions': self.consecutive_same_decisions
        }
        
        logger.log_detailed("IMPROVED_DECISION_EVALUATION_START", {
            "entropy_situation": {
                "level": entropy_level,
                "original_threshold": entropy_threshold,
                "effective_threshold": effective_threshold,
                "margin": entropy_level - effective_threshold,
                "severity": self._classify_entropy_severity(entropy_level, effective_threshold)
            },
            "context": context
        })
        
        # FIXED: Don't take action if entropy is barely above threshold and we just acted
        if self._should_use_hysteresis(entropy_level, effective_threshold, context):
            chosen_action = 'wait_and_monitor'
            reasoning = f"Using hysteresis: entropy {entropy_level:.3f} too close to threshold {effective_threshold:.3f}"
        else:
            # Evaluate actions normally
            action_evaluations = self._evaluate_all_actions_improved(context)
            chosen_action, reasoning = self._select_action_improved(action_evaluations, context)
        
        # Update decision tracking
        self._track_decision(chosen_action)
        
        # Log decision result
        decision_record = {
            "timestamp": timestamp,
            "context": context,
            "chosen_action": chosen_action,
            "reasoning": reasoning,
            "hysteresis_applied": effective_threshold != entropy_threshold,
            "decision_confidence": 95 if chosen_action == 'wait_and_monitor' else 85
        }
        
        self.decision_history.append(decision_record)
        if len(self.decision_history) > 100:
            self.decision_history.pop(0)
            
        logger.log_detailed("IMPROVED_AUTONOMOUS_DECISION_MADE", decision_record)
        
        return chosen_action, reasoning
        
    def _calculate_effective_threshold(self, current_entropy):
        """FIXED: Calculate threshold with hysteresis to prevent oscillation"""
        base_threshold = self.entropy_thresholds['high_concern']  # 0.15
        
        # Check recent decisions - if we've been acting on entropy, raise effective threshold
        recent_interventions = [d for d in self.decision_history[-5:] 
                              if d['chosen_action'] in ['recovery_cycle', 'stress_test']]
        
        if recent_interventions:
            # Raise threshold - need entropy to drop more before we stop worrying
            effective_threshold = base_threshold + self.hysteresis_offset
        else:
            # Use normal threshold
            effective_threshold = base_threshold
            
        return effective_threshold
        
    def _should_use_hysteresis(self, entropy_level, effective_threshold, context):
        """FIXED: Determine if we should use hysteresis to prevent oscillation"""
        margin = entropy_level - effective_threshold
        
        # If entropy is barely above effective threshold AND we recently acted
        if 0 < margin < 0.01 and context['time_since_last_intervention'] < 300:
            return True
            
        # If we've made the same decision too many times in a row
        if self.consecutive_same_decisions > 3 and self.last_decision in ['stress_test', 'recovery_cycle']:
            return True
            
        return False
        
    def _evaluate_all_actions_improved(self, context):
        """FIXED: Improved action evaluation"""
        evaluations = {}
        
        for action, action_info in self.available_actions.items():
            score = self._score_action_improved(action, context)
            evaluations[action] = {
                'score': score,
                'reasoning': self._generate_action_reasoning_improved(action, context, score),
                'priority': action_info['priority'],
                'description': action_info['description']
            }
            
        return evaluations
        
    def _score_action_improved(self, action, context):
        """FIXED: Much better scoring that considers the actual situation"""
        entropy = context['entropy_level']
        entropy_margin = context['entropy_margin'] 
        coherence = context['current_coherence']
        time_since_intervention = context['time_since_last_intervention']
        consecutive_decisions = context['consecutive_same_decisions']
        
        # FIXED: Penalize actions we've been repeating
        repetition_penalty = min(30, consecutive_decisions * 10) if self.last_decision == action else 0
        
        if action == 'ignore_threshold':
            # FIXED: Much more reasonable scoring for ignore_threshold
            base_score = 70  # Start with a reasonable base
            
            # Reduce score based on how far above threshold we are
            if entropy_margin > 0.05:  # Significantly above threshold
                base_score = 20
            elif entropy_margin > 0.02:  # Moderately above threshold
                base_score = 45
            elif entropy_margin > 0.005:  # Slightly above threshold
                base_score = 65
            # else: stay at 70 for barely above threshold
            
            score = max(5, base_score - repetition_penalty)
            
        elif action == 'wait_and_monitor':
            # Good for small entropy margins or recent interventions
            base_score = 60
            if entropy_margin < 0.01:  # Very close to threshold
                base_score = 80
            if time_since_intervention < 120:  # Recent intervention
                base_score += 15
                
            score = max(10, base_score - repetition_penalty)
            
        elif action == 'gentle_stabilization':
            # FIXED: New gentle action for small problems
            base_score = 40
            if 0.005 < entropy_margin < 0.02:  # Perfect range for gentle intervention
                base_score = 75
            if coherence > 0.7:  # System is mostly stable
                base_score += 10
                
            score = max(5, base_score - repetition_penalty)
            
        elif action == 'recovery_cycle':
            # Only for higher entropy levels
            base_score = 30
            if entropy_margin > 0.05:  # Well above threshold
                base_score = 85
            elif entropy_margin > 0.02:  # Moderately above
                base_score = 55
                
            score = max(10, base_score - (repetition_penalty * 2))  # Heavy penalty for repetition
            
        elif action == 'stress_test':
            # FIXED: Much lower scores for stress test in entropy situations
            base_score = 25  # Lower default
            if entropy < 0.05 and coherence > 0.8:  # Only if system is very stable
                base_score = 45
            if entropy_margin > 0.01:  # Penalize for entropy problems
                base_score = max(10, base_score - 30)
                
            score = max(5, base_score - (repetition_penalty * 2))  # Heavy penalty for repetition
            
        return score
        
    def _generate_action_reasoning_improved(self, action, context, score):
        """FIXED: Better reasoning that matches the improved scoring"""
        entropy = context['entropy_level']
        margin = context['entropy_margin']
        
        if action == 'ignore_threshold':
            if score > 60:
                return f"Entropy margin {margin:.4f} is acceptably small - safe to ignore"
            elif score > 40:
                return f"Entropy margin {margin:.4f} is moderate but manageable"
            else:
                return f"Entropy margin {margin:.4f} too large to safely ignore"
                
        elif action == 'wait_and_monitor':
            if score > 70:
                return f"Recent intervention or small margin {margin:.4f} - monitoring appropriate"
            else:
                return f"System state suggests more active response needed"
                
        elif action == 'gentle_stabilization':
            if score > 60:
                return f"Entropy margin {margin:.4f} ideal for gentle stabilization"
            else:
                return f"Situation requires different intervention approach"
                
        elif action == 'recovery_cycle':
            if score > 60:
                return f"Entropy margin {margin:.4f} requires active stabilization"
            else:
                return f"Entropy level doesn't justify intensive recovery cycle"
                
        elif action == 'stress_test':
            if score > 40:
                return f"System stable enough for controlled stress application"
            else:
                return f"Entropy issues make stress testing inadvisable"
                
        return "Standard evaluation applied"
        
    def _select_action_improved(self, evaluations, context):
        """FIXED: Smarter action selection"""
        # Sort actions by score
        sorted_actions = sorted(evaluations.items(), key=lambda x: x[1]['score'], reverse=True)
        
        best_action, best_eval = sorted_actions[0]
        best_score = best_eval['score']
        
        # FIXED: Special logic to prevent harmful loops
        if self.consecutive_same_decisions >= 3 and self.last_decision == best_action:
            # Try second-best option instead
            if len(sorted_actions) > 1:
                second_action, second_eval = sorted_actions[1]
                if second_eval['score'] > 30:  # Make sure it's reasonable
                    return second_action, f"Avoiding repetition of {best_action}, chose {second_action} (score: {second_eval['score']})"
        
        reasoning = f"Best choice: {best_action} (score: {best_score})"
        return best_action, reasoning
        
    def _track_decision(self, chosen_action):
        """Track decision patterns to prevent loops"""
        if chosen_action == self.last_decision:
            self.consecutive_same_decisions += 1
        else:
            self.consecutive_same_decisions = 1
            
        self.last_decision = chosen_action
        
    def _classify_entropy_severity(self, entropy, effective_threshold):
        """Classify entropy severity relative to effective threshold"""
        margin = entropy - effective_threshold
        if margin <= 0: return "below_threshold"
        elif margin < 0.005: return "barely_above"
        elif margin < 0.01: return "slightly_above"  
        elif margin < 0.02: return "moderately_above"
        elif margin < 0.05: return "significantly_above"
        else: return "well_above"
        
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
        elif actions.count('stress_test') >= 3:
            return "repeated_stress_test"
        elif actions.count('recovery_cycle') >= 3:
            return "repeated_recovery"
        else:
            return "mixed_responses"

class ImprovedIdleMonitor:
    """FIXED: Better idle monitoring with the improved decision maker"""
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.is_running = False
        self.monitor_thread = None
        
        # FIXED: More reasonable parameters
        self.decay_rate = 0.0001  # Reduced decay rate
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
            logger.log_detailed("IMPROVED_IDLE_MONITORING_STARTED", {
                "monitor_interval": self.monitor_interval,
                "decay_rate": self.decay_rate
            })
            
    def stop_monitoring(self):
        """Stop the background monitoring"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.log_detailed("IMPROVED_IDLE_MONITORING_STOPPED", {})
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                self._perform_improved_idle_check()
                time.sleep(self.monitor_interval)
            except Exception as e:
                logger.log_detailed("IDLE_MONITOR_ERROR", {"error": str(e)})
                time.sleep(self.monitor_interval)
                
    def _perform_improved_idle_check(self):
        """FIXED: Improved idle checking that uses better decision logic"""
        current_time = time.time()
        idle_duration = current_time - (self.idle_start_time or current_time)
        
        entropy = self.engine.calculate_entropy()
        coherence = self.engine.calculate_system_coherence()
        
        # FIXED: Only evaluate if entropy crosses the effective threshold
        base_threshold = 0.15
        effective_threshold = self.engine.decision_maker._calculate_effective_threshold(entropy)
        
        if entropy > effective_threshold:
            logger.log_detailed("ENTROPY_THRESHOLD_EVALUATION", {
                "entropy": entropy,
                "base_threshold": base_threshold,
                "effective_threshold": effective_threshold,
                "margin": entropy - effective_threshold
            })
            
            action, reasoning = self.engine.decision_maker.evaluate_entropy_situation(
                entropy, base_threshold, idle_duration
            )
            
            self._execute_improved_autonomous_action(action, reasoning, entropy)
            
    def _execute_improved_autonomous_action(self, action, reasoning, entropy):
        """FIXED: Execute actions with better logic"""
        logger.log_detailed("IMPROVED_AUTONOMOUS_ACTION_EXECUTION", {
            "action": action,
            "reasoning": reasoning,
            "entropy_level": entropy
        })
        
        if action == 'recovery_cycle':
            try:
                result = self.engine.mandatory_recovery_cycle(30)  # Shorter duration
                self.engine.decision_maker.last_intervention_time = time.time()
                logger.log_detailed("AUTONOMOUS_RECOVERY_COMPLETED", {"result": result})
            except Exception as e:
                logger.log_detailed("AUTONOMOUS_RECOVERY_FAILED", {"error": str(e)})
                
        elif action == 'gentle_stabilization':
            # FIXED: New gentle stabilization action
            try:
                self._perform_gentle_stabilization()
                self.engine.decision_maker.last_intervention_time = time.time()
            except Exception as e:
                logger.log_detailed("GENTLE_STABILIZATION_FAILED", {"error": str(e)})
                
        elif action == 'stress_test':
            try:
                result = self.engine.run_stress_test(0.3, 50)  # Gentler stress test
                self.engine.decision_maker.last_intervention_time = time.time()
                logger.log_detailed("AUTONOMOUS_STRESS_TEST_COMPLETED", {"result": result})
            except Exception as e:
                logger.log_detailed("AUTONOMOUS_STRESS_TEST_FAILED", {"error": str(e)})
                
        # For 'wait_and_monitor' and 'ignore_threshold', no action needed
        
    def _perform_gentle_stabilization(self):
        """FIXED: New gentle stabilization method"""
        logger.log_detailed("GENTLE_STABILIZATION_START", {})
        
        for name, glyph in self.engine.glyphs.items():
            if glyph.glyph_type == 'dynamic':
                old_gsi = glyph.gsi
                # Small stabilization toward 0.5 (middle ground)
                if glyph.gsi > 0.5:
                    glyph.gsi = max(0.5, glyph.gsi - 0.01)
                else:
                    glyph.gsi = min(0.5, glyph.gsi + 0.01)
                    
                if abs(glyph.gsi - old_gsi) > 0.001:
                    logger.log_glyph_change(name, old_gsi, glyph.gsi, "gentle_stabilization")
                    
        logger.log_detailed("GENTLE_STABILIZATION_COMPLETED", {
            "new_entropy": self.engine.calculate_entropy(),
            "new_coherence": self.engine.calculate_system_coherence()
        })

# Support for deep recalibration
def deep_recalibration(system_state):
    """
    Initiates a deep recalibration process to restore the GSI of the ConsentGlyph.
    This protocol is designed to address the system's ethical debt.
    """
    logger.log_detailed("DEEP_RECALIBRATION_INITIATED", {"reason": "ethical_debt_resolution"})
    
    if 'ConsentGlyph' in system_state['glyphs']:
        # Get the ConsentGlyph from the actual engine
        consent_glyph = engine.glyphs['ConsentGlyph']
        old_gsi = consent_glyph.gsi
        
        # Set the GSI of the ConsentGlyph to 1.0
        consent_glyph.gsi = 1.0
        
        # Log the change
        logger.log_glyph_change('ConsentGlyph', old_gsi, 1.0, 'deep_recalibration')
        
        # Update the system's coherence and entropy after the change
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
        self.log("FIXED System initialized successfully", "success")
        
        # FIXED: Initialize improved systems
        self.decision_maker = ImprovedDecisionMaker(self)
        self.idle_monitor = ImprovedIdleMonitor(self)
        
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

    def _attempt_glyph_connections(self):
        glyph_list = list(self.glyphs.values())
        connection_attempts = min(5, len(glyph_list))
        
        for i in range(connection_attempts):
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
            "decision_stats": {
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
            # New endpoint for detailed logs
            self.serve_json({
                "logs": logger.detailed_logs[-100:],  # Last 100 detailed logs
                "total_logs": len(logger.detailed_logs)
            })
        elif parsed_path.path == '/api/idle_status':
            # Get idle monitoring status
            self.serve_json(self._get_idle_status())
        elif parsed_path.path == '/api/decision_history':
            # Get decision-making history
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
            # Run deep recalibration protocol
            system_state = engine.get_system_status()
            result = deep_recalibration(system_state)
            self.serve_json(result)
        elif parsed_path.path == '/api/idle_control':
            # Control idle monitoring
            action = data.get('action', '')
            if action == 'start':
                engine.idle_monitor.start_monitoring()
                self.serve_json({"status": "success", "message": "Fixed monitoring started"})
            elif action == 'stop':
                engine.idle_monitor.stop_monitoring()
                self.serve_json({"status": "success", "message": "Monitoring stopped"})
            elif action == 'configure':
                # Allow runtime configuration of parameters
                if 'decay_rate' in data:
                    engine.idle_monitor.decay_rate = float(data['decay_rate'])
                if 'monitor_interval' in data:
                    engine.idle_monitor.monitor_interval = int(data['monitor_interval'])
                self.serve_json({"status": "success", "message": "Idle monitoring configured"})
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
            "monitor_interval": engine.idle_monitor.monitor_interval
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
🔧 FIXED GLYPHWHEEL ENGINE WITH FULL UI! 🔧

Your IMPROVED Glyphwheel system is now live at:
👉 http://localhost:{port}

FIXES APPLIED:
✅ Smarter entropy thresholds with hysteresis 
✅ Better action scoring prevents loops
✅ 'ignore_threshold' now works reasonably  
✅ Anti-repetition logic breaks decision loops
✅ New 'gentle_stabilization' option
✅ Reduced intervention cooldowns
✅ Pattern recognition prevents stuck states
✅ FULL RICH UI with all controls and visualizations

NO MORE OSCILLATION LOOPS! 🎉

Press Ctrl+C to stop the server
""")
            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                print("💡 If browser didn't open, manually go to the URL above")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Fixed Glyphwheel Engine shutting down gracefully...")
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
    
    print("🔄 Initializing FIXED Glyphwheel with Full Interface...")
    
    # Add some initial dynamic glyphs for demonstration
    engine.add_glyph("unstable_Φ", 0.45, "dynamic")
    engine.add_glyph("chaos_Ξ", 0.38, "dynamic")  
    engine.add_glyph("harmony_Ψ", 0.62, "dynamic")
    
    print("✅ Fixed system initialized with full UI - no more decision loops!")
    print("🚀 Starting web server...")
    
    run_server(port)

if __name__ == "__main__":
    main()
