#!/usr/bin/env python3
"""
Knowledge Organization and Productivity System for Obsidian MCP Server
Focuses on organizing existing content and managing productivity workflows
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import os
import re
from pathlib import Path
import glob

class KnowledgeOrganizer:
    """Organize and structure existing knowledge in the vault"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        
    def categorize_notes_by_content(self) -> Dict[str, Any]:
        """Automatically categorize notes based on their content"""
        categories = {
            "Research": [],
            "Projects": [],
            "Meetings": [],
            "Ideas": [],
            "Tasks": [],
            "Learning": [],
            "References": [],
            "Journal": [],
            "Templates": [],
            "Other": []
        }
        
        # Find all markdown files
        pattern = os.path.join(self.vault_path, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            relative_path = os.path.relpath(file_path, self.vault_path)
            filename = os.path.basename(file_path).replace('.md', '')
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Categorize based on content patterns
                if any(keyword in content for keyword in ["research", "study", "experiment", "hypothesis", "methodology"]):
                    categories["Research"].append(relative_path)
                elif any(keyword in content for keyword in ["project", "milestone", "deliverable", "timeline"]):
                    categories["Projects"].append(relative_path)
                elif any(keyword in content for keyword in ["meeting", "agenda", "attendees", "discussion"]):
                    categories["Meetings"].append(relative_path)
                elif any(keyword in content for keyword in ["idea", "concept", "brainstorm", "innovation"]):
                    categories["Ideas"].append(relative_path)
                elif any(keyword in content for keyword in ["task", "to do", "checklist", "[ ]", "action item"]):
                    categories["Tasks"].append(relative_path)
                elif any(keyword in content for keyword in ["learn", "course", "tutorial", "education", "book"]):
                    categories["Learning"].append(relative_path)
                elif any(keyword in content for keyword in ["reference", "bibliography", "citation", "source"]):
                    categories["References"].append(relative_path)
                elif any(keyword in content for keyword in ["daily", "weekly", "journal", "reflection", "today"]):
                    categories["Journal"].append(relative_path)
                elif "template" in filename.lower() or "template" in content:
                    categories["Templates"].append(relative_path)
                else:
                    categories["Other"].append(relative_path)
                    
            except Exception:
                categories["Other"].append(relative_path)
        
        return categories
    
    def create_tag_hierarchy(self) -> Dict[str, Any]:
        """Create a tag hierarchy based on existing tags"""
        tag_hierarchy = {}
        
        # Find all markdown files and extract tags
        pattern = os.path.join(self.vault_path, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract tags (both #tag format and tags in frontmatter)
                tags = re.findall(r'#(\w+)', content)
                
                # Look for tags in frontmatter
                if content.startswith('---'):
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end != -1:
                        frontmatter = content[3:frontmatter_end]
                        tag_matches = re.findall(r'tags?:\s*\[([^\]]+)\]', frontmatter)
                        for match in tag_matches:
                            tags.extend([tag.strip().strip('"\'') for tag in match.split(',')])
                
                # Build hierarchy
                for tag in tags:
                    if tag not in tag_hierarchy:
                        tag_hierarchy[tag] = []
                    tag_hierarchy[tag].append(os.path.relpath(file_path, self.vault_path))
                    
            except Exception:
                continue
        
        return tag_hierarchy
    
    def generate_knowledge_map(self) -> str:
        """Generate a visual knowledge map of the vault"""
        categories = self.categorize_notes_by_content()
        tag_hierarchy = self.create_tag_hierarchy()
        
        output = "# Knowledge Map\n\n"
        output += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        output += "## Categories\n\n"
        for category, notes in categories.items():
            if notes:
                output += f"### {category} ({len(notes)} notes)\n"
                for note in notes[:10]:  # Limit to 10 notes per category
                    filename = os.path.basename(note).replace('.md', '')
                    output += f"- [[{filename}]]\n"
                if len(notes) > 10:
                    output += f"- *... and {len(notes) - 10} more*\n\n"
        
        output += "## Top Tags\n\n"
        sorted_tags = sorted(tag_hierarchy.items(), key=lambda x: len(x[1]), reverse=True)
        for tag, notes in sorted_tags[:20]:  # Top 20 tags
            output += f"### #{tag} ({len(notes)} notes)\n"
            for note in notes[:5]:  # Limit to 5 notes per tag
                filename = os.path.basename(note).replace('.md', '')
                output += f"- [[{filename}]]\n"
            if len(notes) > 5:
                output += f"- *... and {len(notes) - 5} more*\n\n"
        
        return output

class ProgressTracker:
    """Track progress on tasks, projects, and goals"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
    
    def extract_tasks_from_notes(self) -> List[Dict[str, Any]]:
        """Extract all tasks from notes in the vault"""
        tasks = []
        
        # Find all markdown files
        pattern = os.path.join(self.vault_path, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            relative_path = os.path.relpath(file_path, self.vault_path)
            filename = os.path.basename(file_path).replace('.md', '')
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract tasks in various formats
                # Checkbox format: - [ ] Task or - [x] Task
                checkbox_tasks = re.findall(r'- \[([ x])\]\s*(.+)', content)
                for status, task_text in checkbox_tasks:
                    tasks.append({
                        "text": task_text.strip(),
                        "completed": status == 'x',
                        "source_note": relative_path,
                        "source_title": filename,
                        "type": "checkbox"
                    })
                
                # Numbered task format: 1. Task or 1) Task
                numbered_tasks = re.findall(r'(?:\d+\.|\d+\))\s*(.+)', content)
                for task_text in numbered_tasks:
                    # Check if it's already captured as a checkbox task
                    if not any(task_text.strip() == task["text"] for task in tasks if task["source_note"] == relative_path):
                        tasks.append({
                            "text": task_text.strip(),
                            "completed": False,
                            "source_note": relative_path,
                            "source_title": filename,
                            "type": "numbered"
                        })
                        
            except Exception:
                continue
        
        return tasks
    
    def generate_progress_report(self) -> str:
        """Generate a progress report based on tasks in the vault"""
        tasks = self.extract_tasks_from_notes()
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task["completed"])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Group tasks by source note
        tasks_by_note = {}
        for task in tasks:
            if task["source_note"] not in tasks_by_note:
                tasks_by_note[task["source_note"]] = []
            tasks_by_note[task["source_note"]].append(task)
        
        output = "# Progress Report\n\n"
        output += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        output += f"## Overall Progress\n"
        output += f"- **Total Tasks:** {total_tasks}\n"
        output += f"- **Completed Tasks:** {completed_tasks}\n"
        output += f"- **Completion Rate:** {completion_rate:.1f}%\n\n"
        
        output += f"## Tasks by Note\n\n"
        for note_path, note_tasks in tasks_by_note.items():
            completed_in_note = sum(1 for task in note_tasks if task["completed"])
            note_completion_rate = (completed_in_note / len(note_tasks) * 100) if note_tasks else 0
            
            filename = os.path.basename(note_path).replace('.md', '')
            output += f"### [[{filename}]] ({note_completion_rate:.1f}% complete)\n"
            output += f"- Total: {len(note_tasks)} tasks\n"
            output += f"- Completed: {completed_in_note} tasks\n\n"
        
        return output

class ContentRepurposer:
    """Convert existing content into different formats"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
    
    def convert_note_to_blog_post(self, note_path: str) -> str:
        """Convert a note to a blog post format"""
        full_path = os.path.join(self.vault_path, note_path)
        
        if not os.path.exists(full_path):
            return f"Note not found: {note_path}"
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from filename or frontmatter
            title = os.path.basename(note_path).replace('.md', '')
            
            # Simple conversion - in practice, this would be more sophisticated
            blog_post = f"# {title}\n\n"
            blog_post += "## Introduction\n\n"
            blog_post += "This post is based on my notes and explores key concepts in this area.\n\n"
            blog_post += "## Main Content\n\n"
            blog_post += content[:1000] + "...\n\n"  # Truncate for demo
            blog_post += "## Conclusion\n\n"
            blog_post += "These notes represent my current understanding of the topic. I'll continue to update and refine this as I learn more.\n\n"
            blog_post += "---\n"
            blog_post += f"*Originally from [[{title}]]*"
            
            return blog_post
            
        except Exception as e:
            return f"Error converting note: {e}"
    
    def create_summary_from_note(self, note_path: str) -> str:
        """Create a summary of a note"""
        full_path = os.path.join(self.vault_path, note_path)
        
        if not os.path.exists(full_path):
            return f"Note not found: {note_path}"
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key points (simplified approach)
            lines = content.split('\n')
            key_points = [line.strip('- ') for line in lines if line.strip().startswith('- ') and len(line.strip()) > 10]
            
            summary = f"# Summary of {os.path.basename(note_path).replace('.md', '')}\n\n"
            summary += "## Key Points\n\n"
            for i, point in enumerate(key_points[:10], 1):  # Limit to 10 points
                summary += f"{i}. {point}\n"
            
            if len(key_points) > 10:
                summary += f"\n*... and {len(key_points) - 10} more points*\n"
            
            summary += f"\n---\n*Summary generated from [[{os.path.basename(note_path).replace('.md', '')}]]*"
            
            return summary
            
        except Exception as e:
            return f"Error creating summary: {e}"

# Global instances
knowledge_organizer = None
progress_tracker = None
content_repurposer = None

def get_productivity_system(vault_path: str):
    """Get or create productivity system components"""
    global knowledge_organizer, progress_tracker, content_repurposer
    
    if knowledge_organizer is None:
        knowledge_organizer = KnowledgeOrganizer(vault_path)
    if progress_tracker is None:
        progress_tracker = ProgressTracker(vault_path)
    if content_repurposer is None:
        content_repurposer = ContentRepurposer(vault_path)
    
    return {
        "knowledge_organizer": knowledge_organizer,
        "progress_tracker": progress_tracker,
        "content_repurposer": content_repurposer
    }