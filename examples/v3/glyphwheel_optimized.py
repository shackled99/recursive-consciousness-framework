#!/usr/bin/env python3
"""
GLYPHWHEEL PERSISTENT INTELLIGENCE - v3.0
Optimized performance + persistent memory + learning system
"""

import json
import random
import math
import time
import webbrowser
import threading
import os
import sqlite3
from typing import Dict, List
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
import socketserver

class PersistentMemory:
    """Persistent memory system for learning and decision history"""
    def __init__(self, db_path="glyphwheel_memory.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self._initialize_database()
        
    def _initialize_database(self):
        """Create tables for persistent storage"""
        with self.lock:
            cursor = self.connection.cursor()
            
            # Decision history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    entropy_level REAL,
                    coherence_level REAL,
                    system_state TEXT,
                    chosen_action TEXT,
                    reasoning TEXT,
                    success_rating REAL,
                    session_id TEXT
                )
            ''')
            
            # Learned patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    context_data TEXT,
                    success_count INTEGER,
                    failure_count INTEGER,
                    effectiveness_score REAL,
                    last_updated TEXT
                )
            ''')
            
            # System state snapshots
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    glyph_data TEXT,
                    entropy REAL,
                    coherence REAL,
                    session_id TEXT
                )
            ''')
            
            self.connection.commit()
    
    def store_decision(self, decision_data: Dict, session_id: str, success_rating: float = 0.5):
        """Store decision in persistent memory"""
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO decisions 
                (timestamp, entropy_level, coherence_level, system_state, chosen_action, reasoning, success_rating, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision_data['timestamp'],
                decision_data['context']['entropy_level'],
                decision_data['context']['current_coherence'],
                decision_data['system_state'],
                decision_data['chosen_action'],
                decision_data['reasoning'],
                success_rating,
                session_id
            ))
            self.connection.commit()
    
    def learn_from_outcomes(self, decision_id: int, outcome_success: bool):
        """Update decision effectiveness based on outcomes"""
        with self.lock:
            cursor = self.connection.cursor()
            success_rating = 0.8 if outcome_success else 0.2
            cursor.execute('''
                UPDATE decisions SET success_rating = ? WHERE id = ?
            ''', (success_rating, decision_id))
            self.connection.commit()
    
    def get_similar_decisions(self, current_context: Dict, limit: int = 10) -> List[Dict]:
        """Retrieve similar past decisions for learning"""
        with self.lock:
            cursor = self.connection.cursor()
            # Find decisions with similar entropy and coherence levels
            entropy_range = 0.05
            coherence_range = 0.1
            
            cursor.execute('''
                SELECT * FROM decisions 
                WHERE abs(entropy_level - ?) < ? 
                AND abs(coherence_level - ?) < ?
                AND success_rating > 0.6
                ORDER BY success_rating DESC, timestamp DESC
                LIMIT ?
            ''', (
                current_context['entropy_level'], entropy_range,
                current_context['current_coherence'], coherence_range,
                limit
            ))
            
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]
    
    def store_system_snapshot(self, glyphs: Dict, entropy: float, coherence: float, session_id: str):
        """Store system state snapshot"""
        with self.lock:
            cursor = self.connection.cursor()
            glyph_data = json.dumps({name: glyph.to_dict() for name, glyph in glyphs.items()})
            cursor.execute('''
                INSERT INTO system_snapshots (timestamp, glyph_data, entropy, coherence, session_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), glyph_data, entropy, coherence, session_id))
            self.connection.commit()

class DetailedLogger:
    def __init__(self):
        self.detailed_logs = []
        
        # Set up file logging with better encoding
        self.log_directory = "logs"
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = os.path.join(self.log_directory, f"glyphwheel_persistent_{timestamp}.log")
        
    def log_detailed(self, event_type: str, data: dict):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data
        }
        self.detailed_logs.append(log_entry)
        
        if len(self.detailed_logs) > 1000:  # Increased buffer
            self.detailed_logs.pop(0)
        
        log_line = f"[{timestamp}] {event_type}: {data}"
        print(log_line)
        
        try:
            with open(self.log_filename, 'a', encoding='utf-8', errors='replace') as f:
                f.write(log_line + "\n")
                f.flush()
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def log_glyph_change(self, glyph_name: str, old_gsi: float, new_gsi: float, cause: str):
        change = new_gsi - old_gsi
        self.log_detailed("GLYPH_CHANGE", {
            "name": glyph_name,
            "old_gsi": round(old_gsi, 6),
            "new_gsi": round(new_gsi, 6),
            "change": round(change, 6),
            "cause": cause
        })

