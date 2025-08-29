#!/usr/bin/env python3
"""
Quick Actions Engine
One-click convenience tools that eliminate the need for long prompts
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import glob
import frontmatter

# Optional dependencies
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class QuickActions:
    """One-click convenience actions for common tasks"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.recent_papers_cache = {}
        
    def get_recent_notes(self, days: int = 7) -> List[Dict]:
        """Get notes created/modified in the last N days"""
        recent_notes = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.stat().st_mtime > cutoff_date.timestamp():
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        recent_notes.append({
                            'path': str(md_file.relative_to(self.vault_path)),
                            'title': post.metadata.get('title', md_file.stem),
                            'content': post.content[:200] + "..." if len(post.content) > 200 else post.content,
                            'tags': post.metadata.get('tags', []),
                            'modified': datetime.fromtimestamp(md_file.stat().st_mtime).strftime('%Y-%m-%d')
                        })
                except Exception:
                    continue
        
        return sorted(recent_notes, key=lambda x: x['modified'], reverse=True)[:10]
    
    def extract_research_areas(self) -> List[str]:
        """Extract main research areas from vault tags and content"""
        tag_counts = {}
        
        for md_file in self.vault_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    tags = post.metadata.get('tags', [])
                    for tag in tags:
                        if isinstance(tag, str):
                            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except Exception:
                continue
        
        # Return top research areas
        return sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def generate_research_summary_prompt(self) -> str:
        """Generate a targeted prompt for research summary"""
        research_areas = self.extract_research_areas()
        recent_notes = self.get_recent_notes(7)
        
        areas_text = ", ".join([area[0] for area in research_areas[:3]])
        recent_topics = [note['title'] for note in recent_notes[:5]]
        
        prompt = f"""
Based on my research focus areas ({areas_text}) and recent notes about {', '.join(recent_topics[:3])}, 
please search for and summarize the most relevant recent papers from arXiv, bioRxiv, and other academic sources.

Focus on:
1. Papers published in the last 2 weeks
2. Breakthrough findings in {areas_text}
3. Papers that connect to my recent work on {recent_topics[0] if recent_topics else 'current research'}

Format as a structured summary with key insights, methodology highlights, and relevance to my work.
        """
        
        return prompt.strip()
    
    def generate_blog_conversion_prompt(self, note_path: str) -> str:
        """Generate prompt to convert a specific note to blog post"""
        try:
            full_path = self.vault_path / note_path
            if not full_path.exists():
                return f"Note not found: {note_path}"
                
            with open(full_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
            content_preview = post.content[:500] + "..." if len(post.content) > 500 else post.content
            tags = post.metadata.get('tags', [])
            
            title = post.metadata.get('title', full_path.stem)
            prompt = f"""
Convert this research note into an engaging blog post:

Title: {title}
Tags: {', '.join(tags)}
Research Areas: {', '.join([area[0] for area in self.extract_research_areas()[:2]])}

Original Note Content:
{content_preview}

Please:
1. Create an engaging title and introduction
2. Restructure content for general audience
3. Add relevant examples and analogies
4. Include a compelling conclusion
5. Suggest 2-3 related topics for follow-up posts
6. Format in markdown with proper headings

Target audience: Technically interested but not necessarily expert readers.
            """
            
            return prompt.strip()
            
        except Exception as e:
            return f"Error reading note {note_path}: {str(e)}"
    
    def generate_weekly_digest_prompt(self) -> str:
        """Generate prompt for weekly research digest"""
        recent_notes = self.get_recent_notes(7)
        research_areas = self.extract_research_areas()
        
        if not recent_notes:
            return "No recent notes found for weekly digest."
            
        notes_summary = []
        for note in recent_notes:
            notes_summary.append(f"- {note['title']}: {note['content'][:100]}...")
            
        prompt = f"""
Create a weekly research digest based on my recent work and interests:

My Research Areas: {', '.join([area[0] for area in research_areas[:3]])}

This Week's Notes:
{chr(10).join(notes_summary)}

Please:
1. Search for the most important papers published this week in my research areas
2. Summarize key findings that relate to my recent work
3. Identify connections between external research and my notes
4. Highlight emerging trends or surprises
5. Suggest 3 specific follow-up investigations
6. Format as a newsletter-style digest with clear sections

Focus on actionable insights and connections to my existing research interests.
        """
        
        return prompt.strip()
    
    def generate_note_cleanup_prompt(self, note_path: str) -> str:
        """Generate prompt to clean up and improve a note"""
        try:
            full_path = self.vault_path / note_path
            if not full_path.exists():
                return f"Note not found: {note_path}"
                
            with open(full_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
            prompt = f"""
Please clean up and improve this note:

Current Title: {post.metadata.get('title', full_path.stem)}
Current Tags: {post.metadata.get('tags', [])}

Content:
{post.content}

Please:
1. Improve formatting and structure with clear headings
2. Suggest better tags based on content (research area tags: {[area[0] for area in self.extract_research_areas()[:5]]})
3. Add a brief summary at the top if missing
4. Identify and highlight key insights
5. Suggest internal links to related concepts
6. Improve clarity without changing meaning
7. Add metadata like creation date, source, etc.

Return the cleaned-up note in proper markdown format with frontmatter.
            """
            
            return prompt.strip()
            
        except Exception as e:
            return f"Error reading note {note_path}: {str(e)}"

def get_quick_actions(vault_path: str) -> QuickActions:
    """Factory function to create QuickActions instance"""
    return QuickActions(vault_path)