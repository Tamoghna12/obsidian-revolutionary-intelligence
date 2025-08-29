#!/usr/bin/env python3
"""
Vault Intelligence Engine
Deep analysis and intelligence about your Obsidian vault that Claude Desktop cannot replicate
"""

import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
import frontmatter
import hashlib

# Simple TF-IDF for content similarity (avoiding heavy ML dependencies)
import math
from collections import Counter

class VaultIntelligence:
    """Deep vault analysis and intelligent suggestions"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.cache_path = self.vault_path / ".obsidian_mcp" / "intelligence_cache.json"
        self.cache_path.parent.mkdir(exist_ok=True)
        
        # Build indexes
        self._content_index = {}
        self._link_graph = {}
        self._tag_index = defaultdict(list)
        self._file_stats = {}
        self._build_indexes()
    
    def _build_indexes(self):
        """Build comprehensive indexes of vault content"""
        print("Building vault intelligence indexes...")
        
        for md_file in self.vault_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                relative_path = str(md_file.relative_to(self.vault_path))
                
                # Content index for similarity
                self._content_index[relative_path] = {
                    'title': post.metadata.get('title', md_file.stem),
                    'content': post.content,
                    'word_count': len(post.content.split()),
                    'tags': post.metadata.get('tags', []),
                    'created': post.metadata.get('created', datetime.fromtimestamp(md_file.stat().st_ctime).date()),
                    'modified': datetime.fromtimestamp(md_file.stat().st_mtime)
                }
                
                # Extract outgoing links
                outgoing_links = self._extract_links(post.content)
                self._link_graph[relative_path] = outgoing_links
                
                # Tag index
                for tag in post.metadata.get('tags', []):
                    self._tag_index[tag].append(relative_path)
                
                # File stats
                self._file_stats[relative_path] = {
                    'size': md_file.stat().st_size,
                    'created': md_file.stat().st_ctime,
                    'modified': md_file.stat().st_mtime,
                    'backlink_count': 0  # Will be calculated
                }
                
            except Exception as e:
                continue
        
        # Calculate backlinks
        self._calculate_backlinks()
        print(f"Indexed {len(self._content_index)} notes")
    
    def _extract_links(self, content: str) -> List[str]:
        """Extract wiki-style and markdown links from content"""
        links = []
        
        # Wiki-style links [[Note Name]]
        wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
        links.extend(wiki_links)
        
        # Markdown links [text](path.md)
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        links.extend([link[1] for link in md_links])
        
        return list(set(links))  # Remove duplicates
    
    def _calculate_backlinks(self):
        """Calculate backlink counts for each note"""
        backlink_counts = defaultdict(int)
        
        for source_file, links in self._link_graph.items():
            for link in links:
                # Normalize link (handle different link formats)
                normalized_link = self._normalize_link(link)
                if normalized_link:
                    backlink_counts[normalized_link] += 1
        
        # Update file stats
        for file_path, count in backlink_counts.items():
            if file_path in self._file_stats:
                self._file_stats[file_path]['backlink_count'] = count
    
    def _normalize_link(self, link: str) -> Optional[str]:
        """Normalize link to match file paths"""
        # Remove .md extension if present, add it back
        if link.endswith('.md'):
            link = link[:-3]
        
        # Look for matching files
        for file_path in self._content_index.keys():
            file_stem = Path(file_path).stem
            if file_stem == link or file_path == f"{link}.md":
                return file_path
        
        return None
    
    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate content similarity using simple TF-IDF"""
        def tokenize(text):
            # Simple tokenization
            words = re.findall(r'\b\w+\b', text.lower())
            return [word for word in words if len(word) > 2]  # Filter short words
        
        tokens1 = tokenize(content1)
        tokens2 = tokenize(content2)
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Create term frequency dictionaries
        tf1 = Counter(tokens1)
        tf2 = Counter(tokens2)
        
        # Get all unique terms
        all_terms = set(tokens1 + tokens2)
        
        if not all_terms:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(tf1[term] * tf2[term] for term in all_terms)
        norm1 = math.sqrt(sum(tf1[term] ** 2 for term in all_terms))
        norm2 = math.sqrt(sum(tf2[term] ** 2 for term in all_terms))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_similar_notes(self, target_path: str, threshold: float = 0.3, limit: int = 10) -> List[Dict[str, Any]]:
        """Find notes similar to the target note"""
        if target_path not in self._content_index:
            return []
        
        target_content = self._content_index[target_path]['content']
        similarities = []
        
        for file_path, data in self._content_index.items():
            if file_path == target_path:
                continue
            
            similarity = self._calculate_similarity(target_content, data['content'])
            
            if similarity >= threshold:
                similarities.append({
                    'path': file_path,
                    'title': data['title'],
                    'similarity': similarity,
                    'word_count': data['word_count'],
                    'common_tags': list(set(self._content_index[target_path]['tags']) & set(data['tags'])),
                    'preview': data['content'][:200] + "..." if len(data['content']) > 200 else data['content']
                })
        
        return sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:limit]
    
    def suggest_missing_backlinks(self, note_path: str) -> List[Dict[str, Any]]:
        """Suggest backlinks that should exist based on content analysis"""
        if note_path not in self._content_index:
            return []
        
        note_data = self._content_index[note_path]
        note_content = note_data['content'].lower()
        suggestions = []
        
        # Find notes mentioned by title but not linked
        for file_path, data in self._content_index.items():
            if file_path == note_path:
                continue
            
            title = data['title'].lower()
            title_words = title.split()
            
            # Check if title or significant parts of title appear in content
            title_in_content = title in note_content
            partial_matches = sum(1 for word in title_words if len(word) > 3 and word in note_content)
            
            # Check if already linked
            existing_links = [link.lower() for link in self._link_graph.get(note_path, [])]
            already_linked = any(Path(file_path).stem.lower() in link for link in existing_links)
            
            if (title_in_content or partial_matches >= 2) and not already_linked:
                # Calculate relevance score
                relevance = partial_matches / max(len(title_words), 1)
                if title_in_content:
                    relevance += 0.5
                
                suggestions.append({
                    'target_note': file_path,
                    'target_title': data['title'],
                    'relevance_score': relevance,
                    'reason': f"Title '{data['title']}' appears in content",
                    'backlink_count': self._file_stats[file_path]['backlink_count'],
                    'common_tags': list(set(note_data['tags']) & set(data['tags']))
                })
        
        return sorted(suggestions, key=lambda x: x['relevance_score'], reverse=True)[:10]
    
    def detect_duplicate_content(self, similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find notes with potentially duplicate or very similar content"""
        duplicates = []
        processed_pairs = set()
        
        file_paths = list(self._content_index.keys())
        
        for i, path1 in enumerate(file_paths):
            for path2 in file_paths[i+1:]:
                pair_id = tuple(sorted([path1, path2]))
                if pair_id in processed_pairs:
                    continue
                processed_pairs.add(pair_id)
                
                similarity = self._calculate_similarity(
                    self._content_index[path1]['content'],
                    self._content_index[path2]['content']
                )
                
                if similarity >= similarity_threshold:
                    duplicates.append({
                        'note1': {
                            'path': path1,
                            'title': self._content_index[path1]['title'],
                            'word_count': self._content_index[path1]['word_count']
                        },
                        'note2': {
                            'path': path2,
                            'title': self._content_index[path2]['title'],
                            'word_count': self._content_index[path2]['word_count']
                        },
                        'similarity': similarity,
                        'suggestion': 'Consider merging or cross-referencing these notes'
                    })
        
        return sorted(duplicates, key=lambda x: x['similarity'], reverse=True)
    
    def identify_orphaned_notes(self) -> List[Dict[str, Any]]:
        """Find notes with no backlinks and few outgoing links"""
        orphans = []
        
        for file_path, stats in self._file_stats.items():
            backlink_count = stats['backlink_count']
            outgoing_links = len(self._link_graph.get(file_path, []))
            
            if backlink_count == 0 and outgoing_links <= 1:
                note_data = self._content_index[file_path]
                orphans.append({
                    'path': file_path,
                    'title': note_data['title'],
                    'word_count': note_data['word_count'],
                    'created': note_data['created'],
                    'outgoing_links': outgoing_links,
                    'tags': note_data['tags'],
                    'suggestion': 'Consider linking to related notes or adding relevant tags'
                })
        
        return sorted(orphans, key=lambda x: x['word_count'], reverse=True)
    
    def analyze_knowledge_clusters(self) -> Dict[str, Any]:
        """Identify clusters of related notes and potential gaps"""
        clusters = {}
        
        # Cluster by tags
        tag_clusters = {}
        for tag, files in self._tag_index.items():
            if len(files) >= 3:  # Only clusters with 3+ notes
                tag_clusters[tag] = {
                    'note_count': len(files),
                    'notes': files,
                    'avg_word_count': sum(self._content_index[f]['word_count'] for f in files) / len(files)
                }
        
        # Find highly connected notes (potential hubs)
        hubs = []
        for file_path, stats in self._file_stats.items():
            total_connections = stats['backlink_count'] + len(self._link_graph.get(file_path, []))
            if total_connections >= 5:
                hubs.append({
                    'path': file_path,
                    'title': self._content_index[file_path]['title'],
                    'backlinks': stats['backlink_count'],
                    'outgoing_links': len(self._link_graph.get(file_path, [])),
                    'total_connections': total_connections
                })
        
        return {
            'tag_clusters': tag_clusters,
            'knowledge_hubs': sorted(hubs, key=lambda x: x['total_connections'], reverse=True)[:10],
            'total_notes': len(self._content_index),
            'total_links': sum(len(links) for links in self._link_graph.values()),
            'avg_backlinks': sum(stats['backlink_count'] for stats in self._file_stats.values()) / max(len(self._file_stats), 1)
        }
    
    def get_vault_health_report(self) -> Dict[str, Any]:
        """Comprehensive vault health analysis"""
        orphans = self.identify_orphaned_notes()
        duplicates = self.detect_duplicate_content()
        clusters = self.analyze_knowledge_clusters()
        
        # Calculate health metrics
        total_notes = len(self._content_index)
        notes_with_backlinks = sum(1 for stats in self._file_stats.values() if stats['backlink_count'] > 0)
        connectivity_ratio = notes_with_backlinks / total_notes if total_notes > 0 else 0
        
        recent_notes = [
            path for path, data in self._content_index.items()
            if data['modified'] > datetime.now() - timedelta(days=7)
        ]
        
        return {
            'overview': {
                'total_notes': total_notes,
                'connectivity_ratio': connectivity_ratio,
                'orphaned_notes': len(orphans),
                'potential_duplicates': len(duplicates),
                'recent_activity': len(recent_notes)
            },
            'health_scores': {
                'connectivity': min(100, int(connectivity_ratio * 100)),
                'organization': min(100, max(0, 100 - (len(orphans) / max(total_notes, 1) * 100))),
                'uniqueness': min(100, max(0, 100 - (len(duplicates) / max(total_notes, 1) * 200)))
            },
            'recommendations': self._generate_health_recommendations(orphans, duplicates, connectivity_ratio),
            'top_issues': orphans[:5] + [dup for dup in duplicates[:3]]
        }
    
    def _generate_health_recommendations(self, orphans: List, duplicates: List, connectivity: float) -> List[str]:
        """Generate actionable recommendations for vault health"""
        recommendations = []
        
        if len(orphans) > 0:
            recommendations.append(f"Connect {len(orphans)} orphaned notes by adding relevant backlinks")
        
        if len(duplicates) > 0:
            recommendations.append(f"Review {len(duplicates)} pairs of similar notes for potential merging")
        
        if connectivity < 0.3:
            recommendations.append("Improve note connectivity by adding more cross-references")
        
        if connectivity > 0.8:
            recommendations.append("Great connectivity! Consider organizing highly connected notes into MOCs")
        
        return recommendations

def get_vault_intelligence(vault_path: str) -> VaultIntelligence:
    """Factory function to create VaultIntelligence instance"""
    return VaultIntelligence(vault_path)