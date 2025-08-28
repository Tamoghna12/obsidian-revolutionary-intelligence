#!/usr/bin/env python3
"""
Proactive Knowledge Assistant
AI assistant that proactively surfaces insights and suggests knowledge improvements
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import re

class ProactiveAssistant:
    """Proactive knowledge assistant that surfaces forgotten insights and suggests improvements"""
    
    def __init__(self, vault_path: str, memory_system=None, vault_intelligence=None):
        self.vault_path = Path(vault_path)
        self.memory = memory_system
        self.vault_intel = vault_intelligence
        self.insights_history = []
        self.user_patterns = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Load user behavior patterns from history"""
        patterns_file = self.vault_path / ".obsidian_mcp" / "user_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    self.user_patterns = json.load(f)
            except Exception:
                self.user_patterns = {}
        else:
            self.user_patterns = {
                'research_areas': [],
                'active_projects': [],
                'note_creation_patterns': {},
                'favorite_tags': [],
                'work_schedule': {},
                'knowledge_gaps': []
            }
    
    def _save_patterns(self):
        """Save user behavior patterns"""
        patterns_file = self.vault_path / ".obsidian_mcp" / "user_patterns.json"
        patterns_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(patterns_file, 'w') as f:
                json.dump(self.user_patterns, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def analyze_current_context(self, current_note_content: str = "", recent_activity: List[str] = None) -> Dict[str, Any]:
        """Analyze current context to provide proactive suggestions"""
        context = {
            'extracted_concepts': [],
            'identified_projects': [],
            'detected_research_areas': [],
            'work_patterns': {},
            'suggested_actions': []
        }
        
        if current_note_content:
            # Extract concepts from current work
            context['extracted_concepts'] = self._extract_concepts(current_note_content)
            
            # Identify potential projects
            context['identified_projects'] = self._identify_projects(current_note_content)
            
            # Detect research areas
            context['detected_research_areas'] = self._detect_research_areas(current_note_content)
        
        if recent_activity:
            context['work_patterns'] = self._analyze_work_patterns(recent_activity)
        
        return context
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        if self.memory:
            return self.memory.extract_concepts(text)
        
        # Simple fallback extraction
        concepts = []
        
        # Technical terms (capitalized words, acronyms)
        technical_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        concepts.extend(technical_terms)
        
        # Acronyms
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        concepts.extend(acronyms)
        
        return list(set(concepts))
    
    def _identify_projects(self, text: str) -> List[str]:
        """Identify potential project references"""
        project_indicators = [
            'project', 'research', 'study', 'investigation', 'experiment',
            'analysis', 'development', 'implementation', 'thesis', 'paper'
        ]
        
        projects = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in project_indicators):
                # Extract potential project name
                if ':' in line:
                    project_name = line.split(':')[0].strip('# -')
                    if len(project_name) < 50:  # Reasonable project name length
                        projects.append(project_name)
        
        return projects[:5]  # Limit to 5 projects
    
    def _detect_research_areas(self, text: str) -> List[str]:
        """Detect research areas from text"""
        research_keywords = {
            'machine_learning': ['machine learning', 'ml', 'neural network', 'deep learning', 'ai', 'artificial intelligence'],
            'biology': ['biology', 'genetics', 'dna', 'rna', 'protein', 'cell', 'organism'],
            'physics': ['physics', 'quantum', 'relativity', 'particle', 'energy', 'matter'],
            'computer_science': ['algorithm', 'data structure', 'programming', 'software', 'computation'],
            'mathematics': ['mathematics', 'calculus', 'algebra', 'statistics', 'probability', 'theorem'],
            'chemistry': ['chemistry', 'molecule', 'reaction', 'compound', 'element', 'bond'],
            'neuroscience': ['neuroscience', 'brain', 'neuron', 'cognition', 'consciousness'],
            'psychology': ['psychology', 'behavior', 'cognitive', 'mental', 'emotion', 'learning']
        }
        
        detected_areas = []
        text_lower = text.lower()
        
        for area, keywords in research_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_areas.append(area.replace('_', ' ').title())
        
        return detected_areas
    
    def _analyze_work_patterns(self, recent_activity: List[str]) -> Dict[str, Any]:
        """Analyze work patterns from recent activity"""
        patterns = {
            'most_active_times': [],
            'preferred_note_types': [],
            'research_focus_shift': [],
            'productivity_indicators': {}
        }
        
        # This would analyze timestamps, note types, etc.
        # Simplified for now
        patterns['activity_level'] = len(recent_activity)
        patterns['recent_focus'] = recent_activity[:3] if recent_activity else []
        
        return patterns
    
    def surface_forgotten_insights(self, current_concepts: List[str] = None) -> List[Dict[str, Any]]:
        """Surface relevant insights from the past that might be forgotten"""
        insights = []
        
        if not current_concepts and self.memory:
            # Get concepts from recent activity
            current_concepts = []
        
        if self.memory and current_concepts:
            # Get forgotten connections from memory
            forgotten = self.memory.suggest_forgotten_connections(current_concepts)
            
            for item in forgotten:
                insights.append({
                    'type': 'forgotten_connection',
                    'insight': f"You previously connected '{item['forgotten_concept']}' to '{item['relationship_to']}' - this might be relevant to your current work",
                    'relevance_score': item['strength'],
                    'context': item['context'],
                    'action': f"Consider reviewing notes about '{item['forgotten_concept']}'"
                })
        
        if self.vault_intel:
            # Surface similar notes from vault intelligence
            # This would require current note context
            pass
        
        # Add pattern-based insights
        if self.user_patterns.get('research_areas'):
            for area in self.user_patterns['research_areas']:
                if current_concepts and any(area.lower() in concept.lower() for concept in current_concepts):
                    insights.append({
                        'type': 'research_area_connection',
                        'insight': f"This connects to your ongoing research in {area}",
                        'relevance_score': 0.7,
                        'action': f"Consider updating your {area} knowledge map"
                    })
        
        return sorted(insights, key=lambda x: x['relevance_score'], reverse=True)[:10]
    
    def identify_knowledge_gaps(self, research_area: str = None) -> List[Dict[str, Any]]:
        """Identify gaps in knowledge based on patterns and references"""
        gaps = []
        
        if self.memory:
            # Find concepts that are mentioned but not deeply explored
            memory_summary = self.memory.get_knowledge_summary()
            top_concepts = memory_summary.get('top_concepts', [])
            
            for concept_data in top_concepts:
                concept_name = concept_data['name']
                access_count = concept_data['access_count']
                
                # If concept is mentioned often but not deeply explored
                if access_count > 5:
                    concept_history = self.memory.recall_concept_history(concept_name, days_back=90)
                    insight_count = len(concept_history.get('recent_insights', []))
                    
                    if insight_count < 3:  # Few insights despite high mentions
                        gaps.append({
                            'concept': concept_name,
                            'gap_type': 'shallow_exploration',
                            'description': f"'{concept_name}' is frequently mentioned but rarely explored in depth",
                            'suggestion': f"Consider creating a dedicated deep-dive note on {concept_name}",
                            'priority': 'high' if access_count > 10 else 'medium'
                        })
        
        if self.vault_intel:
            # Find orphaned notes that might indicate gaps
            orphans = self.vault_intel.identify_orphaned_notes()
            
            for orphan in orphans[:5]:  # Top 5 orphans
                gaps.append({
                    'concept': orphan['title'],
                    'gap_type': 'disconnected_knowledge',
                    'description': f"Note '{orphan['title']}' exists but isn't connected to your knowledge network",
                    'suggestion': f"Review and connect '{orphan['title']}' to related notes",
                    'priority': 'medium'
                })
        
        return gaps[:10]
    
    def suggest_review_schedule(self) -> List[Dict[str, Any]]:
        """Suggest notes to review based on importance and time since last access"""
        suggestions = []
        
        if self.memory:
            memory_summary = self.memory.get_knowledge_summary()
            top_concepts = memory_summary.get('top_concepts', [])
            
            for concept_data in top_concepts[:10]:
                concept_name = concept_data['name']
                history = self.memory.recall_concept_history(concept_name, days_back=30)
                
                if history.get('concept'):
                    last_accessed = history['concept'].get('last_accessed')
                    importance = history['concept'].get('importance_score', 0)
                    
                    # Simple scoring: important concepts not accessed recently
                    if importance > 0.5:
                        suggestions.append({
                            'concept': concept_name,
                            'importance': importance,
                            'last_accessed': last_accessed,
                            'suggestion': f"Review notes about '{concept_name}' - it's important but hasn't been accessed recently",
                            'review_priority': importance * 0.7 + 0.3  # Boost for importance
                        })
        
        return sorted(suggestions, key=lambda x: x['review_priority'], reverse=True)[:8]
    
    def detect_research_momentum_shifts(self) -> List[Dict[str, Any]]:
        """Detect shifts in research focus and suggest actions"""
        shifts = []
        
        if not self.memory:
            return shifts
        
        # Get recent vs older insights to detect shifts
        recent_insights = []  # Would get from memory system
        older_insights = []   # Would get from memory system
        
        # This would compare concept frequencies over different time periods
        # Simplified for now
        
        shifts.append({
            'shift_type': 'emerging_interest',
            'description': 'New concepts appearing frequently in recent notes',
            'suggestion': 'Consider formalizing this new research direction',
            'confidence': 0.6
        })
        
        return shifts
    
    def generate_proactive_suggestions(self, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate comprehensive proactive suggestions"""
        suggestions = []
        
        # Forgotten insights
        forgotten = self.surface_forgotten_insights(
            context.get('extracted_concepts', []) if context else None
        )
        suggestions.extend(forgotten)
        
        # Knowledge gaps
        gaps = self.identify_knowledge_gaps()
        suggestions.extend([{
            'type': 'knowledge_gap',
            'insight': gap['description'],
            'relevance_score': 0.6 if gap['priority'] == 'high' else 0.4,
            'action': gap['suggestion']
        } for gap in gaps])
        
        # Review suggestions
        review_items = self.suggest_review_schedule()
        suggestions.extend([{
            'type': 'review_suggestion',
            'insight': item['suggestion'],
            'relevance_score': item['review_priority'],
            'action': f"Review notes about {item['concept']}"
        } for item in review_items])
        
        # Limit and sort by relevance
        return sorted(suggestions, key=lambda x: x['relevance_score'], reverse=True)[:15]
    
    def update_user_patterns(self, activity_data: Dict[str, Any]):
        """Update user patterns based on new activity"""
        if 'research_areas' in activity_data:
            for area in activity_data['research_areas']:
                if area not in self.user_patterns['research_areas']:
                    self.user_patterns['research_areas'].append(area)
        
        if 'concepts' in activity_data:
            # Track concept usage patterns
            pass
        
        self._save_patterns()

def get_proactive_assistant(vault_path: str, memory_system=None, vault_intelligence=None) -> ProactiveAssistant:
    """Factory function to create ProactiveAssistant instance"""
    return ProactiveAssistant(vault_path, memory_system, vault_intelligence)