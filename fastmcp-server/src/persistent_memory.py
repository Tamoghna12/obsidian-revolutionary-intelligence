#!/usr/bin/env python3
"""
Persistent Memory System
Cross-session concept relationships and conversation memory that Claude Desktop cannot replicate
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
from dataclasses import dataclass

@dataclass
class ConceptRelationship:
    concept1: str
    concept2: str
    relationship_type: str
    strength: float
    context: str
    created_date: datetime
    last_accessed: datetime

@dataclass
class ConversationInsight:
    content: str
    concepts: List[str]
    insight_type: str
    importance_score: float
    created_date: datetime
    conversation_id: str

class PersistentMemory:
    """Cross-session persistent memory for concepts, relationships, and insights"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.db_path = self.vault_path / ".obsidian_mcp" / "memory.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS concepts (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    category TEXT,
                    importance_score REAL DEFAULT 1.0,
                    first_mentioned DATE,
                    last_accessed DATE,
                    access_count INTEGER DEFAULT 1
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS concept_relationships (
                    id INTEGER PRIMARY KEY,
                    concept1_id INTEGER,
                    concept2_id INTEGER,
                    relationship_type TEXT,
                    strength REAL,
                    context TEXT,
                    created_date DATE,
                    last_accessed DATE,
                    FOREIGN KEY (concept1_id) REFERENCES concepts (id),
                    FOREIGN KEY (concept2_id) REFERENCES concepts (id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_insights (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL,
                    concepts TEXT,  -- JSON array of concept names
                    insight_type TEXT,
                    importance_score REAL,
                    created_date DATE,
                    conversation_id TEXT,
                    source_context TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_sessions (
                    id INTEGER PRIMARY KEY,
                    session_id TEXT UNIQUE,
                    start_time DATE,
                    end_time DATE,
                    topics_discussed TEXT,  -- JSON array
                    insights_count INTEGER DEFAULT 0,
                    relationships_formed INTEGER DEFAULT 0
                )
            """)
    
    def extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text using simple heuristics"""
        # This is a basic implementation - could be enhanced with NLP
        text_lower = text.lower()
        
        # Common research/academic concept patterns
        concept_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Proper nouns (Neural Networks)
            r'\b\w+(?:[-_]\w+)+\b',          # Hyphenated terms (machine-learning)
            r'\b[A-Z]{2,}\b',                # Acronyms (AI, ML, NLP)
        ]
        
        concepts = []
        for pattern in concept_patterns:
            matches = re.findall(pattern, text)
            concepts.extend([match.strip() for match in matches])
        
        # Add some domain-specific keywords
        domain_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural networks', 'transformer', 'attention mechanism',
            'quantum computing', 'blockchain', 'cryptography',
            'bioinformatics', 'crispr', 'gene therapy',
            'climate change', 'renewable energy', 'sustainability'
        ]
        
        for keyword in domain_keywords:
            if keyword in text_lower:
                concepts.append(keyword.title())
        
        return list(set(concepts))  # Remove duplicates
    
    def store_concept(self, name: str, description: str = "", category: str = "") -> int:
        """Store or update a concept in persistent memory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if concept exists
            cursor.execute("SELECT id, access_count FROM concepts WHERE name = ?", (name,))
            result = cursor.fetchone()
            
            if result:
                # Update existing concept
                concept_id, access_count = result
                cursor.execute("""
                    UPDATE concepts 
                    SET last_accessed = ?, access_count = ?, description = COALESCE(?, description)
                    WHERE id = ?
                """, (datetime.now(), access_count + 1, description, concept_id))
                return concept_id
            else:
                # Insert new concept
                cursor.execute("""
                    INSERT INTO concepts (name, description, category, first_mentioned, last_accessed)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, description, category, datetime.now(), datetime.now()))
                return cursor.lastrowid
    
    def store_relationship(self, concept1: str, concept2: str, relationship_type: str, 
                          strength: float, context: str) -> bool:
        """Store relationship between concepts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get or create concept IDs
                id1 = self.store_concept(concept1)
                id2 = self.store_concept(concept2)
                
                if id1 == id2:  # Don't relate concept to itself
                    return False
                
                # Check if relationship already exists
                cursor.execute("""
                    SELECT id, strength FROM concept_relationships 
                    WHERE (concept1_id = ? AND concept2_id = ?) 
                       OR (concept1_id = ? AND concept2_id = ?)
                """, (id1, id2, id2, id1))
                
                result = cursor.fetchone()
                
                if result:
                    # Update existing relationship
                    rel_id, old_strength = result
                    new_strength = min(1.0, (old_strength + strength) / 2)  # Average and cap at 1.0
                    cursor.execute("""
                        UPDATE concept_relationships 
                        SET strength = ?, context = ?, last_accessed = ?
                        WHERE id = ?
                    """, (new_strength, context, datetime.now(), rel_id))
                else:
                    # Insert new relationship
                    cursor.execute("""
                        INSERT INTO concept_relationships 
                        (concept1_id, concept2_id, relationship_type, strength, context, created_date, last_accessed)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (id1, id2, relationship_type, strength, context, datetime.now(), datetime.now()))
                
                return True
                
        except Exception as e:
            print(f"Error storing relationship: {e}")
            return False
    
    def store_conversation_insight(self, content: str, insight_type: str = "general", 
                                 importance_score: float = 0.5, conversation_id: str = None) -> bool:
        """Store insights from conversations"""
        try:
            if conversation_id is None:
                conversation_id = hashlib.md5(f"{datetime.now().isoformat()}{content[:100]}".encode()).hexdigest()[:12]
            
            concepts = self.extract_concepts(content)
            
            # Store each concept
            for concept in concepts:
                self.store_concept(concept)
            
            # Store relationships between concepts mentioned together
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    self.store_relationship(
                        concept1, concept2, "co-mentioned", 
                        0.3, f"Discussed together in conversation {conversation_id}"
                    )
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversation_insights 
                    (content, concepts, insight_type, importance_score, created_date, conversation_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (content, json.dumps(concepts), insight_type, importance_score, 
                     datetime.now(), conversation_id))
            
            return True
            
        except Exception as e:
            print(f"Error storing conversation insight: {e}")
            return False
    
    def recall_concept_history(self, concept_name: str, days_back: int = 30) -> Dict[str, Any]:
        """Retrieve all information about a concept"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get concept info
            cursor.execute("""
                SELECT * FROM concepts WHERE name LIKE ?
            """, (f"%{concept_name}%",))
            concept_info = cursor.fetchone()
            
            if not concept_info:
                return {"error": f"No information found for concept: {concept_name}"}
            
            concept_id = concept_info[0]
            
            # Get relationships
            cursor.execute("""
                SELECT c1.name, c2.name, cr.relationship_type, cr.strength, cr.context, cr.created_date
                FROM concept_relationships cr
                JOIN concepts c1 ON cr.concept1_id = c1.id
                JOIN concepts c2 ON cr.concept2_id = c2.id
                WHERE cr.concept1_id = ? OR cr.concept2_id = ?
                ORDER BY cr.strength DESC, cr.created_date DESC
            """, (concept_id, concept_id))
            relationships = cursor.fetchall()
            
            # Get conversation insights
            cutoff_date = datetime.now() - timedelta(days=days_back)
            cursor.execute("""
                SELECT content, insight_type, importance_score, created_date, conversation_id
                FROM conversation_insights
                WHERE concepts LIKE ? AND created_date >= ?
                ORDER BY importance_score DESC, created_date DESC
            """, (f'%{concept_name}%', cutoff_date))
            insights = cursor.fetchall()
            
            return {
                "concept": {
                    "name": concept_info[1],
                    "description": concept_info[2],
                    "category": concept_info[3],
                    "importance_score": concept_info[4],
                    "first_mentioned": concept_info[5],
                    "last_accessed": concept_info[6],
                    "access_count": concept_info[7]
                },
                "relationships": [
                    {
                        "concepts": [rel[0], rel[1]],
                        "type": rel[2],
                        "strength": rel[3],
                        "context": rel[4],
                        "created": rel[5]
                    } for rel in relationships
                ],
                "recent_insights": [
                    {
                        "content": insight[0],
                        "type": insight[1],
                        "importance": insight[2],
                        "date": insight[3],
                        "conversation_id": insight[4]
                    } for insight in insights
                ]
            }
    
    def suggest_forgotten_connections(self, current_concepts: List[str]) -> List[Dict[str, Any]]:
        """Find related concepts from memory that might be relevant"""
        suggestions = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for concept in current_concepts:
                # Find concepts with strong relationships
                cursor.execute("""
                    SELECT c2.name, cr.relationship_type, cr.strength, cr.context
                    FROM concept_relationships cr
                    JOIN concepts c1 ON cr.concept1_id = c1.id
                    JOIN concepts c2 ON cr.concept2_id = c2.id
                    WHERE c1.name LIKE ? AND cr.strength > 0.5
                    ORDER BY cr.strength DESC
                    LIMIT 5
                """, (f"%{concept}%",))
                
                related = cursor.fetchall()
                
                for rel in related:
                    if rel[0].lower() not in [c.lower() for c in current_concepts]:
                        suggestions.append({
                            "forgotten_concept": rel[0],
                            "relationship_to": concept,
                            "relationship_type": rel[1],
                            "strength": rel[2],
                            "context": rel[3]
                        })
        
        return sorted(suggestions, key=lambda x: x["strength"], reverse=True)[:10]
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of stored knowledge"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Count concepts
            cursor.execute("SELECT COUNT(*) FROM concepts")
            concept_count = cursor.fetchone()[0]
            
            # Count relationships
            cursor.execute("SELECT COUNT(*) FROM concept_relationships")
            relationship_count = cursor.fetchone()[0]
            
            # Count insights
            cursor.execute("SELECT COUNT(*) FROM conversation_insights")
            insight_count = cursor.fetchone()[0]
            
            # Get top concepts by importance/access
            cursor.execute("""
                SELECT name, importance_score, access_count 
                FROM concepts 
                ORDER BY importance_score * access_count DESC 
                LIMIT 10
            """)
            top_concepts = cursor.fetchall()
            
            return {
                "total_concepts": concept_count,
                "total_relationships": relationship_count,
                "total_insights": insight_count,
                "top_concepts": [
                    {"name": c[0], "importance": c[1], "access_count": c[2]} 
                    for c in top_concepts
                ]
            }

def get_persistent_memory(vault_path: str) -> PersistentMemory:
    """Factory function to create PersistentMemory instance"""
    return PersistentMemory(vault_path)