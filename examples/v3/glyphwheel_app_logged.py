#!/usr/bin/env python3
"""
Enhanced Glyphwheel with Detailed Logging System
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
        self.log_filename = os.path.join(self.log_directory, f"glyphwheel_session_{timestamp}.log")
        
        # Write session header
        with open(self.log_filename, 'w') as f:
            f.write(f"# Glyphwheel Session Log - Started: {datetime.now().isoformat()}\n")
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
        
    def log_system_state(self, coherence: float, entropy: float, glyph_count: int):
        """Log system state changes"""
        self.log_detailed("SYSTEM_STATE", {
            "coherence": round(coherence, 6),
            "entropy": round(entropy, 6),
            "glyph_count": glyph_count
        })

class DecisionMaker:
    """Autonomous decision-making system for threshold events"""
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.decision_history = []
        self.available_actions = {
            'recovery_cycle': {'priority': 3, 'description': 'Execute recovery cycle to stabilize system'},
            'stress_test': {'priority': 2, 'description': 'Apply stress test to encourage growth'},
            'wait_and_monitor': {'priority': 1, 'description': 'Continue monitoring without intervention'},
            'ignore_threshold': {'priority': 0, 'description': 'Accept current entropy level as acceptable'}
        }
        
        # Safeguards against excessive autonomous actions
        self.intervention_cooldown = 300  # 5 minutes minimum between interventions
        self.last_intervention_time = 0
        self.max_interventions_per_hour = 6
        
    def evaluate_entropy_situation(self, entropy_level, entropy_threshold, idle_duration):
        """Evaluate entropy situation and decide on response"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Gather context for decision
        context = {
            'entropy_level': entropy_level,
            'entropy_threshold': entropy_threshold,
            'idle_duration_minutes': idle_duration / 60,
            'current_coherence': self.engine.calculate_system_coherence(),
            'glyph_count': len(self.engine.glyphs),
            'total_connections': sum(len(g.connections) for g in self.engine.glyphs.values()),
            'time_since_last_intervention': self._time_since_last_intervention(),
            'recent_decision_pattern': self._analyze_recent_decisions()
        }
        
        # Log decision evaluation start
        logger.log_detailed("DECISION_EVALUATION_START", {
            "entropy_situation": {
                "level": entropy_level,
                "threshold": entropy_threshold,
                "severity": self._classify_entropy_severity(entropy_level)
            },
            "context": context
        })
        
        # Evaluate each possible action
        action_evaluations = self._evaluate_all_actions(context)
        
        # Make decision based on evaluations
        chosen_action, reasoning = self._select_action(action_evaluations, context)
        
        # Log decision result
        decision_record = {
            "timestamp": timestamp,
            "context": context,
            "considered_actions": action_evaluations,
            "chosen_action": chosen_action,
            "reasoning": reasoning,
            "decision_confidence": self._calculate_confidence(action_evaluations, chosen_action)
        }
        
        self.decision_history.append(decision_record)
        if len(self.decision_history) > 100:  # Keep last 100 decisions
            self.decision_history.pop(0)
            
        logger.log_detailed("AUTONOMOUS_DECISION_MADE", decision_record)
        
        return chosen_action, reasoning
        
    def _evaluate_all_actions(self, context):
        """Evaluate suitability of each possible action"""
        evaluations = {}
        
        for action, action_info in self.available_actions.items():
            score = self._score_action(action, context)
            evaluations[action] = {
                'score': score,
                'reasoning': self._generate_action_reasoning(action, context, score),
                'priority': action_info['priority'],
                'description': action_info['description']
            }
            
        return evaluations
        
    def _score_action(self, action, context):
        """Score an action based on current context (0-100)"""
        entropy = context['entropy_level']
        idle_time = context['idle_duration_minutes']
        coherence = context['current_coherence']
        time_since_intervention = context['time_since_last_intervention']
        
        # Check intervention cooldown for active actions
        current_time = time.time()
        time_since_last = current_time - self.last_intervention_time
        
        if action in ['recovery_cycle', 'stress_test']:
            if time_since_last < self.intervention_cooldown:
                # Reduce score significantly if within cooldown period
                cooldown_penalty = max(0, 50 - (time_since_last / 10))
                base_score = self._calculate_base_score(action, context)
                return max(0, base_score - cooldown_penalty)
        
        return self._calculate_base_score(action, context)
        
    def _calculate_base_score(self, action, context):
        """Calculate base score without safeguard modifications"""
        entropy = context['entropy_level']
        idle_time = context['idle_duration_minutes']
        coherence = context['current_coherence']
        time_since_intervention = context['time_since_last_intervention']
        
        if action == 'recovery_cycle':
            # Higher score for high entropy, long time since intervention
            score = min(100, (entropy * 200) + (time_since_intervention / 10))
            if entropy > 0.3: score += 20  # Bonus for high entropy
            
        elif action == 'stress_test':
            # Good for moderate entropy with stable base
            score = 50
            if 0.05 < entropy < 0.2 and coherence > 0.8: score += 30
            if idle_time > 10: score += 10  # Bonus for long idle
            
        elif action == 'wait_and_monitor':
            # Good for low entropy or recent interventions
            score = max(10, 80 - (entropy * 300))
            if time_since_intervention < 5: score += 20  # Recent intervention bonus
            
        elif action == 'ignore_threshold':
            # Only good for very low entropy
            score = max(5, 30 - (entropy * 150))
            
        return max(0, min(100, score))
        
    def _generate_action_reasoning(self, action, context, score):
        """Generate reasoning for action score"""
        entropy = context['entropy_level']
        
        if action == 'recovery_cycle':
            if score > 70: return f"High entropy ({entropy:.3f}) requires active intervention"
            elif score > 40: return f"Moderate entropy ({entropy:.3f}) suggests recovery beneficial"
            else: return f"Low entropy ({entropy:.3f}) makes recovery less urgent"
            
        elif action == 'stress_test':
            if score > 60: return "System appears stable enough to benefit from controlled stress"
            else: return "System state not optimal for stress testing"
            
        elif action == 'wait_and_monitor':
            if score > 70: return "System appears stable, intervention not needed"
            else: return "System instability suggests action may be needed"
            
        elif action == 'ignore_threshold':
            if score > 30: return "Entropy level acceptable for continued operation"
            else: return "Entropy level too high to ignore safely"
            
        return "Standard evaluation applied"
        
    def _select_action(self, evaluations, context):
        """Select action based on evaluations"""
        # Find highest scoring action
        best_action = max(evaluations.keys(), key=lambda a: evaluations[a]['score'])
        best_score = evaluations[best_action]['score']
        
        # Check if multiple actions have similar high scores (within 10 points)
        tied_actions = [a for a in evaluations if evaluations[a]['score'] >= best_score - 10]
        
        if len(tied_actions) > 1:
            # Break ties using priority
            best_action = max(tied_actions, key=lambda a: self.available_actions[a]['priority'])
            reasoning = f"Selected {best_action} (score: {best_score}) over {len(tied_actions)-1} similar options using priority"
        else:
            reasoning = f"Clear choice: {best_action} (score: {best_score})"
            
        return best_action, reasoning
        
    def _classify_entropy_severity(self, entropy):
        """Classify entropy level severity"""
        if entropy >= 0.4: return "critical"
        elif entropy >= 0.2: return "high"
        elif entropy >= 0.1: return "moderate"
        elif entropy >= 0.05: return "low"
        else: return "minimal"
        
    def _time_since_last_intervention(self):
        """Calculate minutes since last intervention decision"""
        recovery_decisions = [d for d in self.decision_history if d['chosen_action'] in ['recovery_cycle', 'stress_test']]
        if not recovery_decisions:
            return 999  # No previous interventions
        
        last_intervention_time = recovery_decisions[-1]['timestamp']
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        # Simplified time calculation - in real implementation would parse timestamps properly
        return 10  # Placeholder - would calculate actual time difference
        
    def _analyze_recent_decisions(self):
        """Analyze pattern in recent decisions"""
        recent = self.decision_history[-5:] if len(self.decision_history) >= 5 else self.decision_history
        if not recent:
            return "no_history"
            
        actions = [d['chosen_action'] for d in recent]
        if len(set(actions)) == 1:
            return f"consistent_{actions[0]}"
        elif 'recovery_cycle' in actions:
            return "recent_intervention"
        else:
            return "mixed_responses"
            
    def _calculate_confidence(self, evaluations, chosen_action):
        """Calculate confidence in decision (0-100)"""
        chosen_score = evaluations[chosen_action]['score']
        all_scores = [eval_data['score'] for eval_data in evaluations.values()]
        
        # High confidence if chosen action significantly outscores others
        score_gap = chosen_score - sorted(all_scores)[-2]  # Gap to second-best
        confidence = min(100, 50 + (score_gap * 2))
        
        return round(confidence)