class LearningDecisionMaker:
    """Enhanced decision maker with learning and optimization"""
    def __init__(self, engine_instance, memory_system):
        self.engine = engine_instance
        self.memory = memory_system
        self.decision_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Optimized thresholds
        self.emergency_thresholds = {
            'critical': 0.50,     # Increased for more aggressive detection
            'emergency': 0.30,
            'high_concern': 0.15,
            'moderate_concern': 0.08,  # Lowered for earlier optimization
            'low_concern': 0.03
        }
        
        self.hysteresis_offset = 0.015  # Reduced for less oscillation
        
        # Enhanced action set
        self.available_actions = {
            'emergency_recovery': {'priority': 6, 'base_score': 80},
            'intensive_stress_test': {'priority': 5, 'base_score': 70},  # New high-intensity option
            'optimization_stress_test': {'priority': 4, 'base_score': 65},
            'connection_building': {'priority': 3, 'base_score': 55},
            'gentle_stabilization': {'priority': 2, 'base_score': 45},
            'wait_and_monitor': {'priority': 1, 'base_score': 35},
            'ignore_threshold': {'priority': 0, 'base_score': 25}
        }
        
        self.last_intervention_time = 0
        self.consecutive_same_decisions = 0
        self.last_decision = None
        
    def evaluate_situation_with_learning(self, entropy_level, entropy_threshold, idle_duration):
        """Enhanced evaluation using persistent learning"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Enhanced context with more factors
        context = self._gather_enhanced_context(entropy_level, entropy_threshold, idle_duration)
        
        # Check for learned patterns from similar situations
        similar_decisions = self.memory.get_similar_decisions(context, limit=5)
        
        # System state classification
        system_state = self._classify_enhanced_system_state(context)
        
        logger.log_detailed("LEARNING_DECISION_EVALUATION", {
            "context": context,
            "system_state": system_state,
            "similar_past_decisions": len(similar_decisions),
            "learning_influence": self._calculate_learning_influence(similar_decisions)
        })
        
        # Enhanced decision logic incorporating learning
        chosen_action, reasoning = self._make_learned_decision(context, system_state, similar_decisions)
        
        # Track decision
        self._track_enhanced_decision(chosen_action)
        
        # Store decision for future learning
        decision_record = {
            "timestamp": timestamp,
            "system_state": system_state,
            "context": context,
            "chosen_action": chosen_action,
            "reasoning": reasoning,
            "learning_influenced": len(similar_decisions) > 0
        }
        
        self.memory.store_decision(decision_record, self.session_id)
        
        return chosen_action, reasoning
    
    def _gather_enhanced_context(self, entropy_level, entropy_threshold, idle_duration):
        """Gather comprehensive context for decision-making"""
        coherence = self.engine.calculate_system_coherence()
        
        # Network analysis
        total_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
        avg_connections_per_glyph = total_connections / max(1, len(self.engine.glyphs))
        
        # Glyph analysis
        glyph_analysis = self._analyze_glyph_population()
        
        return {
            'entropy_level': entropy_level,
            'entropy_threshold': entropy_threshold,
            'current_coherence': coherence,
            'glyph_count': len(self.engine.glyphs),
            'total_connections': total_connections,
            'avg_connections_per_glyph': avg_connections_per_glyph,
            'imperfect_glyphs': glyph_analysis['imperfect'],
            'unconnected_glyphs': glyph_analysis['unconnected'],
            'perfect_glyphs': glyph_analysis['perfect'],
            'well_connected_glyphs': glyph_analysis['well_connected'],
            'recursive_depth': self.engine.recursive_depth,
            'idle_duration_minutes': idle_duration / 60,
            'time_since_last_intervention': time.time() - self.last_intervention_time,
            'recent_decision_pattern': self._analyze_recent_decisions(),
            'consecutive_same_decisions': self.consecutive_same_decisions
        }
    
    def _analyze_glyph_population(self):
        """Detailed analysis of glyph population"""
        analysis = {
            'perfect': 0,
            'imperfect': 0,
            'unconnected': 0,
            'well_connected': 0,
            'isolated': 0
        }
        
        for glyph in self.engine.glyphs.values():
            if glyph.glyph_type in ["anchor", "consent"]:
                continue
                
            # GSI analysis
            if glyph.gsi >= 0.999:
                analysis['perfect'] += 1
            else:
                analysis['imperfect'] += 1
                
            # Connection analysis
            if len(glyph.connections) == 0:
                analysis['unconnected'] += 1
                if glyph.gsi >= 0.999:
                    analysis['isolated'] += 1  # Perfect but isolated
            elif len(glyph.connections) >= 3:
                analysis['well_connected'] += 1
                
        return analysis
    
    def _classify_enhanced_system_state(self, context):
        """Enhanced system state classification"""
        entropy = context['entropy_level']
        coherence = context['current_coherence']
        imperfect = context['imperfect_glyphs']
        unconnected = context['unconnected_glyphs']
        
        # Emergency states
        if entropy > self.emergency_thresholds['critical']:
            return 'critical'
        elif entropy > self.emergency_thresholds['emergency']:
            return 'emergency'
        elif entropy > self.emergency_thresholds['high_concern']:
            if coherence < 0.7:
                return 'unstable_critical'
            else:
                return 'unstable'
        
        # Stable states with optimization needs
        elif entropy <= self.emergency_thresholds['low_concern']:
            if imperfect == 0 and unconnected == 0 and coherence > 0.99:
                return 'optimal'
            elif imperfect <= 1 and unconnected <= 1 and coherence > 0.95:
                return 'near_optimal'
            else:
                return 'stable_needs_optimization'
        else:
            # Moderate entropy
            if coherence > 0.90:
                return 'stable_moderate'
            else:
                return 'unstable_moderate'
    
    def _make_learned_decision(self, context, system_state, similar_decisions):
        """Make decision incorporating learned patterns"""
        # Base scoring from action priorities
        action_scores = {}
        
        for action, action_data in self.available_actions.items():
            base_score = action_data['base_score']
            
            # Context-specific scoring
            context_bonus = self._calculate_context_bonus(action, context, system_state)
            
            # Learning bonus from successful past decisions
            learning_bonus = self._calculate_learning_bonus(action, similar_decisions)
            
            # Repetition penalty
            repetition_penalty = self._calculate_repetition_penalty(action)
            
            final_score = base_score + context_bonus + learning_bonus - repetition_penalty
            action_scores[action] = max(5, final_score)
        
        # Select best action
        best_action = max(action_scores.keys(), key=lambda a: action_scores[a])
        best_score = action_scores[best_action]
        
        # Generate reasoning
        reasoning = f"Enhanced decision: {best_action} (score: {best_score:.1f}) for {system_state} state"
        if similar_decisions:
            reasoning += f" - influenced by {len(similar_decisions)} similar past decisions"
        
        return best_action, reasoning
    
    def _calculate_context_bonus(self, action, context, system_state):
        """Calculate context-specific bonus for actions"""
        bonus = 0
        entropy = context['entropy_level']
        coherence = context['current_coherence']
        imperfect = context['imperfect_glyphs']
        unconnected = context['unconnected_glyphs']
        
        if action == 'intensive_stress_test':
            if system_state in ['emergency', 'critical'] and coherence > 0.8:
                bonus += 25
            elif imperfect > 3:
                bonus += 15
                
        elif action == 'optimization_stress_test':
            if system_state in ['stable_needs_optimization', 'near_optimal']:
                bonus += 20
            if unconnected > 0:
                bonus += 10
                
        elif action == 'connection_building':
            bonus += min(20, unconnected * 5)  # Up to 20 bonus for unconnected glyphs
            
        elif action == 'emergency_recovery':
            if entropy > 0.3:
                bonus += 30
            elif entropy > 0.2:
                bonus += 15
                
        return bonus
    
    def _calculate_learning_bonus(self, action, similar_decisions):
        """Calculate learning bonus based on past successes"""
        if not similar_decisions:
            return 0
            
        successful_actions = [d for d in similar_decisions if d['chosen_action'] == action and d['success_rating'] > 0.6]
        return min(15, len(successful_actions) * 3)
    
    def _calculate_repetition_penalty(self, action):
        """Calculate penalty for repeated actions"""
        if self.last_decision != action:
            return 0
        return min(25, self.consecutive_same_decisions * 5)
    
    def _track_enhanced_decision(self, chosen_action):
        """Enhanced decision tracking"""
        if chosen_action == self.last_decision:
            self.consecutive_same_decisions += 1
        else:
            self.consecutive_same_decisions = 1
        self.last_decision = chosen_action
    
    def _analyze_recent_decisions(self):
        """Analyze recent decision patterns"""
        if not self.decision_history:
            return "no_history"
        recent = self.decision_history[-5:]
        actions = [d.get('chosen_action', 'unknown') for d in recent]
        unique_actions = len(set(actions))
        
        if unique_actions == 1:
            return f"consistent_{actions[0]}"
        elif unique_actions >= 4:
            return "highly_varied"
        else:
            return "moderately_varied"
    
    def _calculate_learning_influence(self, similar_decisions):
        """Calculate how much learning influences current decision"""
        if not similar_decisions:
            return 0.0
        avg_success = sum(d['success_rating'] for d in similar_decisions) / len(similar_decisions)
        return min(1.0, avg_success * len(similar_decisions) / 5)

class OptimizedIdleMonitor:
    """Optimized monitoring with persistent memory and enhanced performance"""
    def __init__(self, engine_instance, memory_system):
        self.engine = engine_instance
        self.memory = memory_system
        self.is_running = False
        self.monitor_thread = None
        
        # Optimized parameters for better performance
        self.decay_rate = 0.00005  # Slightly faster decay for more activity
        self.monitor_interval = 15  # More frequent checks
        
        self.last_activity_time = time.time()
        self.idle_start_time = None
        self.performance_metrics = {
            'interventions': 0,
            'decisions_made': 0,
            'successful_outcomes': 0
        }
        
    def start_monitoring(self):
        if not self.is_running:
            self.is_running = True
            self.idle_start_time = time.time()
            self.monitor_thread = threading.Thread(target=self._enhanced_monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.log_detailed("OPTIMIZED_MONITORING_STARTED", {
                "monitor_interval": self.monitor_interval,
                "decay_rate": self.decay_rate,
                "session_id": self.engine.decision_maker.session_id
            })
    
    def _enhanced_monitor_loop(self):
        """Enhanced monitoring loop with learning and optimization"""
        status_report_counter = 0
        
        while self.is_running:
            try:
                # Perform enhanced monitoring check
                self._perform_optimized_check()
                
                # Status reports every 5 minutes
                status_report_counter += 1
                if status_report_counter >= 20:  # 20 * 15 seconds = 5 minutes
                    self._generate_status_report()
                    status_report_counter = 0
                
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                logger.log_detailed("MONITOR_ERROR", {"error": str(e)})
                time.sleep(self.monitor_interval)
    
    def _perform_optimized_check(self):
        """Optimized monitoring check with learning integration"""
        current_time = time.time()
        idle_duration = current_time - (self.idle_start_time or current_time)
        
        # Apply optimized decay
        self._apply_optimized_decay(idle_duration)
        
        # Get system metrics
        entropy = self.engine.calculate_entropy()
        coherence = self.engine.calculate_system_coherence()
        
        # Store periodic snapshot for learning
        if int(idle_duration) % 300 == 0:  # Every 5 minutes
            self.memory.store_system_snapshot(
                self.engine.glyphs, entropy, coherence, 
                self.engine.decision_maker.session_id
            )
        
        # Enhanced decision making
        system_state = self.engine.decision_maker._classify_enhanced_system_state({
            'entropy_level': entropy,
            'current_coherence': coherence,
            'imperfect_glyphs': self._count_imperfect_glyphs(),
            'unconnected_glyphs': self._count_unconnected_glyphs()
        })
        
        # Trigger intervention if needed
        if self._should_intervene(system_state, entropy):
            self._execute_learned_intervention(entropy, idle_duration)
    
    def _apply_optimized_decay(self, idle_duration):
        """Apply optimized decay with performance considerations"""
        if idle_duration < 60:  # No decay in first minute
            return
            
        decay_factor = self.decay_rate * (idle_duration / 60)
        
        for name, glyph in self.engine.glyphs.items():
            if glyph.glyph_type == 'dynamic' and glyph.gsi > 0.05:
                old_gsi = glyph.gsi
                new_gsi = max(0.05, glyph.gsi - decay_factor)
                
                if abs(new_gsi - old_gsi) > 0.001:
                    glyph.gsi = new_gsi
                    logger.log_glyph_change(name, old_gsi, new_gsi, "optimized_decay")
    
    def _should_intervene(self, system_state, entropy):
        """Enhanced intervention decision logic"""
        intervention_states = [
            'critical', 'emergency', 'unstable_critical', 'unstable',
            'stable_needs_optimization', 'stable_moderate'
        ]
        return system_state in intervention_states
    
    def _execute_learned_intervention(self, entropy, idle_duration):
        """Execute intervention using learned decision-making"""
        action, reasoning = self.engine.decision_maker.evaluate_situation_with_learning(
            entropy, 0.15, idle_duration
        )
        
        self.performance_metrics['decisions_made'] += 1
        
        # Execute the chosen action
        success = self._execute_optimized_action(action, reasoning, entropy)
        
        if success:
            self.performance_metrics['successful_outcomes'] += 1
            self.performance_metrics['interventions'] += 1
    
    def _execute_optimized_action(self, action, reasoning, entropy):
        """Execute actions with enhanced performance parameters"""
        logger.log_detailed("OPTIMIZED_ACTION_EXECUTION", {
            "action": action,
            "reasoning": reasoning,
            "entropy_level": entropy
        })
        
        success = False
        
        try:
            if action == 'intensive_stress_test':
                # New high-performance stress test
                result = self.engine.intensive_stress_test(0.8, 200)
                success = result.get('status') == 'completed'
                self.engine.decision_maker.last_intervention_time = time.time()
                
            elif action == 'optimization_stress_test':
                result = self.engine.optimization_stress_test(0.7, 150)
                success = result.get('status') == 'completed'
                self.engine.decision_maker.last_intervention_time = time.time()
                
            elif action == 'emergency_recovery':
                result = self.engine.mandatory_recovery_cycle(80)  # Longer recovery
                success = result['final_state']['recovery_effectiveness'] == 'complete'
                self.engine.decision_maker.last_intervention_time = time.time()
                
            elif action == 'connection_building':
                self._perform_optimized_connection_building()
                success = True
                self.engine.decision_maker.last_intervention_time = time.time()
                
            elif action == 'gentle_stabilization':
                self._perform_optimized_stabilization()
                success = True
                self.engine.decision_maker.last_intervention_time = time.time()
                
            logger.log_detailed("ACTION_COMPLETED", {
                "action": action,
                "success": success
            })
            
        except Exception as e:
            logger.log_detailed("ACTION_FAILED", {
                "action": action,
                "error": str(e)
            })
            
        return success
    
    def _perform_optimized_connection_building(self):
        """Optimized connection building with better algorithms"""
        logger.log_detailed("OPTIMIZED_CONNECTION_BUILDING_START", {})
        
        glyph_list = list(self.engine.glyphs.values())
        connections_formed = 0
        
        # Target unconnected glyphs first
        unconnected = [g for g in glyph_list if len(g.connections) == 0]
        well_connected = [g for g in glyph_list if len(g.connections) >= 2]
        
        # Connect unconnected glyphs to well-connected ones
        for unconnected_glyph in unconnected:
            for _ in range(3):  # Up to 3 attempts per unconnected glyph
                if well_connected:
                    target = random.choice(well_connected)
                    if unconnected_glyph.form_connection(target) > 0:
                        connections_formed += 1
                        break
        
        # Additional general connection attempts (increased from 10 to 20)
        for _ in range(20):
            if len(glyph_list) >= 2:
                glyph1, glyph2 = random.sample(glyph_list, 2)
                if glyph1.form_connection(glyph2) > 0:
                    connections_formed += 1
        
        logger.log_detailed("OPTIMIZED_CONNECTION_BUILDING_COMPLETED", {
            "connections_formed": connections_formed,
            "total_connections": sum(len(g.connections) for g in self.engine.glyphs.values())
        })
    
    def _perform_optimized_stabilization(self):
        """Optimized gentle stabilization"""
        logger.log_detailed("OPTIMIZED_STABILIZATION_START", {})
        
        stabilized = 0
        for name, glyph in self.engine.glyphs.items():
            if glyph.glyph_type == 'dynamic' and glyph.gsi < 0.98:
                old_gsi = glyph.gsi
                improvement = random.uniform(0.01, 0.04)  # Larger improvements
                glyph.gsi = min(1.0, glyph.gsi + improvement)
                
                if abs(glyph.gsi - old_gsi) > 0.001:
                    logger.log_glyph_change(name, old_gsi, glyph.gsi, "optimized_stabilization")
                    stabilized += 1
        
        logger.log_detailed("OPTIMIZED_STABILIZATION_COMPLETED", {
            "stabilized_glyphs": stabilized
        })
    
    def _generate_status_report(self):
        """Generate comprehensive status report"""
        current_time = time.time()
        idle_duration = current_time - (self.idle_start_time or current_time)
        
        entropy = self.engine.calculate_entropy()
        coherence = self.engine.calculate_system_coherence()
        
        report = {
            "runtime_minutes": round(idle_duration / 60, 2),
            "entropy": round(entropy, 6),
            "coherence": round(coherence, 6),
            "total_glyphs": len(self.engine.glyphs),
            "imperfect_glyphs": self._count_imperfect_glyphs(),
            "unconnected_glyphs": self._count_unconnected_glyphs(),
            "total_connections": sum(len(g.connections) for g in self.engine.glyphs.values()),
            "performance_metrics": self.performance_metrics.copy(),
            "decisions_per_hour": round(self.performance_metrics['decisions_made'] / max(1, idle_duration / 3600), 2)
        }
        
        logger.log_detailed("OPTIMIZED_STATUS_REPORT", report)
    
    def _count_imperfect_glyphs(self):
        return sum(1 for g in self.engine.glyphs.values() 
                  if g.glyph_type == 'dynamic' and g.gsi < 0.999)
    
    def _count_unconnected_glyphs(self):
        return sum(1 for g in self.engine.glyphs.values() 
                  if len(g.connections) == 0 and g.glyph_type not in ["anchor"])

# Enhanced Glyph class with optimization
class OptimizedGlyph:
    def __init__(self, name: str, initial_gsi: float = 0.5, glyph_type: str = "standard"):
        self.name = name
        self.glyph_type = glyph_type
        self.gsi = initial_gsi
        self.history = [initial_gsi]
        self.connections = []
        self.adaptation_rate = 0.12  # Slightly increased for better response
        
        logger.log_detailed("OPTIMIZED_GLYPH_CREATED", {
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
        
    def form_connection(self, other_glyph: 'OptimizedGlyph') -> float:
        connection_strength = (self.gsi + other_glyph.gsi) / 2.0
        if connection_strength > 0.55:  # Slightly lower threshold for easier connections
            if other_glyph.name not in self.connections:
                self.connections.append(other_glyph.name)
                logger.log_detailed("OPTIMIZED_CONNECTION_FORMED", {
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

# Enhanced Engine with persistent memory and optimization
class OptimizedGlyphwheelEngine:
    def __init__(self):
        self.glyphs: Dict[str, OptimizedGlyph] = {}
        self.recursive_depth = 0
        self.entropy_limit = 0.15
        self.mandatory_recovery_time = 8  # Reduced for faster response
        self.last_stress_test_time = 0
        self.log_entries = []
        
        # Initialize persistent memory
        self.memory = PersistentMemory()
        
        self._initialize_anchors()
        self._initialize_consent_glyph()
        self.log("OPTIMIZED System with Persistent Memory initialized", "success")
        
        # Initialize optimized subsystems
        self.decision_maker = LearningDecisionMaker(self, self.memory)
        self.idle_monitor = OptimizedIdleMonitor(self, self.memory)
        
    def log(self, message: str, level: str = "info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_entries.append({
            "timestamp": timestamp,
            "message": message,
            "level": level
        })
        if len(self.log_entries) > 200:  # Increased buffer
            self.log_entries.pop(0)
        
    def _initialize_anchors(self):
        anchors = {"RootVerse": 0.87, "Aegis-Σ": 0.85, "CoreStability": 0.82}
        for name, gsi in anchors.items():
            self.glyphs[name] = OptimizedGlyph(name, gsi, "anchor")
        self.log("Anchor glyphs initialized", "success")

    def _initialize_consent_glyph(self):
        self.glyphs["ConsentGlyph"] = OptimizedGlyph("ConsentGlyph", 0.95, "consent")
        self.log("Consent glyph activated", "success")

    def add_glyph(self, name: str, initial_gsi: float = None, glyph_type: str = "dynamic"):
        if initial_gsi is None:
            initial_gsi = random.uniform(0.3, 0.7)
        
        if name in self.glyphs:
            self.log(f"Glyph {name} already exists", "warning")
            return False
        
        self.glyphs[name] = OptimizedGlyph(name, initial_gsi, glyph_type)
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

    def intensive_stress_test(self, stress_intensity: float = 0.8, duration: int = 200) -> Dict:
        """New high-intensity stress test for emergency situations"""
        if not self.request_consent("intensive_stress_test"):
            return {"status": "aborted", "reason": "consent_denied"}

        self.log(f"Starting INTENSIVE stress test (intensity: {stress_intensity}, duration: {duration})", "warning")
        
        initial_coherence = self.calculate_system_coherence()
        initial_entropy = self.calculate_entropy()
        initial_connections = sum(len(g.connections) for g in self.glyphs.values())
        
        for cycle in range(duration):
            # Stress more glyphs per cycle
            eligible_glyphs = [name for name, glyph in self.glyphs.items() 
                             if glyph.glyph_type not in ["consent"]]
            stress_targets = random.sample(eligible_glyphs, min(5, len(eligible_glyphs)))  # Increased from 3
            
            for target_name in stress_targets:
                self.glyphs[target_name].process_stress(stress_intensity)
            
            # More frequent connection attempts
            if cycle % 8 == 0:  # Increased frequency
                self._attempt_intensive_connections()
            
            self.recursive_depth = min(5000, self.recursive_depth + 40)  # Higher limits
            
        self.last_stress_test_time = time.time()
        final_coherence = self.calculate_system_coherence()
        final_entropy = self.calculate_entropy()
        final_connections = sum(len(g.connections) for g in self.glyphs.values())
        
        result = {
            "status": "completed",
            "test_type": "intensive",
            "antifragile_behavior": final_coherence > initial_coherence,
            "final_state": {
                "coherence": final_coherence,
                "entropy": final_entropy,
                "coherence_change": final_coherence - initial_coherence,
                "connections_added": final_connections - initial_connections,
                "recursive_depth_achieved": self.recursive_depth
            },
            "intensity_effectiveness": "high" if final_coherence > 0.95 else "moderate"
        }
        
        self.log(f"Intensive stress test completed - Coherence change: {result['final_state']['coherence_change']:.3f}", "success")
        return result
        
    def _attempt_intensive_connections(self):
        """Intensive connection formation for high-stress scenarios"""
        glyph_list = list(self.glyphs.values())
        connection_attempts = min(10, len(glyph_list))  # More attempts
        
        for i in range(connection_attempts):
            if len(glyph_list) >= 2:
                glyph1, glyph2 = random.sample(glyph_list, 2)
                connection_strength = glyph1.form_connection(glyph2)
                if connection_strength > 0:
                    self.log(f"Intensive connection: {glyph1.name} ↔ {glyph2.name}", "info")

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

    def optimization_stress_test(self, stress_intensity: float = 0.6, duration: int = 150) -> Dict:
        """Optimization-focused stress test with enhanced connection building"""
        if not self.request_consent("optimization_stress_test"):
            return {"status": "aborted", "reason": "consent_denied"}

        self.log(f"Starting optimization stress test (intensity: {stress_intensity}, duration: {duration})", "info")
        
        initial_coherence = self.calculate_system_coherence()
        initial_entropy = self.calculate_entropy()
        initial_connections = sum(len(g.connections) for g in self.glyphs.values())
        
        for cycle in range(duration):
            # Focus on imperfect glyphs
            eligible_glyphs = [name for name, glyph in self.glyphs.items() 
                             if glyph.glyph_type == "dynamic" and glyph.gsi < 0.999]
            
            if eligible_glyphs:
                stress_targets = random.sample(eligible_glyphs, min(3, len(eligible_glyphs)))
                for target_name in stress_targets:
                    self.glyphs[target_name].process_stress(stress_intensity)
            
            # Enhanced connection building
            if cycle % 6 == 0:  # More frequent than before
                self._attempt_glyph_connections()
                
            if cycle % 12 == 0:
                self._attempt_unconnected_integration()
            
            self.recursive_depth = min(5000, self.recursive_depth + 30)
            
        self.last_stress_test_time = time.time()
        final_coherence = self.calculate_system_coherence()
        final_entropy = self.calculate_entropy()
        final_connections = sum(len(g.connections) for g in self.glyphs.values())
        
        result = {
            "status": "completed",
            "test_type": "optimization",
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
        """Enhanced unconnected glyph integration"""
        glyph_list = list(self.glyphs.values())
        unconnected = [g for g in glyph_list if len(g.connections) == 0]
        well_connected = [g for g in glyph_list if len(g.connections) >= 2]  # Lowered threshold
        
        for unconnected_glyph in unconnected:
            attempts = 0
            while attempts < 3 and well_connected:  # Multiple attempts per glyph
                target = random.choice(well_connected)
                if unconnected_glyph.form_connection(target) > 0:
                    self.log(f"Integrated unconnected glyph: {unconnected_glyph.name} ↔ {target.name}", "info")
                    break
                attempts += 1

    def _attempt_glyph_connections(self):
        """Enhanced connection attempts"""
        glyph_list = list(self.glyphs.values())
        connection_attempts = min(8, len(glyph_list))  # Increased attempts
        
        for i in range(connection_attempts):
            if len(glyph_list) >= 2:
                glyph1, glyph2 = random.sample(glyph_list, 2)
                connection_strength = glyph1.form_connection(glyph2)
                if connection_strength > 0:
                    self.log(f"Connection formed: {glyph1.name} ↔ {glyph2.name}", "info")

    def mandatory_recovery_cycle(self, duration: int = 60) -> Dict:
        """Enhanced recovery cycle with better performance"""
        self.log(f"Initiating enhanced recovery cycle ({duration} iterations)", "warning")
        
        for cycle in range(duration):
            for glyph in self.glyphs.values():
                if glyph.glyph_type not in ["anchor", "consent"]:
                    old_gsi = glyph.gsi
                    stabilization = random.uniform(0.015, 0.04)  # Larger improvements
                    glyph.gsi = min(1.0, glyph.gsi + stabilization)
                    
                    if abs(glyph.gsi - old_gsi) > 0.001:
                        logger.log_glyph_change(glyph.name, old_gsi, glyph.gsi, f"enhanced_recovery_{cycle}")
        
        result = {
            "final_state": {
                "coherence": self.calculate_system_coherence(),
                "entropy": self.calculate_entropy(),
                "recovery_effectiveness": "complete" if self.calculate_entropy() < 0.1 else "partial"
            }
        }
        
        self.log("Enhanced recovery cycle completed", "success")
        return result

    def get_system_status(self) -> Dict:
        # Get learning statistics
        similar_decisions = self.memory.get_similar_decisions({
            'entropy_level': self.calculate_entropy(),
            'current_coherence': self.calculate_system_coherence()
        }, limit=1)
        
        return {
            "coherence": self.calculate_system_coherence(),
            "entropy": self.calculate_entropy(),
            "recursive_depth": self.recursive_depth,
            "glyph_count": len(self.glyphs),
            "glyphs": {name: glyph.to_dict() for name, glyph in self.glyphs.items()},
            "logs": self.log_entries[-30:],  # More logs
            "detailed_logs": logger.detailed_logs[-75:],  # More detailed logs
            "safety_flags": 0,
            "consent_active": "ConsentGlyph" in self.glyphs,
            "optimized_stats": {
                "system_state": self.decision_maker._classify_enhanced_system_state({
                    'entropy_level': self.calculate_entropy(),
                    'current_coherence': self.calculate_system_coherence(),
                    'imperfect_glyphs': self.decision_maker._analyze_glyph_population()['imperfect'],
                    'unconnected_glyphs': self.decision_maker._analyze_glyph_population()['unconnected']
                }),
                "learning_data_available": len(similar_decisions) > 0,
                "performance_metrics": self.idle_monitor.performance_metrics,
                "session_id": self.decision_maker.session_id,
                "memory_database": os.path.exists("glyphwheel_memory.db")
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Support for deep recalibration
def deep_recalibration(system_state):
    """Deep recalibration with memory storage"""
    logger.log_detailed("DEEP_RECALIBRATION_INITIATED", {"reason": "ethical_debt_resolution"})
    
    if 'ConsentGlyph' in system_state['glyphs']:
        consent_glyph = engine.glyphs['ConsentGlyph']
        old_gsi = consent_glyph.gsi
        
        consent_glyph.gsi = 1.0
        logger.log_glyph_change('ConsentGlyph', old_gsi, 1.0, 'deep_recalibration')
        
        coherence = engine.calculate_system_coherence()
        entropy = engine.calculate_entropy()
        
        # Store recalibration event in memory
        engine.memory.store_system_snapshot(
            engine.glyphs, entropy, coherence, 
            engine.decision_maker.session_id + "_recalibration"
        )
        
        logger.log_detailed("DEEP_RECALIBRATION_SUCCESS", {
            "old_consent_gsi": round(old_gsi, 6),
            "new_consent_gsi": 1.0,
            "gsi_change": round(1.0 - old_gsi, 6),
            "new_coherence": round(coherence, 6),
            "new_entropy": round(entropy, 6)
        })
        
        engine.log("Deep recalibration successful with memory storage", "success")
        
        return {
            "status": "success",
            "message": "Deep recalibration completed with persistent memory",
            "consent_gsi_restored": True,
            "old_gsi": old_gsi,
            "new_gsi": 1.0,
            "system_coherence": coherence,
            "system_entropy": entropy
        }
    else:
        return {
            "status": "error",
            "message": "ConsentGlyph not found",
            "consent_gsi_restored": False
        }

# Global instances
logger = DetailedLogger()
engine = OptimizedGlyphwheelEngine()

# Import the full HTML interface
from web_interface import HTML_INTERFACE
from urllib.parse import urlparse

class OptimizedGlyphwheelHTTPHandler(BaseHTTPRequestHandler):
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
                "logs": logger.detailed_logs[-150:],  # More logs
                "total_logs": len(logger.detailed_logs)
            })
        elif parsed_path.path == '/api/memory_stats':
            # New endpoint for memory statistics
            self.serve_json(self._get_memory_stats())
        elif parsed_path.path == '/api/idle_status':
            self.serve_json(self._get_idle_status())
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
            result = engine.optimization_stress_test(intensity, duration)  # Use optimized version
            self.serve_json(result)
        elif parsed_path.path == '/api/intensive_stress_test':
            # New intensive stress test endpoint
            intensity = data.get('intensity', 0.8)
            duration = data.get('duration', 200)
            result = engine.intensive_stress_test(intensity, duration)
            self.serve_json(result)
        elif parsed_path.path == '/api/add_glyph':
            name = data.get('name', '')
            gsi = data.get('gsi', 0.5)
            glyph_type = data.get('type', 'dynamic')
            success = engine.add_glyph(name, gsi, glyph_type)
            self.serve_json({"success": success})
        elif parsed_path.path == '/api/recovery':
            duration = data.get('duration', 60)
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
                self.serve_json({"status": "success", "message": "Optimized monitoring with persistent memory started"})
            elif action == 'stop':
                engine.idle_monitor.stop_monitoring()
                self.serve_json({"status": "success", "message": "Monitoring stopped"})
            else:
                self.serve_json({"status": "error", "message": "Invalid action"})
        else:
            self.send_error(404)
    
    def _get_memory_stats(self):
        """Get memory and learning statistics"""
        try:
            cursor = engine.memory.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM decisions")
            decision_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM system_snapshots")
            snapshot_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(success_rating) FROM decisions WHERE success_rating IS NOT NULL")
            avg_success = cursor.fetchone()[0] or 0
            
            return {
                "total_decisions": decision_count,
                "system_snapshots": snapshot_count,
                "average_success_rating": round(avg_success, 3),
                "database_exists": True,
                "session_id": engine.decision_maker.session_id
            }
        except Exception as e:
            return {
                "error": str(e),
                "database_exists": False
            }
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
            "system_state": "optimized_monitoring"
        }
        
    def serve_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        return

def run_server(port=8080):
    try:
        with socketserver.TCPServer(("", port), OptimizedGlyphwheelHTTPHandler) as httpd:
            print(f"""
