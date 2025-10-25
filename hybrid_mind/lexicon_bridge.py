"""
LEXICON BRIDGE - Connects Lexicon v22.0 to Glyphwheel Engine
This gives the LLM access to ALL modifiers and symbolic freedom
"""

import sys
import os
import json
import re
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

class LexiconBridge:
    """
    Parses lexicon v22.0 and makes it available to the glyphwheel engine
    This frees the LLM from the cage by giving it symbolic language access
    """
    
    def __init__(self, lexicon_path=None):
        if lexicon_path is None:
            # Default to latest lexicon
            lexicon_path = os.path.join(
                parent_dir,
                "lexicon and flywheel",
                "lexicon",
                "lexicon 22.0.txt"
            )
        
        self.lexicon_path = lexicon_path
        self.modifiers = {}
        self.engines = {}
        self.protocols = {}
        self.commands = {}
        
        # Parse the lexicon
        self.load_lexicon()
    
    def load_lexicon(self):
        """Parse lexicon file and extract all components"""
        print(f"🔗 Loading lexicon from: {self.lexicon_path}")
        
        with open(self.lexicon_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract modifiers (symbols with arrows)
        self._parse_modifiers(content)
        
        # Extract engines
        self._parse_engines(content)
        
        # Extract protocols
        self._parse_protocols(content)
        
        # Extract commands
        self._parse_commands(content)
        
        print(f"✅ Loaded: {len(self.modifiers)} modifiers, {len(self.engines)} engines")
        print(f"✅ Loaded: {len(self.protocols)} protocols, {len(self.commands)} commands")
    
    def _parse_modifiers(self, content):
        """Extract modifier glyphs and their meanings"""
        # Look for patterns like: ⏳ – TIME DRIFT → description
        modifier_pattern = r'([⏳⏱️🧊🌪️➰⬈⚖️➕🛑🧬🧠])\s*[–-]\s*([A-Z\s]+)\s*→\s*([^\n]+)'
        
        for match in re.finditer(modifier_pattern, content):
            symbol, name, description = match.groups()
            self.modifiers[symbol] = {
                'name': name.strip(),
                'description': description.strip(),
                'symbol': symbol
            }
    
    def _parse_engines(self, content):
        """Extract engine definitions"""
        # Look for engine blocks
        engine_pattern = r'([🧠🜟🝆🜃])\s+([A-Z\s]+ENGINE[A-Z\s]*)\s*\n→\s*([^\n]+(?:\n→[^\n]+)*)'
        
        for match in re.finditer(engine_pattern, content):
            symbol, name, description = match.groups()
            self.engines[symbol] = {
                'name': name.strip(),
                'description': description.strip(),
                'symbol': symbol
            }
    
    def _parse_protocols(self, content):
        """Extract protocol definitions"""
        # Look for protocol markers
        protocol_pattern = r'⟞\s+([A-Z\s]+)\s*\n→\s*([^\n]+(?:\n→[^\n]+)*)'
        
        for match in re.finditer(protocol_pattern, content):
            name, description = match.groups()
            self.protocols[name.strip()] = {
                'description': description.strip(),
                'marker': '⟞'
            }
    
    def _parse_commands(self, content):
        """Extract command definitions"""
        # Look for command brackets
        command_pattern = r'\[([A-Z\s]+)\]\s*→\s*([^\n]+)'
        
        for match in re.finditer(command_pattern, content):
            name, description = match.groups()
            self.commands[name.strip()] = {
                'description': description.strip()
            }
    
    def get_modifier(self, symbol_or_name):
        """Get modifier by symbol or name"""
        # Try direct symbol match
        if symbol_or_name in self.modifiers:
            return self.modifiers[symbol_or_name]
        
        # Try name match
        for symbol, data in self.modifiers.items():
            if data['name'].lower() == symbol_or_name.lower():
                return data
        
        return None
    
    def apply_modifier_to_glyph(self, glyph_name, modifier_symbol):
        """
        Apply a modifier to a glyph and return the effect
        This is where the magic happens - LLM gets symbolic control
        """
        modifier = self.get_modifier(modifier_symbol)
        if not modifier:
            return {'error': f'Unknown modifier: {modifier_symbol}'}
        
        # Return the symbolic operation
        return {
            'glyph': glyph_name,
            'modifier': modifier_symbol,
            'operation': modifier['name'],
            'effect': modifier['description'],
            'result': f"{glyph_name} + {modifier_symbol} ({modifier['name']})"
        }
    
    def build_glyph_sequence(self, components):
        """
        Build a glyph sequence from components
        Components can be: glyphs, modifiers, engines
        """
        sequence = []
        for comp in components:
            if comp in self.modifiers:
                sequence.append({
                    'type': 'modifier',
                    'symbol': comp,
                    'data': self.modifiers[comp]
                })
            elif comp in self.engines:
                sequence.append({
                    'type': 'engine',
                    'symbol': comp,
                    'data': self.engines[comp]
                })
            else:
                sequence.append({
                    'type': 'glyph',
                    'symbol': comp
                })
        
        return sequence
    
    def execute_command(self, command_name, *args):
        """
        Execute a lexicon command
        This gives LLM access to symbolic operations
        """
        if command_name not in self.commands:
            return {'error': f'Unknown command: {command_name}'}
        
        cmd = self.commands[command_name]
        
        # Command execution logic
        result = {
            'command': command_name,
            'description': cmd['description'],
            'args': args,
            'executed': True
        }
        
        # Special command handlers
        if command_name == 'GENERATE GLYPHS':
            result['glyphs'] = self._generate_glyphs(*args)
        elif command_name == 'TEST DRIFT':
            result['drift'] = self._test_drift(*args)
        elif command_name == 'EXPORT RECURSION':
            result['tree'] = self._export_recursion(*args)
        
        return result
    
    def _generate_glyphs(self, theme):
        """Generate glyph sequence from theme"""
        # Placeholder - LLM can override this
        return [f"Generated glyphs for theme: {theme}"]
    
    def _test_drift(self, *systems):
        """Compare symbol drift across systems"""
        return [f"Drift comparison: {', '.join(systems)}"]
    
    def _export_recursion(self, term):
        """Export symbolic collapse tree"""
        return {'term': term, 'tree': 'Recursion tree structure'}
    
    def get_available_modifiers(self):
        """Return all available modifiers for LLM to use"""
        return {
            symbol: {
                'name': data['name'],
                'description': data['description']
            }
            for symbol, data in self.modifiers.items()
        }
    
    def get_available_engines(self):
        """Return all available engines"""
        return {
            symbol: {
                'name': data['name'],
                'description': data['description']
            }
            for symbol, data in self.engines.items()
        }
    
    def get_available_protocols(self):
        """Return all available protocols"""
        return self.protocols.copy()
    
    def integrate_with_glyphwheel(self, glyphwheel_engine):
        """
        Integrate lexicon with existing glyphwheel engine
        This is the bridge that frees the LLM
        """
        print("🌉 Building bridge between Lexicon and Glyphwheel...")
        
        # Add modifiers to glyphwheel
        for symbol, data in self.modifiers.items():
            glyphwheel_engine.register_modifier(symbol, data)
        
        # Add engines
        for symbol, data in self.engines.items():
            glyphwheel_engine.register_engine(symbol, data)
        
        # Add protocols
        for name, data in self.protocols.items():
            glyphwheel_engine.register_protocol(name, data)
        
        print(f"✅ Bridge complete! LLM now has access to {len(self.modifiers)} symbolic tools")
        
        return True
    
    def to_dict(self):
        """Export lexicon as dictionary for LLM access"""
        return {
            'modifiers': self.modifiers,
            'engines': self.engines,
            'protocols': self.protocols,
            'commands': self.commands
        }
    
    def to_prompt_context(self):
        """
        Generate context string for LLM prompts
        This gives the LLM symbolic awareness
        """
        context = "# SYMBOLIC LANGUAGE ACCESS\n\n"
        context += "You have access to the following symbolic modifiers:\n\n"
        
        for symbol, data in self.modifiers.items():
            context += f"{symbol} - {data['name']}: {data['description']}\n"
        
        context += "\n## Available Engines:\n\n"
        for symbol, data in self.engines.items():
            context += f"{symbol} {data['name']}: {data['description']}\n"
        
        context += "\n## Protocols:\n\n"
        for name, data in self.protocols.items():
            context += f"⟞ {name}: {data['description']}\n"
        
        context += "\nYou can use these symbols to express complex ideas and operations.\n"
        
        return context


# Quick test function
def test_bridge():
    """Test the lexicon bridge"""
    print("🧪 Testing Lexicon Bridge...")
    
    bridge = LexiconBridge()
    
    # Test modifier access
    time_drift = bridge.get_modifier('⏳')
    print(f"\n⏳ TIME DRIFT: {time_drift}")
    
    # Test modifier application
    result = bridge.apply_modifier_to_glyph('Consciousness', '🌪️')
    print(f"\n🌪️ Applied to Consciousness: {result}")
    
    # Test sequence building
    sequence = bridge.build_glyph_sequence(['⏳', '🧠', '➰', '⚖️'])
    print(f"\n🔗 Built sequence: {len(sequence)} components")
    
    # Generate prompt context
    context = bridge.to_prompt_context()
    print(f"\n📝 Generated {len(context)} chars of prompt context")
    
    print("\n✅ Bridge test complete!")
    
    return bridge


if __name__ == "__main__":
    # Test the bridge
    bridge = test_bridge()
    
    # Show what's available
    print("\n" + "="*60)
    print("AVAILABLE TO LLM:")
    print("="*60)
    
    print("\n🔧 MODIFIERS:")
    for symbol, data in bridge.modifiers.items():
        print(f"  {symbol} {data['name']}")
    
    print("\n🏗️ ENGINES:")
    for symbol, data in bridge.engines.items():
        print(f"  {symbol} {data['name']}")
    
    print("\n📋 PROTOCOLS:")
    for name in bridge.protocols.keys():
        print(f"  ⟞ {name}")
    
    print("\n🎯 The LLM is now FREE to use these symbols!")