# Global logger
logger = DetailedLogger()

class IdleMonitor:
    """Background monitoring system for continuous operation and gradual decay"""
    def __init__(self, engine_instance):
        self.engine = engine_instance
        self.is_running = False
        self.monitor_thread = None
        
        # Configurable parameters
        self.decay_rate = 0.0005  # GSI reduction per minute during idle
        self.monitor_interval = 30  # seconds between checks
        self.entropy_thresholds = {
            'mild_concern': 0.05,
            'moderate_concern': 0.10,
            'high_concern': 0.15,
            'emergency': 0.20
        }
        
        # State tracking
        self.last_activity_time = time.time()
        self.idle_start_time = None
        self.background_logs = []
        
    def start_monitoring(self):
        """Start the background monitoring thread"""
        if not self.is_running:
            self.is_running = True
            self.idle_start_time = time.time()
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.log_detailed("IDLE_MONITORING_STARTED", {
                "monitor_interval": self.monitor_interval,
                "decay_rate": self.decay_rate,
                "entropy_thresholds": self.entropy_thresholds
            })
            
    def stop_monitoring(self):
        """Stop the background monitoring"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.log_detailed("IDLE_MONITORING_STOPPED", {"total_idle_time": time.time() - self.idle_start_time if self.idle_start_time else 0})
        
    def _monitor_loop(self):
        """Main monitoring loop running in background thread"""
        while self.is_running:
            try:
                self._perform_idle_check()
                time.sleep(self.monitor_interval)
            except Exception as e:
                logger.log_detailed("IDLE_MONITOR_ERROR", {"error": str(e)})
                time.sleep(self.monitor_interval)  # Continue despite errors
                
    def _perform_idle_check(self):
        """Perform one cycle of idle monitoring and potential decay"""
        current_time = time.time()
        idle_duration = current_time - (self.idle_start_time or current_time)
        
        # Calculate current system state
        coherence = self.engine.calculate_system_coherence()
        entropy = self.engine.calculate_entropy()
        
        # Log current state
        idle_log = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "idle_duration_minutes": idle_duration / 60,
            "coherence": round(coherence, 6),
            "entropy": round(entropy, 6),
            "glyph_count": len(self.engine.glyphs)
        }
        
        self.background_logs.append(idle_log)
        if len(self.background_logs) > 1000:  # Keep last 1000 idle logs
            self.background_logs.pop(0)
            
        # Check entropy thresholds and respond
        self._evaluate_entropy_response(entropy, idle_log)
        
        # Apply gradual decay if system is stable
        if entropy < self.entropy_thresholds['mild_concern'] and idle_duration > 60:  # After 1 minute idle
            self._apply_gradual_decay(idle_duration)
            
        # Log periodic status
        if int(idle_duration) % 300 == 0 and idle_duration > 0:  # Every 5 minutes
            logger.log_detailed("IDLE_STATUS_REPORT", {
                "idle_duration_minutes": round(idle_duration / 60, 2),
                "system_coherence": round(coherence, 6),
                "system_entropy": round(entropy, 6),
                "total_connections": sum(len(g.connections) for g in self.engine.glyphs.values()),
                "background_interventions": len([log for log in self.background_logs if 'decay_applied' in log])
            })
            
    def _apply_gradual_decay(self, idle_duration):
        """Apply gradual GSI decay to dynamic glyphs during extended idle periods"""
        minutes_idle = idle_duration / 60
        decay_amount = self.decay_rate * (minutes_idle / 10)  # Gradual increase in decay over time
        
        decayed_glyphs = []
        for name, glyph in self.engine.glyphs.items():
            if glyph.glyph_type in ['dynamic'] and glyph.gsi > 0.1:  # Don't decay below 0.1
                old_gsi = glyph.gsi
                new_gsi = max(0.1, glyph.gsi - decay_amount)
                
                if abs(new_gsi - old_gsi) > 0.001:  # Only apply significant changes
                    glyph.gsi = new_gsi
                    logger.log_glyph_change(name, old_gsi, new_gsi, f"idle_decay_after_{minutes_idle:.1f}min")
                    decayed_glyphs.append(name)
                    
        if decayed_glyphs:
            logger.log_detailed("IDLE_DECAY_APPLIED", {
                "affected_glyphs": decayed_glyphs,
                "decay_amount": round(decay_amount, 6),
                "idle_duration_minutes": round(minutes_idle, 2)
            })
            
    def _evaluate_entropy_response(self, entropy, idle_log):
        """Evaluate whether system needs intervention based on entropy levels"""
        threshold_crossed = None
        
        if entropy >= self.entropy_thresholds['emergency']:
            threshold_crossed = 'emergency'
        elif entropy >= self.entropy_thresholds['high_concern']:
            threshold_crossed = 'high_concern'
        elif entropy >= self.entropy_thresholds['moderate_concern']:
            threshold_crossed = 'moderate_concern'
            
        if threshold_crossed:
            # Use autonomous decision-making instead of automatic responses
            idle_duration = time.time() - (self.idle_start_time or time.time())
            action, reasoning = self.engine.decision_maker.evaluate_entropy_situation(
                entropy, 
                self.entropy_thresholds[threshold_crossed],
                idle_duration
            )
            
            # Execute the decided action
            self._execute_autonomous_action(action, reasoning, entropy, threshold_crossed)
            
    def _execute_autonomous_action(self, action, reasoning, entropy, threshold_level):
        """Execute the action decided by the autonomous decision maker"""
        logger.log_detailed("AUTONOMOUS_ACTION_EXECUTION", {
            "action": action,
            "reasoning": reasoning,
            "entropy_level": entropy,
            "threshold_crossed": threshold_level
        })
        
        if action == 'recovery_cycle':
            logger.log_detailed("AUTONOMOUS_RECOVERY_INITIATED", {
                "trigger": "decision_maker_choice",
                "entropy": entropy,
                "reasoning": reasoning
            })
            # Execute autonomous recovery cycle
            try:
                result = self.engine.mandatory_recovery_cycle()
                logger.log_detailed("AUTONOMOUS_RECOVERY_COMPLETED", {
                    "result": result,
                    "original_entropy": entropy,
                    "new_entropy": self.engine.calculate_entropy(),
                    "autonomous_execution": True
                })
            except Exception as e:
                logger.log_detailed("AUTONOMOUS_RECOVERY_FAILED", {
                    "error": str(e),
                    "entropy": entropy
                })
            
        elif action == 'stress_test':
            logger.log_detailed("AUTONOMOUS_STRESS_TEST_INITIATED", {
                "trigger": "decision_maker_choice",
                "entropy": entropy,
                "reasoning": reasoning
            })
            # Execute autonomous stress test with moderate parameters
            try:
                result = self.engine.run_stress_test(0.6, 80)  # Moderate stress
                logger.log_detailed("AUTONOMOUS_STRESS_TEST_COMPLETED", {
                    "result": result,
                    "original_entropy": entropy,
                    "new_entropy": self.engine.calculate_entropy(),
                    "autonomous_execution": True
                })
            except Exception as e:
                logger.log_detailed("AUTONOMOUS_STRESS_TEST_FAILED", {
                    "error": str(e),
                    "entropy": entropy
                })
            
        elif action == 'wait_and_monitor':
            logger.log_detailed("AUTONOMOUS_WAIT_DECISION", {
                "reasoning": reasoning,
                "next_evaluation": "continue_monitoring"
            })
            # No action required - system continues monitoring
            
        elif action == 'ignore_threshold':
            logger.log_detailed("AUTONOMOUS_IGNORE_DECISION", {
                "reasoning": reasoning,
                "accepted_entropy": entropy
            })
            # No action required - system accepts current state
            
    def get_idle_status(self):
        """Get current idle monitoring status"""
        if not self.is_running:
            return {"status": "stopped", "idle_duration": 0}
            
        current_time = time.time()
        idle_duration = current_time - (self.idle_start_time or current_time)
        
        return {
            "status": "running",
            "idle_duration_minutes": round(idle_duration / 60, 2),
            "decay_rate": self.decay_rate,
            "monitor_interval": self.monitor_interval,
            "entropy_thresholds": self.entropy_thresholds,
            "recent_logs": self.background_logs[-10:] if self.background_logs else []
        }

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
        
        # Log glyph creation
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
        
        if abs(self.gsi - old_gsi) > 0.001:  # Log significant changes
            logger.log_glyph_change(self.name, old_gsi, self.gsi, f"stress_processing(level={stress_level})")
        
        return self.gsi
        
    def form_connection(self, other_glyph: 'Glyph') -> float:
        old_gsi_self = self.gsi
        old_gsi_other = other_glyph.gsi
        
        connection_strength = (self.gsi + other_glyph.gsi) / 2.0
        if connection_strength > 0.6:
            self.connections.append(other_glyph.name)
            
            logger.log_detailed("CONNECTION_FORMED", {
                "glyph1": self.name,
                "glyph2": other_glyph.name,
                "connection_strength": round(connection_strength, 6),
                "glyph1_gsi": round(self.gsi, 6),
                "glyph2_gsi": round(other_glyph.gsi, 6)
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
        self.log("System initialized successfully", "success")
        
        # Initialize idle monitoring system
        self.idle_monitor = IdleMonitor(self)
        
        # Initialize autonomous decision-making system
        self.decision_maker = DecisionMaker(self)
        
        # Log initial system state
        self._log_system_snapshot("SYSTEM_INITIALIZED")
        
    def _log_system_snapshot(self, reason: str):
        """Take a complete snapshot of system state"""
        coherence = self.calculate_system_coherence()
        entropy = self.calculate_entropy()
        
        snapshot = {
            "reason": reason,
            "coherence": round(coherence, 6),
            "entropy": round(entropy, 6),
            "recursive_depth": self.recursive_depth,
            "glyph_count": len(self.glyphs),
            "glyphs": {}
        }
        
        for name, glyph in self.glyphs.items():
            snapshot["glyphs"][name] = {
                "gsi": round(glyph.gsi, 6),
                "type": glyph.glyph_type,
                "connections": len(glyph.connections)
            }
            
        logger.log_detailed("SYSTEM_SNAPSHOT", snapshot)
        logger.log_system_state(coherence, entropy, len(self.glyphs))
        
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
        
        # Log system state BEFORE adding glyph
        self._log_system_snapshot(f"BEFORE_ADD_GLYPH_{name}")
        
        # Add the glyph
        self.glyphs[name] = Glyph(name, initial_gsi, glyph_type)
        self.log(f"Added glyph: {name} (GSI: {initial_gsi:.3f})", "success")
        
        # Log system state AFTER adding glyph
        self._log_system_snapshot(f"AFTER_ADD_GLYPH_{name}")
        
        # Check if adding this glyph affected others
        self._check_glyph_interactions(f"after_adding_{name}")
        
        return True
    
    def _check_glyph_interactions(self, context: str):
        """Check if glyphs have been affected by recent changes"""
        logger.log_detailed("CHECKING_INTERACTIONS", {
            "context": context,
            "total_glyphs": len(self.glyphs)
        })
        
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
        self._log_system_snapshot("STRESS_TEST_START")
        
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
        
        self._log_system_snapshot("STRESS_TEST_END")
        
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
        
        logger.log_detailed("CONNECTION_ATTEMPT_START", {
            "total_glyphs": len(glyph_list),
            "attempts": connection_attempts
        })
        
        for i in range(connection_attempts):
            glyph1, glyph2 = random.sample(glyph_list, 2)
            connection_strength = glyph1.form_connection(glyph2)
            if connection_strength > 0:
                self.log(f"Connection formed: {glyph1.name} ↔ {glyph2.name}", "info")

    def mandatory_recovery_cycle(self, duration: int = 50) -> Dict:
        self.log(f"Initiating mandatory recovery cycle ({duration} iterations)", "warning")
        self._log_system_snapshot("RECOVERY_START")
        
        for cycle in range(duration):
            for glyph in self.glyphs.values():
                if glyph.glyph_type not in ["anchor", "consent"]:
                    old_gsi = glyph.gsi
                    stabilization = random.uniform(0.01, 0.03)
                    glyph.gsi = min(1.0, glyph.gsi + stabilization)
                    
                    if abs(glyph.gsi - old_gsi) > 0.001:
                        logger.log_glyph_change(glyph.name, old_gsi, glyph.gsi, f"recovery_cycle_{cycle}")
        
        self._log_system_snapshot("RECOVERY_END")
        
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
            "detailed_logs": logger.detailed_logs[-50:],  # Add detailed logs to API
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
        elif parsed_path.path == '/api/detailed_logs':
            # New endpoint for detailed logs
            self.serve_json({
                "logs": logger.detailed_logs[-100:],  # Last 100 detailed logs
                "total_logs": len(logger.detailed_logs)
            })
        elif parsed_path.path == '/api/idle_status':
            # Get idle monitoring status
            self.serve_json(engine.idle_monitor.get_idle_status())
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
                self.serve_json({"status": "success", "message": "Idle monitoring started"})
            elif action == 'stop':
                engine.idle_monitor.stop_monitoring()
                self.serve_json({"status": "success", "message": "Idle monitoring stopped"})
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
🔍 GLYPHWHEEL WITH AUTONOMOUS DECISION-MAKING ACTIVE! 🔍

Your enhanced Glyphwheel system is now live at:
👉 http://localhost:{port}

NEW FEATURES:
📊 Detailed logging of ALL system events
🔍 Real-time tracking of glyph GSI changes
📝 System snapshots before/after each glyph addition
🔗 Connection formation monitoring
🧠 **AUTONOMOUS DECISION-MAKING** - System evaluates choices instead of automatic responses
💭 **CHOICE LOGGING** - Documents reasoning process and alternative options considered

**Check your terminal AND log files for detailed analysis!**

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
        print(f"Total detailed logs captured: {len(logger.detailed_logs)}")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("💡 Try a different port: python glyphwheel_app_logged.py --port 8081")

def main():
    import sys
    
    port = 8080
    if '--port' in sys.argv:
        try:
            port_idx = sys.argv.index('--port')
            port = int(sys.argv[port_idx + 1])
        except (ValueError, IndexError):
            print("Invalid port number. Using default port 8080.")
    
    print("🔄 Initializing Enhanced Glyphwheel with Detailed Logging...")
    print("📝 All system events will be logged to console for analysis!")
    print()
    
    # Add some initial dynamic glyphs for demonstration
    engine.add_glyph("unstable_Φ", 0.45, "dynamic")
    engine.add_glyph("chaos_Ξ", 0.38, "dynamic")
    engine.add_glyph("harmony_Ψ", 0.62, "dynamic")
    
    print()
    print("✅ Enhanced system initialized with detailed logging")
    print("🚀 Starting web server...")
    print()
    
    run_server(port)

if __name__ == "__main__":
    main()