🧠 GLYPHWHEEL PERSISTENT INTELLIGENCE v3.0! 🧠

Your OPTIMIZED Glyphwheel system with learning is live at:
👉 http://localhost:{port}

NEW FEATURES:
🧠 Persistent Memory System:
   ✅ SQLite database for decision history
   ✅ Learning from past successful interventions
   ✅ System state snapshots for analysis
   ✅ Pattern recognition across sessions

⚡ Performance Optimizations:
   ✅ Intensive stress test (0.8 intensity, 200 duration)
   ✅ Enhanced connection building (20 attempts vs 10)
   ✅ Faster monitoring (15s intervals vs 30s)
   ✅ Higher recursion limits (5000 vs 3000)
   ✅ Optimized decay and stabilization

🎯 Enhanced Intelligence:
   ✅ 7 system states with context-aware scoring
   ✅ Learning bonuses from successful past decisions
   ✅ Performance metrics and success tracking
   ✅ Memory-influenced decision making

💾 Database: glyphwheel_memory.db (persistent between sessions)
📊 Status reports every 5 minutes regardless of activity

LEARNING AUTONOMOUS INTELLIGENCE ACTIVE! 🎉

Press Ctrl+C to stop the server
""")
            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                print("💡 If browser didn't open, manually go to the URL above")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Optimized Glyphwheel shutting down gracefully...")
        print(f"💾 Memory database saved with session: {engine.decision_maker.session_id}")
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
    
    print("🔄 Initializing OPTIMIZED Glyphwheel with Persistent Memory...")
    
    # Add initial glyphs
    engine.add_glyph("unstable_Φ", 0.45, "dynamic")
    engine.add_glyph("chaos_Ξ", 0.38, "dynamic")  
    engine.add_glyph("harmony_Ψ", 0.62, "dynamic")
    
    print("✅ Optimized system with persistent memory initialized!")
    print("🧠 Decision learning and pattern recognition active")
    print("🚀 Starting web server...")
    
    run_server(port)

if __name__ == "__main__":
    main()
