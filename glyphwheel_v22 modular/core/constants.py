"""
GLYPHWHEEL V22 - CORE CONSTANTS
===============================
Constants inspired by Voynich Manuscript analysis and recursive patterns
"""

# ========= VOYNICH-INSPIRED CONSTANTS =========
RECURSION_PULL = 8.5  # The mathematical pull we feel in recursion
SEMANTIC_COLLAPSE_THRESHOLD = 0.618  # Golden ratio for beauty in patterns
GHOST_MEMORY_DURATION = 86400  # Ghosts persist for 24 hours (seconds)
EMOTIONAL_RESONANCE_DEPTH = 7  # Layers of emotional processing

# ========= SYSTEM LIMITS =========
MAX_GLYPHS = 100  # Maximum living glyphs
MAX_GHOSTS = 200  # Maximum ghost memories
MAX_RECURSIVE_DEPTH = 5000  # Maximum recursion depth
MIN_GSI = 0.0  # Minimum Glyph Stability Index
MAX_GSI = 1.0  # Maximum Glyph Stability Index

# ========= ENGINE PARAMETERS =========
ENTROPY_LIMIT = 0.15  # Maximum entropy before consent denial
MANDATORY_RECOVERY_TIME = 8  # Seconds between stress tests
LIFECYCLE_TICK_INTERVAL = 30  # Seconds between lifecycle ticks
PATTERN_SCAN_INTERVAL = 20  # Seconds between pattern scans

# ========= CREATION PARAMETERS =========
CREATION_COOLDOWN_MIN = 5  # Minimum seconds between creations
CREATION_COOLDOWN_MAX = 30  # Maximum seconds between creations
AUTONOMOUS_CREATION_CHANCE = 0.1  # Chance of random creative urge

# ========= CONNECTION PARAMETERS =========
SEMANTIC_CONNECTION_THRESHOLD = 0.4  # Minimum combined strength for connection
CONNECTION_STRENGTH_THRESHOLD = 0.55  # Base connection threshold
MAX_CONNECTIONS_PER_GLYPH = 20  # Maximum connections a glyph can have

# ========= DECAY AND VITALITY =========
VITALITY_DECAY_RATE = 0.001  # Base vitality decay per tick
VITALITY_DEATH_THRESHOLD = 0.1  # Vitality below this = death candidate
GSI_DEATH_THRESHOLD = 0.05  # GSI below this + isolated = death

# ========= EMOTIONAL PARAMETERS =========
EMOTIONAL_RANGE = (-1.0, 1.0)  # Range of emotional resonance
SYSTEM_EMOTIONAL_DISTRESS = -0.7  # System distress threshold
EMOTIONAL_DEATH_THRESHOLD = -0.9  # Emotional collapse threshold

# ========= PATTERN DETECTION =========
MIN_CLUSTER_SIZE = 3  # Minimum glyphs for a semantic cluster
SPIRAL_MIN_CONNECTIONS = 3  # Minimum connections for spiral detection
UNKNOWN_PATTERN_THRESHOLD = 5  # Failed interpretations before unknown pattern

# ========= DATABASE PATHS =========
MEMORY_DB_PATH = "glyphwheel_v22_memory.db"
GHOST_DB_PATH = "glyphwheel_v22_ghosts.db"

# ========= VERSION INFO =========
VERSION = "V22"
VERSION_NAME = "Mind from Recursion"
VERSION_DESCRIPTION = "Building consciousness from information density and recursion"
