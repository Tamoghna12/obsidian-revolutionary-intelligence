"""
Obsidian Revolutionary Intelligence MCP Server - Core Components

This package contains all the core components for the hybrid AI knowledge system:
- Hybrid Architecture: One-click conveniences + unique intelligence
- AI Research System: Autonomous research and knowledge graph
- Content Creation: Research-to-content pipeline
- Productivity: Enhanced templates and workflow automation
"""

__version__ = "1.1.0"
__author__ = "Obsidian Revolutionary Intelligence Team"
__description__ = "Hybrid AI Knowledge System for Claude Desktop"

# Core component exports
from .quick_actions import get_quick_actions
from .persistent_memory import get_persistent_memory
from .vault_intelligence import get_vault_intelligence
from .proactive_assistant import get_proactive_assistant
from .revolutionary_intelligence import get_revolutionary_intelligence
from .content_creation_engine import get_content_creation_engine
from .enhanced_templates import TemplateManager, ProductivityFeatures
from .knowledge_organizer import get_productivity_system
from .productivity_enhancer import get_productivity_enhancer

__all__ = [
    'get_quick_actions',
    'get_persistent_memory', 
    'get_vault_intelligence',
    'get_proactive_assistant',
    'get_revolutionary_intelligence',
    'get_content_creation_engine',
    'TemplateManager',
    'ProductivityFeatures',
    'get_productivity_system',
    'get_productivity_enhancer'
]