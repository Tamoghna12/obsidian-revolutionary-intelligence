#!/usr/bin/env python3
"""
Obsidian MCP Server using FastMCP
Enables Claude Desktop to read, write, and manage Obsidian vault notes
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import frontmatter
import re

from fastmcp import FastMCP
from src.enhanced_templates import TemplateManager, ProductivityFeatures
from src.revolutionary_intelligence import get_revolutionary_intelligence
from src.content_creation_engine import get_content_creation_engine
from src.knowledge_organizer import get_productivity_system

# New hybrid capabilities
from src.quick_actions import get_quick_actions
from src.persistent_memory import get_persistent_memory
from src.vault_intelligence import get_vault_intelligence
from src.proactive_assistant import get_proactive_assistant

# Initialize FastMCP server
mcp = FastMCP("Obsidian Revolutionary Intelligence")

# Initialize enhanced features
template_manager = TemplateManager()
productivity_features = None  # Will be initialized when vault path is confirmed
revolutionary_intelligence = None  # Will be initialized when vault path is confirmed
content_engine = get_content_creation_engine()  # Content creation engine
productivity_system = None  # Will be initialized when vault path is confirmed

# Initialize hybrid capabilities
quick_actions = None  # Will be initialized when vault path is confirmed
persistent_memory = None  # Will be initialized when vault path is confirmed
vault_intelligence = None  # Will be initialized when vault path is confirmed
proactive_assistant = None  # Will be initialized when vault path is confirmed

# Get vault path from environment or use default
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", 
                      os.path.expanduser("~/Documents/ObsidianVault"))

def ensure_vault_exists():
    """Ensure the vault directory exists"""
    global productivity_features, revolutionary_intelligence, productivity_system
    global quick_actions, persistent_memory, vault_intelligence, proactive_assistant
    
    if not os.path.exists(VAULT_PATH):
        print(f"Warning: Vault path does not exist: {VAULT_PATH}")
        print("Set OBSIDIAN_VAULT_PATH environment variable")
        return False
    
    # Initialize productivity features when vault is confirmed
    if productivity_features is None:
        productivity_features = ProductivityFeatures(VAULT_PATH)
    
    # Initialize revolutionary intelligence
    if revolutionary_intelligence is None:
        revolutionary_intelligence = get_revolutionary_intelligence(VAULT_PATH)
    
    # Initialize productivity system
    if productivity_system is None:
        productivity_system = get_productivity_system(VAULT_PATH)
    
    # Initialize hybrid capabilities
    if quick_actions is None:
        quick_actions = get_quick_actions(VAULT_PATH)
    
    if persistent_memory is None:
        persistent_memory = get_persistent_memory(VAULT_PATH)
    
    if vault_intelligence is None:
        vault_intelligence = get_vault_intelligence(VAULT_PATH)
    
    if proactive_assistant is None:
        proactive_assistant = get_proactive_assistant(VAULT_PATH, persistent_memory, vault_intelligence)
    
    return True

def get_note_path(relative_path: str) -> Path:
    """Get full path for a note"""
    if not relative_path.endswith('.md'):
        relative_path += '.md'
    return Path(VAULT_PATH) / relative_path

def extract_excerpt(content: str, query: str, max_length: int = 200) -> str:
    """Extract a relevant excerpt from content"""
    query_lower = query.lower()
    content_lower = content.lower()
    
    index = content_lower.find(query_lower)
    if index != -1:
        start = max(0, index - 50)
        end = min(len(content), index + max_length)
        excerpt = content[start:end]
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."
        return excerpt
    else:
        return content[:max_length] + ("..." if len(content) > max_length else "")

# Note Templates
TEMPLATES = {
    'research': '''# {title}

## Research Context
- **Project**: {project}
- **Research Question**: 
- **Date**: {date}
- **Source**: Claude Conversation

## Key Findings & Insights
{content}

## Methodology
- **Approach**: 
- **Tools Used**: 
- **Data Sources**: 

## Next Steps
- [ ] Review findings
- [ ] Validate results  
- [ ] Document methodology
- [ ] Plan follow-up research

## Related Notes
{backlinks}

---
**Tags**: {tags}''',

    'pipeline': '''# {title}

## Pipeline Overview
- **Project**: {project}
- **Objective**: 
- **Date**: {date}

## Current Analysis
{content}

## Architecture Design
### Input → Processing → Output
1. **Input Stage**: 
2. **Processing**: 
3. **Output**: 

## Implementation Plan
- [ ] Design core pipeline
- [ ] Set up environment
- [ ] Implement processing logic
- [ ] Add error handling
- [ ] Create tests
- [ ] Deploy and monitor

## Related Work
{backlinks}

---
**Tags**: {tags}''',

    'meeting': '''# {title}

## Meeting Details
- **Date**: {date}
- **Project**: {project}
- **Participants**: 

## Discussion Notes
{content}

## Decisions Made
- 

## Action Items
- [ ] 
- [ ] 
- [ ] 

## Next Meeting
- **Date**: 
- **Agenda**: 

---
**Tags**: {tags}''',
}

@mcp.tool()
def read_note(path: str) -> str:
    """
    Read the content of a specific note from the Obsidian vault
    
    Args:
        path: Path to the note file (relative to vault root, .md extension optional)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        note_path = get_note_path(path)
        if not note_path.exists():
            return f"Note not found: {path}"
        
        with open(note_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        result = f"# {note_path.stem}\n\n"
        
        if post.metadata:
            result += "**Metadata:**\n"
            for key, value in post.metadata.items():
                result += f"- **{key}**: {value}\n"
            result += "\n"
        
        result += post.content
        
        return result
        
    except Exception as e:
        return f"Error reading note: {e}"

@mcp.tool()
def write_note(path: str, content: str, tags: str = "", title: str = "") -> str:
    """
    Create or update a note in the Obsidian vault
    
    Args:
        path: Path where the note should be saved (relative to vault, .md extension optional)
        content: The markdown content of the note
        tags: Comma-separated tags for the note
        title: Title for the note (optional, uses filename if not provided)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        note_path = get_note_path(path)
        
        # Ensure directory exists
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare metadata
        metadata = {
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
        }
        
        if title:
            metadata['title'] = title
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            metadata['tags'] = tag_list
        
        # Create frontmatter post
        post = frontmatter.Post(content, **metadata)
        
        # Write the file
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Note saved: {path}"
        
    except Exception as e:
        return f"Error writing note: {e}"

@mcp.tool()
def search_notes(query: str, limit: int = 10) -> str:
    """
    Search for notes in the vault by content or filename
    
    Args:
        query: Search query (searches in filename and content)
        limit: Maximum number of results to return
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        results = []
        query_lower = query.lower()
        
        # Find all markdown files
        pattern = os.path.join(VAULT_PATH, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            relative_path = os.path.relpath(file_path, VAULT_PATH)
            filename = os.path.basename(file_path)
            
            score = 0
            
            # Score filename matches
            if query_lower in filename.lower():
                score += 10
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    content = post.content.lower()
                    
                    # Score content matches
                    content_matches = content.count(query_lower)
                    score += content_matches
                    
                    if score > 0:
                        excerpt = extract_excerpt(post.content, query)
                        results.append({
                            'path': relative_path,
                            'filename': filename.replace('.md', ''),
                            'score': score,
                            'excerpt': excerpt
                        })
                        
            except Exception:
                continue  # Skip files that can't be read
        
        # Sort by score and limit results
        results.sort(key=lambda x: x['score'], reverse=True)
        results = results[:limit]
        
        if not results:
            return f"No notes found matching: {query}"
        
        output = f"Found {len(results)} notes matching '{query}':\n\n"
        for i, result in enumerate(results, 1):
            output += f"**{i}. {result['filename']}**\n"
            output += f"Path: {result['path']}\n"
            output += f"Excerpt: {result['excerpt']}\n\n"
        
        return output
        
    except Exception as e:
        return f"Error searching notes: {e}"

@mcp.tool()
def list_notes(folder: str = "", recursive: bool = True) -> str:
    """
    List all notes in the vault or in a specific folder
    
    Args:
        folder: Optional folder path to list notes from (default: root)
        recursive: Whether to include subfolders
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        search_path = os.path.join(VAULT_PATH, folder) if folder else VAULT_PATH
        
        if recursive:
            pattern = os.path.join(search_path, "**", "*.md")
            files = glob.glob(pattern, recursive=True)
        else:
            pattern = os.path.join(search_path, "*.md")
            files = glob.glob(pattern)
        
        if not files:
            return f"No notes found in: {folder or 'vault root'}"
        
        # Sort files
        files.sort()
        
        output = f"Found {len(files)} notes"
        if folder:
            output += f" in folder: {folder}"
        output += "\n\n"
        
        for file_path in files:
            relative_path = os.path.relpath(file_path, VAULT_PATH)
            filename = os.path.basename(file_path).replace('.md', '')
            
            try:
                # Get file stats
                stat = os.stat(file_path)
                modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                
                output += f"- **{filename}**\n"
                output += f"  Path: {relative_path}\n"
                output += f"  Modified: {modified}\n\n"
                
            except Exception:
                output += f"- **{filename}** (path: {relative_path})\n\n"
        
        return output
        
    except Exception as e:
        return f"Error listing notes: {e}"

@mcp.tool()
def get_backlinks(note_path: str) -> str:
    """
    Get all notes that link to a specific note
    
    Args:
        note_path: Path to the note to find backlinks for
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        target_name = os.path.basename(note_path).replace('.md', '')
        backlinks = []
        
        # Find all markdown files
        pattern = os.path.join(VAULT_PATH, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            relative_path = os.path.relpath(file_path, VAULT_PATH)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Look for wiki-style links [[Note Name]]
                    wiki_pattern = rf'\[\[{re.escape(target_name)}(\|.*?)?\]\]'
                    # Look for markdown links [text](Note Name.md)
                    md_pattern = rf'\[.*?\]\({re.escape(target_name)}\.md\)'
                    
                    if re.search(wiki_pattern, content, re.IGNORECASE) or \
                       re.search(md_pattern, content, re.IGNORECASE):
                        backlinks.append(relative_path)
                        
            except Exception:
                continue
        
        if not backlinks:
            return f"No backlinks found for: {target_name}"
        
        output = f"Found {len(backlinks)} notes linking to '{target_name}':\n\n"
        for link in backlinks:
            filename = os.path.basename(link).replace('.md', '')
            output += f"- **{filename}** ({link})\n"
        
        return output
        
    except Exception as e:
        return f"Error finding backlinks: {e}"

@mcp.tool()
def create_structured_note(path: str, template: str, project: str = "", 
                          content: str = "", tags: str = "") -> str:
    """
    Create a note using one of the predefined templates
    
    Args:
        path: Path where the note should be saved
        template: Template type (research, pipeline, meeting, literature-review, troubleshooting, daily-note, weekly-review, project-brief, blog-post, book-notes, course-notes)
        project: Project name for the note
        content: Main content to include
        tags: Comma-separated tags
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    available_templates = list(template_manager.templates.keys())
    if template not in available_templates:
        available = ', '.join(available_templates)
        return f"Unknown template: {template}. Available: {available}"
    
    try:
        note_path = get_note_path(path)
        
        # Prepare template variables
        variables = {
            'title': os.path.basename(path).replace('.md', ''),
            'project': project or "Untitled Project",
            'content': content or "Content will be added here...",
            'tags': f"#{template}" + (f" #{tags.replace(',', ' #')}" if tags else ""),
            'backlinks': "- [[Related Note 1]]\n- [[Related Note 2]]"
        }
        
        # Add common additional variables for templates
        variables.update({
            'research_question': '',
            'hypothesis': '',
            'methodology': '',
            'main_priority': 'Focus for today',
            'energy_level': '7',
            'weekly_theme': 'Focus theme',
            'week_rating': '8'
        })
        
        # Fill template using enhanced template manager
        template_content = template_manager.fill_template(template, variables)
        
        # Create metadata
        metadata = {
            'title': variables['title'],
            'created': datetime.now().isoformat(),
            'template': template,
            'project': project
        }
        
        if tags:
            metadata['tags'] = [tag.strip() for tag in tags.split(',')]
        
        # Write note
        note_path.parent.mkdir(parents=True, exist_ok=True)
        post = frontmatter.Post(template_content, **metadata)
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Structured note created: {path} (using {template} template)"
        
    except Exception as e:
        return f"Error creating structured note: {e}"

@mcp.tool()
def vault_stats() -> str:
    """Get statistics about the Obsidian vault"""
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        pattern = os.path.join(VAULT_PATH, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        total_notes = len(files)
        total_words = 0
        tag_counts = {}
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                    # Count words
                    words = len(post.content.split())
                    total_words += words
                    
                    # Count tags
                    if 'tags' in post.metadata:
                        tags = post.metadata['tags']
                        if isinstance(tags, list):
                            for tag in tags:
                                tag_counts[tag] = tag_counts.get(tag, 0) + 1
                        
            except Exception:
                continue
        
        avg_words = total_words // total_notes if total_notes > 0 else 0
        
        # Top tags
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        output = f"**Vault Statistics**\n\n"
        output += f"📁 **Vault Path**: {VAULT_PATH}\n"
        output += f"📄 **Total Notes**: {total_notes}\n"
        output += f"📝 **Total Words**: {total_words:,}\n"
        output += f"📊 **Average Words per Note**: {avg_words}\n\n"
        
        if top_tags:
            output += "**Most Common Tags:**\n"
            for tag, count in top_tags:
                output += f"- #{tag}: {count} notes\n"
        
        return output
        
    except Exception as e:
        return f"Error getting vault stats: {e}"

# Enhanced Productivity Tools

@mcp.tool()
def list_templates(category: str = "all") -> str:
    """
    List available note templates with their descriptions and required variables
    
    Args:
        category: Template category (academic, technical, productivity, content, learning, all)
    """
    try:
        template_info = template_manager.get_template_info()
        
        if category == "all":
            result = "**Available Note Templates:**\n\n"
            for cat, templates in template_info.items():
                result += f"### {cat.title()} Templates\n"
                for template_name, info in templates.items():
                    result += f"- **{template_name}**: {info['description']}\n"
                    if info['variables']:
                        main_vars = [v for v in info['variables'] if v in ['title', 'project', 'content', 'tags']]
                        if main_vars:
                            result += f"  - Main variables: {', '.join(main_vars)}\n"
                result += "\n"
        else:
            if category in template_info:
                templates = template_info[category]
                result = f"**{category.title()} Templates:**\n\n"
                for template_name, info in templates.items():
                    result += f"- **{template_name}**: {info['description']}\n"
                    result += f"  - Variables: {', '.join(info['variables'])}\n\n"
            else:
                available_categories = ', '.join(template_info.keys())
                result = f"Category '{category}' not found. Available: {available_categories}"
        
        return result
        
    except Exception as e:
        return f"Error listing templates: {e}"

@mcp.tool()
def create_daily_note(date: str = "") -> str:
    """
    Create or open today's daily note with productivity template
    
    Args:
        date: Date in YYYY-MM-DD format (default: today)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        daily_info = productivity_features.create_daily_note(date if date else None)
        
        # Check if note already exists
        note_path = get_note_path(daily_info['path'])
        if note_path.exists():
            return f"Daily note already exists: {daily_info['path']}"
        
        # Create daily note with template
        return create_structured_note(
            path=daily_info['path'],
            template=daily_info['template'],
            tags=daily_info['suggested_tags'],
            main_priority="Focus for today",
            morning_time="9:00 AM",
            afternoon_time="1:00 PM", 
            evening_time="6:00 PM"
        )
        
    except Exception as e:
        return f"Error creating daily note: {e}"

@mcp.tool()
def create_weekly_review() -> str:
    """Create this week's review note for reflection and planning"""
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        weekly_info = productivity_features.create_weekly_review()
        
        # Check if note already exists
        note_path = get_note_path(weekly_info['path'])
        if note_path.exists():
            return f"Weekly review already exists: {weekly_info['path']}"
        
        # Create weekly review with template
        return create_structured_note(
            path=weekly_info['path'],
            template=weekly_info['template'],
            tags=weekly_info['suggested_tags'],
            weekly_theme="Focus theme for the week",
            week_rating="8"
        )
        
    except Exception as e:
        return f"Error creating weekly review: {e}"

@mcp.tool()
def get_productivity_insights() -> str:
    """Get productivity insights and suggestions based on recent activity"""
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Parse recent notes for analysis
        recent_notes = []
        for note_path in glob.glob(os.path.join(VAULT_PATH, "**", "*.md"), recursive=True):
            try:
                stat = os.stat(note_path)
                relative_path = os.path.relpath(note_path, VAULT_PATH)
                
                # Parse frontmatter to get template info
                with open(note_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                recent_notes.append({
                    'path': relative_path,
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'template': post.metadata.get('template', 'unknown'),
                    'content': post.content
                })
            except Exception:
                continue
        
        # Filter to last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_notes = [n for n in recent_notes if n['created'] > thirty_days_ago]
        
        insights = productivity_features.get_productivity_insights(recent_notes)
        suggestions = productivity_features.suggest_next_actions(recent_notes)
        
        # Get task summary
        note_contents = [n['content'] for n in recent_notes]
        task_summary = productivity_features.get_task_summary(note_contents)
        
        result = "**Productivity Insights (Last 30 Days)**\n\n"
        result += f"📊 **Overview**\n"
        result += f"- Total notes created: {insights['total_notes']}\n"
        result += f"- Most productive day: {insights['most_productive_day']}\n"
        result += f"- Most used template: {insights['most_used_template']}\n\n"
        
        result += f"✅ **Task Completion**\n"
        result += f"- Total tasks: {task_summary['total_tasks']}\n"
        result += f"- Completed: {task_summary['completed_tasks']}\n"
        result += f"- Pending: {task_summary['pending_tasks']}\n"
        result += f"- Completion rate: {task_summary['completion_rate']}%\n\n"
        
        if insights['notes_by_day']:
            result += f"📅 **Activity by Day**\n"
            for day, count in insights['notes_by_day'].items():
                result += f"- {day}: {count} notes\n"
            result += "\n"
        
        if suggestions:
            result += f"💡 **Suggested Actions**\n"
            for suggestion in suggestions:
                priority_icon = "🔴" if suggestion['priority'] == 'high' else "🟡" if suggestion['priority'] == 'medium' else "🟢"
                result += f"{priority_icon} {suggestion['action']}\n"
        
        return result
        
    except Exception as e:
        return f"Error getting productivity insights: {e}"

@mcp.tool()
def advanced_search(query: str, filters: str = "", limit: int = 10) -> str:
    """
    Advanced search with filtering options
    
    Args:
        query: Search query
        filters: Comma-separated filters (template:research, created:2024, tags:ai, etc.)
        limit: Maximum results to return
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Parse filters
        filter_dict = {}
        if filters:
            for filter_item in filters.split(','):
                if ':' in filter_item:
                    key, value = filter_item.strip().split(':', 1)
                    filter_dict[key] = value.lower()
        
        results = []
        query_lower = query.lower()
        
        # Find all markdown files
        pattern = os.path.join(VAULT_PATH, "**", "*.md")
        files = glob.glob(pattern, recursive=True)
        
        for file_path in files:
            relative_path = os.path.relpath(file_path, VAULT_PATH)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # Apply filters
                skip = False
                
                if 'template' in filter_dict:
                    if post.metadata.get('template', '').lower() != filter_dict['template']:
                        skip = True
                
                if 'created' in filter_dict:
                    created_date = post.metadata.get('created', '')
                    if filter_dict['created'] not in created_date:
                        skip = True
                
                if 'tags' in filter_dict:
                    note_tags = post.metadata.get('tags', [])
                    if isinstance(note_tags, list):
                        note_tags_lower = [tag.lower() for tag in note_tags]
                    else:
                        note_tags_lower = [str(note_tags).lower()]
                    if filter_dict['tags'] not in ' '.join(note_tags_lower):
                        skip = True
                
                if skip:
                    continue
                
                # Score content
                score = 0
                filename = os.path.basename(file_path)
                content = post.content.lower()
                
                if query_lower in filename.lower():
                    score += 10
                
                content_matches = content.count(query_lower)
                score += content_matches
                
                if score > 0:
                    excerpt = extract_excerpt(post.content, query)
                    results.append({
                        'path': relative_path,
                        'filename': filename.replace('.md', ''),
                        'score': score,
                        'excerpt': excerpt,
                        'template': post.metadata.get('template', 'unknown'),
                        'created': post.metadata.get('created', 'unknown')
                    })
                    
            except Exception:
                continue
        
        # Sort by score and limit results
        results.sort(key=lambda x: x['score'], reverse=True)
        results = results[:limit]
        
        if not results:
            return f"No notes found matching: {query} with filters: {filters}"
        
        output = f"Found {len(results)} notes matching '{query}'"
        if filters:
            output += f" with filters: {filters}"
        output += "\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"**{i}. {result['filename']}**\n"
            output += f"Path: {result['path']}\n"
            output += f"Template: {result['template']}\n"
            output += f"Created: {result['created']}\n"
            output += f"Excerpt: {result['excerpt']}\n\n"
        
        return output
        
    except Exception as e:
        return f"Error in advanced search: {e}"


# 🚀 REVOLUTIONARY INTELLIGENCE TOOLS

@mcp.tool()
def autonomous_research(topic: str, depth: str = "comprehensive") -> str:
    """
    Launch autonomous research agent that independently researches any topic across multiple sources
    
    Args:
        topic: Research topic or question
        depth: Research depth (quick, standard, comprehensive)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        import asyncio
        
        # Run the async research
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                revolutionary_intelligence.autonomous_research(topic, depth)
            )
            return result
        finally:
            loop.close()
            
    except Exception as e:
        return f"Autonomous research failed: {e}"


@mcp.tool()
def semantic_analysis(concept: str) -> str:
    """
    Analyze semantic connections and relationships for a concept in your knowledge graph
    
    Args:
        concept: Concept to analyze for semantic relationships
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        result = revolutionary_intelligence.analyze_semantic_connections(concept)
        return result
        
    except Exception as e:
        return f"Semantic analysis failed: {e}"


@mcp.tool()
def process_multimodal_content(file_path: str) -> str:
    """
    Process multi-modal content (PDF, images, audio, video) with AI analysis
    
    Args:
        file_path: Path to file to process (PDF, image, audio, video, etc.)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Handle relative paths
        if not os.path.isabs(file_path):
            file_path = os.path.join(VAULT_PATH, file_path)
        
        result = revolutionary_intelligence.process_multimodal_file(file_path)
        return result
        
    except Exception as e:
        return f"Multi-modal processing failed: {e}"


@mcp.tool()
def predictive_insights() -> str:
    """
    Get predictive insights about your research patterns and suggested future directions
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Analyze recent notes for patterns
        recent_notes = []
        for note_path in glob.glob(os.path.join(VAULT_PATH, "**", "*.md"), recursive=True):
            try:
                stat = os.stat(note_path)
                relative_path = os.path.relpath(note_path, VAULT_PATH)
                
                # Get recent notes (last 30 days)
                if datetime.now() - datetime.fromtimestamp(stat.st_ctime) < timedelta(days=30):
                    with open(note_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    recent_notes.append({
                        'path': relative_path,
                        'topic': os.path.basename(note_path).replace('.md', ''),
                        'timestamp': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'template': post.metadata.get('template', 'unknown'),
                        'content_preview': post.content[:200]
                    })
            except Exception:
                continue
        
        # Analyze patterns
        analysis = revolutionary_intelligence.predictive_intelligence.analyze_research_patterns(recent_notes)
        
        # Format output
        output = f"# 🔮 Predictive Research Insights\n\n"
        output += f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        output += f"**Notes Analyzed**: {len(recent_notes)}\n\n"
        
        if analysis.get("most_researched_topics"):
            output += f"## 📊 Your Research Focus Areas\n"
            for topic, frequency in analysis["most_researched_topics"][:10]:
                output += f"- **{topic}**: {frequency} occurrences\n"
            output += "\n"
        
        if analysis.get("predicted_interests"):
            output += f"## 🎯 Predicted Next Interests\n"
            for interest in analysis["predicted_interests"][:8]:
                output += f"- {interest}\n"
            output += "\n"
        
        if analysis.get("recommended_areas"):
            output += f"## 💡 Recommended Research Areas\n"
            for area in analysis["recommended_areas"]:
                output += f"- {area}\n"
        
        return output
        
    except Exception as e:
        return f"Predictive insights failed: {e}"


@mcp.tool()
def knowledge_graph_status() -> str:
    """
    Get status and analytics of your semantic knowledge graph
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        stats = revolutionary_intelligence.knowledge_graph.get_knowledge_graph_analysis()
        
        output = f"# 🧠 Knowledge Graph Status\n\n"
        output += f"**Total Concepts**: {stats['total_concepts']}\n"
        output += f"**Total Connections**: {stats['total_connections']}\n"
        output += f"**Connected Components**: {stats['connected_components']}\n"
        output += f"**Average Clustering**: {stats['average_clustering']:.3f}\n\n"
        
        if stats.get("most_connected_concepts"):
            output += f"## 🌟 Most Central Concepts\n"
            for concept_info in stats["most_connected_concepts"][:10]:
                output += f"- **{concept_info['concept']}** (centrality: {concept_info['centrality']:.3f})\n"
        
        if stats['total_concepts'] == 0:
            output += "\n💡 **Tip**: Your knowledge graph is empty. Use `autonomous_research` to add concepts!\n"
        
        return output
        
    except Exception as e:
        return f"Knowledge graph analysis failed: {e}"


# 📝 CONTENT CREATION & PUBLISHING TOOLS

@mcp.tool()
def process_research_paper(paper_title: str, paper_url: str = "", paper_abstract: str = "", authors: str = "") -> str:
    """
    Process a research paper (found via Claude Desktop's search) for analysis and content creation
    
    Args:
        paper_title: Title of the research paper
        paper_url: URL to the paper (optional)
        paper_abstract: Abstract/summary of the paper (optional)  
        authors: Paper authors (optional)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Create paper structure from provided information
        paper = {
            "title": paper_title,
            "authors": [author.strip() for author in authors.split(',') if author.strip()] if authors else ["Research Team"],
            "summary": paper_abstract or f"Research paper analyzing {paper_title.lower()}",
            "published": datetime.now().strftime("%Y-%m-%d"),
            "source": "Research Literature",
            "link": paper_url or "#",
            "categories": []
        }
        
        # Analyze and categorize the paper
        field = content_engine["generator"]._identify_field(paper)
        complexity = content_engine["generator"]._assess_complexity(paper)
        
        # Save paper information for future reference
        paper_path = f"Research Papers/{paper_title.replace(':', ' -')}"
        note_path = get_note_path(paper_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        paper_content = f"# {paper_title}\n\n"
        paper_content += f"**Authors**: {', '.join(paper['authors'])}\n"
        paper_content += f"**Field**: {field}\n"
        paper_content += f"**Complexity**: {complexity}\n"
        if paper_url:
            paper_content += f"**URL**: {paper_url}\n"
        paper_content += f"\n## Abstract\n{paper_abstract}\n\n"
        paper_content += f"## Analysis Notes\n*Add your analysis and insights here*\n\n"
        paper_content += f"## Related Content\n*Links to generated blog posts, scripts, etc.*\n"
        
        metadata = {
            'title': f"Paper: {paper_title}",
            'created': datetime.now().isoformat(),
            'type': 'research_paper',
            'field': field,
            'complexity': complexity,
            'processed': True
        }
        
        post = frontmatter.Post(paper_content, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        output = f"# Paper Processed: {paper_title}\n\n"
        output += f"**Field**: {field}\n"
        output += f"**Complexity Level**: {complexity}\n"
        output += f"**Paper saved to**: {paper_path}\n\n"
        output += f"## Available Content Generation Options:\n"
        output += f"1. `generate_blog_post('{paper_title}', 'accessible')` - Create blog post\n"
        output += f"2. `generate_video_script('{paper_title}', 5)` - Create video script\n"
        output += f"3. `generate_substack_post('{paper_title}', 'your commentary')` - Create Substack post\n"
        output += f"4. Add to newsletter with `generate_newsletter('{field}', '')`\n\n"
        output += f"## Analysis Ready For:\n"
        output += f"- Content creation in multiple formats\n"
        output += f"- Integration with knowledge graph\n"
        output += f"- Semantic analysis and connections\n"
        
        return output
        
    except Exception as e:
        return f"Paper processing failed: {e}"


@mcp.tool()
def generate_blog_post(paper_title: str, style: str = "accessible") -> str:
    """
    Generate a blog post from a research paper
    
    Args:
        paper_title: Title of the paper (from recent search results)
        style: Writing style (technical, accessible, academic)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # In a real implementation, would store and retrieve paper details
        # For now, create a placeholder structure
        paper = {
            "title": paper_title,
            "authors": ["Research Team"],
            "summary": f"This paper explores {paper_title.lower()} and presents novel findings in the field.",
            "published": datetime.now().strftime("%Y-%m-%d"),
            "source": "Research Literature",
            "link": "#",
            "categories": ["research"]
        }
        
        blog_post = content_engine["generator"].generate_blog_post(paper, style)
        
        # Save to vault
        blog_path = f"Generated Content/Blog Posts/{paper_title.replace(':', ' -')}"
        note_path = get_note_path(blog_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create metadata
        metadata = {
            'title': f"Blog: {paper_title}",
            'created': datetime.now().isoformat(),
            'type': 'blog_post',
            'style': style,
            'source_paper': paper_title
        }
        
        post = frontmatter.Post(blog_post, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Blog post generated and saved: {blog_path}\n\nPreview:\n{blog_post[:500]}..."
        
    except Exception as e:
        return f"Blog post generation failed: {e}"


@mcp.tool()
def generate_newsletter(theme: str = "Weekly Research Update", week_date: str = "") -> str:
    """
    Generate a research newsletter from processed papers in your vault
    
    Args:
        theme: Newsletter theme/title
        week_date: Week date (auto-generated if empty)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        if not week_date:
            week_date = datetime.now().strftime("%B %d, %Y")
        
        # Find processed papers from the last week
        papers_by_field = {}
        research_papers_dir = Path(VAULT_PATH) / "Research Papers"
        
        if research_papers_dir.exists():
            for paper_file in research_papers_dir.glob("*.md"):
                try:
                    with open(paper_file, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    # Check if processed in last 7 days
                    created_date = datetime.fromisoformat(post.metadata.get('created', datetime.now().isoformat()))
                    if datetime.now() - created_date < timedelta(days=7):
                        field = post.metadata.get('field', 'General Research')
                        if field not in papers_by_field:
                            papers_by_field[field] = []
                        
                        papers_by_field[field].append({
                            'title': post.metadata.get('title', '').replace('Paper: ', ''),
                            'authors': post.metadata.get('authors', ['Unknown']),
                            'summary': post.content[:300],
                            'link': '#',
                            'source': 'Research Literature'
                        })
                except:
                    continue
        
        # If no recent papers, create template newsletter
        if not papers_by_field:
            papers_by_field = {
                "Featured Research": [{
                    'title': 'Recent Research Updates',
                    'authors': ['Research Team'],
                    'summary': 'Use process_research_paper() to add papers from Claude Desktop search to generate content for future newsletters.',
                    'link': '#',
                    'source': 'Research Literature'
                }]
            }
        
        newsletter = content_engine["generator"].generate_newsletter(papers_by_field, week_date)
        
        # Save newsletter
        newsletter_path = f"Generated Content/Newsletters/{theme} - {week_date}"
        note_path = get_note_path(newsletter_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        total_papers = sum(len(papers) for papers in papers_by_field.values())
        
        metadata = {
            'title': f"{theme} - {week_date}",
            'created': datetime.now().isoformat(),
            'type': 'newsletter',
            'theme': theme,
            'paper_count': total_papers,
            'fields': list(papers_by_field.keys())
        }
        
        post = frontmatter.Post(newsletter, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Newsletter generated: {newsletter_path}\n\n**Papers included**: {total_papers}\n**Fields**: {', '.join(papers_by_field.keys())}\n\nPreview:\n{newsletter[:600]}..."
        
    except Exception as e:
        return f"Newsletter generation failed: {e}"


@mcp.tool()
def generate_video_script(paper_title: str, duration_minutes: int = 5) -> str:
    """
    Generate a video script from a research paper
    
    Args:
        paper_title: Title of the paper
        duration_minutes: Target video duration
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Create paper structure (would fetch real data in production)
        paper = {
            "title": paper_title,
            "authors": ["Research Team"],
            "summary": f"This research investigates {paper_title.lower()} using innovative methodologies and presents significant findings that advance the field.",
            "published": datetime.now().strftime("%Y-%m-%d"),
            "source": "Academic Research",
            "categories": ["research"]
        }
        
        script = content_engine["generator"].generate_video_script(paper, duration_minutes)
        
        # Save script
        script_path = f"Generated Content/Video Scripts/{paper_title.replace(':', ' -')}"
        note_path = get_note_path(script_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': f"Video Script: {paper_title}",
            'created': datetime.now().isoformat(),
            'type': 'video_script',
            'duration_minutes': duration_minutes,
            'source_paper': paper_title
        }
        
        post = frontmatter.Post(script, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Video script generated: {script_path}\n\nPreview:\n{script[:500]}..."
        
    except Exception as e:
        return f"Video script generation failed: {e}"


@mcp.tool()
def generate_substack_post(paper_title: str, personal_commentary: str = "") -> str:
    """
    Generate a Substack post with personal commentary
    
    Args:
        paper_title: Title of the research paper
        personal_commentary: Your personal insights and commentary (optional)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Create paper structure
        paper = {
            "title": paper_title,
            "authors": ["Research Authors"],
            "summary": f"This study examines {paper_title.lower()} through comprehensive analysis and presents novel insights that could reshape understanding in the field.",
            "published": datetime.now().strftime("%Y-%m-%d"),
            "source": "Academic Literature",
            "link": "#",
            "categories": ["research"]
        }
        
        substack_post = content_engine["generator"].generate_substack_post(paper, personal_commentary)
        
        # Save post
        post_path = f"Generated Content/Substack Posts/{paper_title.replace(':', ' -')}"
        note_path = get_note_path(post_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': f"Substack: {paper_title}",
            'created': datetime.now().isoformat(),
            'type': 'substack_post',
            'source_paper': paper_title,
            'has_commentary': bool(personal_commentary)
        }
        
        post = frontmatter.Post(substack_post, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Substack post generated: {post_path}\n\nPreview:\n{substack_post[:500]}..."
        
    except Exception as e:
        return f"Substack post generation failed: {e}"


@mcp.tool()
def generate_podcast_script(episode_title: str, topic: str, duration_minutes: int = 30) -> str:
    """
    Generate a podcast script for a given topic
    
    Args:
        episode_title: Title of the podcast episode
        topic: Topic to discuss in the podcast
        duration_minutes: Target duration of the podcast in minutes
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Create podcast structure
        podcast = {
            "title": episode_title,
            "topic": topic,
            "duration_minutes": duration_minutes,
            "episode_number": "001",  # Would be dynamically calculated in production
            "host": "Host Name",
            "guests": "Guest Experts",
            "main_question": f"What's new and exciting in {topic}?",
            "takeaway1": f"Key insight about {topic}",
            "takeaway2": f"Practical applications of {topic}",
            "takeaway3": f"Future directions in {topic}",
            "research_notes": f"Research notes about {topic}",
            "key_point1": f"Fundamentals of {topic}",
            "key_point2": f"Recent developments in {topic}",
            "key_point3": f"Future implications of {topic}",
            "question1": f"What are the biggest misconceptions about {topic}?",
            "question2": f"What exciting developments are happening in {topic}?",
            "question3": f"What should our listeners know about {topic}?",
            "intro_script": f"Welcome to our show where we explore {topic} and its impact on our world.",
            "segment1_host": f"Today we're diving into {topic} with our special guest.",
            "segment1_guest": f"Thanks for having me. {topic} is fascinating because...",
            "segment2_start": "5",
            "segment2_end": str(duration_minutes - 10),
            "segment2_host": f"Let's dig deeper into {topic}.",
            "segment2_guest": f"One of the most exciting aspects is...",
            "segment3_start": str(duration_minutes - 10),
            "segment3_end": str(duration_minutes - 5),
            "segment3_host": f"How can our listeners apply this to their work?",
            "segment3_guest": f"Here are three practical takeaways...",
            "outro_script": f"Thanks for listening to our discussion on {topic}. Don't forget to subscribe!",
            "show_notes": f"Detailed notes about {topic}",
            "link1": "https://example.com/resource1",
            "link2": "https://example.com/resource2",
            "link3": "https://example.com/resource3",
            "quote1": f"{topic} is changing the way we think about...",
            "quote2": f"The future of {topic} looks incredibly promising...",
            "series_name": "Knowledge Series",
            "category": topic
        }
        
        # Generate podcast script using template
        template_content = template_manager.fill_template('podcast-script', podcast)
        
        # Save script
        script_path = f"Generated Content/Podcast Scripts/{episode_title.replace(':', ' -')}"
        note_path = get_note_path(script_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': f"Podcast: {episode_title}",
            'created': datetime.now().isoformat(),
            'type': 'podcast_script',
            'topic': topic,
            'duration_minutes': duration_minutes
        }
        
        post = frontmatter.Post(template_content, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Podcast script generated: {script_path}\n\nPreview:\n{template_content[:500]}..."
        
    except Exception as e:
        return f"Podcast script generation failed: {e}"


@mcp.tool()
def content_pipeline_summary() -> str:
    """Get summary of content creation capabilities and recent activity"""
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Count generated content and processed papers
        content_dir = Path(VAULT_PATH) / "Generated Content"
        papers_dir = Path(VAULT_PATH) / "Research Papers"
        
        content_stats = {
            "Blog Posts": 0,
            "Newsletters": 0,
            "Video Scripts": 0,
            "Substack Posts": 0,
            "Podcast Scripts": 0
        }
        
        processed_papers = 0
        
        if content_dir.exists():
            for content_type in content_stats.keys():
                type_dir = content_dir / content_type
                if type_dir.exists():
                    content_stats[content_type] = len(list(type_dir.glob("*.md")))
        
        if papers_dir.exists():
            processed_papers = len(list(papers_dir.glob("*.md")))
        
        output = f"# 🚀 Research-to-Content Pipeline Status\n\n"
        output += f"## 📊 Content Statistics\n"
        output += f"- **Processed Papers**: {processed_papers} papers\n"
        for content_type, count in content_stats.items():
            output += f"- **{content_type}**: {count} items\n"
        
        output += f"\n## 🔍 Research Integration Workflow\n"
        output += f"1. **Search with Claude Desktop**: Use Claude's web search to find papers\n"
        output += f"2. **Process Paper**: Use `process_research_paper()` to analyze and categorize\n"  
        output += f"3. **Generate Content**: Create blogs, scripts, newsletters from processed papers\n"
        output += f"4. **Knowledge Integration**: AI analysis and semantic connections\n"
        
        output += f"\n## 📝 Content Generation Capabilities\n"
        output += f"- **Blog Posts**: Technical and accessible styles\n"
        output += f"- **Research Newsletters**: From your processed papers\n"
        output += f"- **Video Scripts**: 3-10 minute educational content\n"
        output += f"- **Substack Posts**: Long-form analysis with commentary\n"
        output += f"- **Podcast Scripts**: Structured audio content for knowledge sharing\n"
        output += f"- **Paper Analysis**: AI-powered field classification and complexity assessment\n"
        
        output += f"\n## 🎯 Unique AI Capabilities\n"
        output += f"- **Semantic Analysis**: Connect concepts across disciplines\n"
        output += f"- **Knowledge Graph**: Build relationships between ideas\n"
        output += f"- **Predictive Insights**: Suggest research directions\n"
        output += f"- **Multi-Modal Processing**: Extract insights from PDFs and documents\n"
        output += f"- **Autonomous Research**: Independent topic investigation\n"
        
        output += f"\n## 🚀 Workflow Examples\n"
        output += f"1. Find paper with Claude Desktop search → `process_research_paper('Title', 'URL', 'Abstract', 'Authors')`\n"
        output += f"2. Generate blog: `generate_blog_post('Paper Title', 'accessible')`\n"
        output += f"3. Create newsletter: `generate_newsletter('Weekly AI Update', '')`\n"
        output += f"4. Make video script: `generate_video_script('Paper Title', 5)`\n"
        output += f"5. Create podcast: `generate_podcast_script('Episode Title', 'Topic', 30)`\n"
        output += f"6. AI analysis: `semantic_analysis('concept')` or `autonomous_research('topic', 'comprehensive')`\n"
        
        return output
        
    except Exception as e:
        return f"Pipeline summary failed: {e}"


# 🎯 ADVANCED PRODUCTIVITY ENHANCEMENT TOOLS

@mcp.tool()
def create_project_workflow(project_name: str, project_type: str = "general") -> str:
    """
    Create a complete project workflow with milestones and tasks
    
    Args:
        project_name: Name of the project
        project_type: Type of project (research, content, learning, general)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get productivity enhancer components
        productivity_enhancer = get_productivity_enhancer(VAULT_PATH)
        workflow_automation = productivity_enhancer["workflow_automation"]
        
        # Create workflow
        result = workflow_automation.create_project_workflow(project_name, project_type)
        
        return f"Project workflow created: {result['message']}\nSaved to: {result['path']}"
        
    except Exception as e:
        return f"Project workflow creation failed: {e}"


@mcp.tool()
def track_project_progress(project_name: str) -> str:
    """
    Track progress on a project workflow
    
    Args:
        project_name: Name of the project to track
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get productivity enhancer components
        productivity_enhancer = get_productivity_enhancer(VAULT_PATH)
        workflow_automation = productivity_enhancer["workflow_automation"]
        
        # Track progress
        result = workflow_automation.track_project_progress(project_name)
        
        if "error" in result:
            return result["error"]
        
        output = f"# Project Progress: {project_name}\n\n"
        output += f"**Status**: {result['status']}\n"
        output += f"**Completion**: {result['completed_tasks']}/{result['total_tasks']} tasks ({result['completion_rate']}%)\n\n"
        output += f"## Phases:\n"
        for phase in result['phases']:
            output += f"- {phase}\n"
        
        return output
        
    except Exception as e:
        return f"Project progress tracking failed: {e}"


@mcp.tool()
def create_objectives_and_key_results(timeframe: str, objectives: list) -> str:
    """
    Create OKRs (Objectives and Key Results) framework
    
    Args:
        timeframe: Timeframe for OKRs (e.g., "Q3 2024", "Next 90 Days")
        objectives: List of objectives with key results
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get productivity enhancer components
        productivity_enhancer = get_productivity_enhancer(VAULT_PATH)
        goal_tracker = productivity_enhancer["goal_tracker"]
        
        # Format objectives properly
        formatted_objectives = []
        for obj in objectives:
            if isinstance(obj, dict):
                formatted_objectives.append(obj)
            elif isinstance(obj, str):
                formatted_objectives.append({"name": obj, "key_results": []})
        
        # Create OKRs
        result = goal_tracker.create_objectives_and_key_results(timeframe, formatted_objectives)
        
        return f"OKRs created: {result['message']}\nSaved to: {result['path']}"
        
    except Exception as e:
        return f"OKR creation failed: {e}"


@mcp.tool()
def start_focus_session(topic: str, planned_duration: int, environment: str = "default") -> str:
    """
    Start a deep work focus session
    
    Args:
        topic: Topic or task for the focus session
        planned_duration: Planned duration in minutes
        environment: Work environment description
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get productivity enhancer components
        productivity_enhancer = get_productivity_enhancer(VAULT_PATH)
        focus_manager = productivity_enhancer["focus_session_manager"]
        
        # Start focus session
        result = focus_manager.start_focus_session(topic, planned_duration, environment)
        
        return f"Focus session started: {result['message']}\nSession ID: {result['session']['session_id']}"
        
    except Exception as e:
        return f"Focus session start failed: {e}"


@mcp.tool()
def end_focus_session(session_id: str, achievements: list = None) -> str:
    """
    End a focus session and record achievements
    
    Args:
        session_id: Session ID from start_focus_session
        achievements: List of accomplishments during the session
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get productivity enhancer components
        productivity_enhancer = get_productivity_enhancer(VAULT_PATH)
        focus_manager = productivity_enhancer["focus_session_manager"]
        
        # End focus session
        result = focus_manager.end_focus_session(session_id, achievements)
        
        if "error" in result:
            return result["error"]
        
        return f"Focus session ended: {result['message']}"
        
    except Exception as e:
        return f"Focus session end failed: {e}"


@mcp.tool()
def get_productivity_optimization_suggestions() -> str:
    """
    Get personalized productivity optimization suggestions
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get productivity enhancer components
        productivity_enhancer = get_productivity_enhancer(VAULT_PATH)
        resource_optimizer = productivity_enhancer["resource_optimizer"]
        
        # Parse recent notes for analysis
        recent_notes = []
        for note_path in glob.glob(os.path.join(VAULT_PATH, "**", "*.md"), recursive=True):
            try:
                stat = os.stat(note_path)
                relative_path = os.path.relpath(note_path, VAULT_PATH)
                
                # Get recent notes (last 30 days)
                if datetime.now() - datetime.fromtimestamp(stat.st_ctime) < timedelta(days=30):
                    with open(note_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    recent_notes.append({
                        'path': relative_path,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'tags': post.metadata.get('tags', []),
                        'template': post.metadata.get('template', 'unknown')
                    })
            except Exception:
                continue
        
        # Analyze patterns
        patterns = resource_optimizer.analyze_productivity_patterns(recent_notes)
        suggestions = resource_optimizer.suggest_optimal_schedule({})
        
        output = f"# 🎯 Productivity Optimization Suggestions\n\n"
        output += f"## 📊 Your Productivity Patterns\n"
        output += f"- **Peak Hour**: {patterns['peak_productivity_hour']['hour']}:00 ({patterns['peak_productivity_hour']['count']} notes)\n"
        output += f"- **Peak Day**: {patterns['peak_productivity_day']['day']} ({patterns['peak_productivity_day']['count']} notes)\n\n"
        
        if patterns['popular_tags']:
            output += f"## 🔖 Popular Tags\n"
            for tag, count in patterns['popular_tags'][:5]:
                output += f"- #{tag}: {count} notes\n"
            output += "\n"
        
        output += f"## 🕐 Schedule Optimization\n"
        output += f"- **Optimal Work Hours**: {suggestions['schedule_suggestions']['optimal_work_hours']}\n"
        output += f"- **Best Focus Time**: {suggestions['schedule_suggestions']['best_focus_time']}\n"
        output += f"- **Break Schedule**: {suggestions['schedule_suggestions']['break_schedule']}\n\n"
        
        output += f"## ⚡ Implementation Tips\n"
        for tip in suggestions['implementation_tips']:
            output += f"- {tip}\n"
        
        return output
        
    except Exception as e:
        return f"Productivity optimization failed: {e}"


# 🧠 KNOWLEDGE ORGANIZATION & PRODUCTIVITY TOOLS

@mcp.tool()
def organize_knowledge_base() -> str:
    """
    Automatically categorize and organize your knowledge base
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get knowledge organizer
        knowledge_organizer = productivity_system["knowledge_organizer"]
        
        # Generate knowledge map
        knowledge_map = knowledge_organizer.generate_knowledge_map()
        
        # Save to vault
        map_path = "Knowledge Management/Knowledge Map.md"
        note_path = get_note_path(map_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': 'Knowledge Map',
            'created': datetime.now().isoformat(),
            'type': 'knowledge_map',
            'categories': 'knowledge-management'
        }
        
        post = frontmatter.Post(knowledge_map, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Knowledge base organized and map saved to: {map_path}\n\nPreview:\n{knowledge_map[:500]}..."
        
    except Exception as e:
        return f"Knowledge organization failed: {e}"


@mcp.tool()
def generate_progress_report() -> str:
    """
    Generate a comprehensive progress report of all tasks and projects
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get progress tracker
        progress_tracker = productivity_system["progress_tracker"]
        
        # Generate progress report
        progress_report = progress_tracker.generate_progress_report()
        
        # Save to vault
        report_path = "Knowledge Management/Progress Report.md"
        note_path = get_note_path(report_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': 'Progress Report',
            'created': datetime.now().isoformat(),
            'type': 'progress_report',
            'categories': 'productivity'
        }
        
        post = frontmatter.Post(progress_report, **metadata)
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Progress report generated and saved to: {report_path}\n\nPreview:\n{progress_report[:500]}..."
        
    except Exception as e:
        return f"Progress report generation failed: {e}"


@mcp.tool()
def convert_note_to_blog_post(note_path: str) -> str:
    """
    Convert an existing note to a blog post format
    
    Args:
        note_path: Path to the note to convert
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get content repurposer
        content_repurposer = productivity_system["content_repurposer"]
        
        # Convert note to blog post
        blog_post = content_repurposer.convert_note_to_blog_post(note_path)
        
        # Save to vault
        blog_path = f"Generated Content/Blog Posts/Converted_{os.path.basename(note_path).replace('.md', '')}"
        note_path_obj = get_note_path(blog_path)
        note_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': f"Blog: {os.path.basename(note_path).replace('.md', '')}",
            'created': datetime.now().isoformat(),
            'type': 'blog_post',
            'source_note': note_path,
            'format': 'converted'
        }
        
        post = frontmatter.Post(blog_post, **metadata)
        with open(note_path_obj, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Note converted to blog post and saved to: {blog_path}\n\nPreview:\n{blog_post[:500]}..."
        
    except Exception as e:
        return f"Note conversion failed: {e}"


@mcp.tool()
def create_summary_from_note(note_path: str) -> str:
    """
    Create a summary of an existing note
    
    Args:
        note_path: Path to the note to summarize
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        # Get content repurposer
        content_repurposer = productivity_system["content_repurposer"]
        
        # Create summary
        summary = content_repurposer.create_summary_from_note(note_path)
        
        # Save to vault
        summary_path = f"Summaries/{os.path.basename(note_path).replace('.md', '')}_Summary"
        note_path_obj = get_note_path(summary_path)
        note_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            'title': f"Summary: {os.path.basename(note_path).replace('.md', '')}",
            'created': datetime.now().isoformat(),
            'type': 'summary',
            'source_note': note_path
        }
        
        post = frontmatter.Post(summary, **metadata)
        with open(note_path_obj, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return f"Summary created and saved to: {summary_path}\n\nPreview:\n{summary[:500]}..."
        
    except Exception as e:
        return f"Summary creation failed: {e}"


# ==================================================
# HYBRID TOOLS: One-Click Conveniences + Unique Intelligence
# ==================================================

@mcp.tool()
def quick_research_summary() -> str:
    """
    🚀 ONE-CLICK: Generate research summary based on your areas and recent notes
    No typing needed - automatically analyzes your vault and creates targeted research summary prompt
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        prompt = quick_actions.generate_research_summary_prompt()
        return f"📊 **Research Summary Prompt Generated:**\n\n{prompt}\n\n" + \
               "💡 **Next Step:** Copy this prompt to Claude Desktop for instant research summary!"
    except Exception as e:
        return f"Error generating research summary prompt: {e}"

@mcp.tool()
def quick_blog_from_note(note_path: str) -> str:
    """
    🚀 ONE-CLICK: Convert any note to blog post
    
    Args:
        note_path: Path to note to convert (e.g., "research/my-study.md")
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        prompt = quick_actions.generate_blog_conversion_prompt(note_path)
        return f"✍️ **Blog Conversion Prompt Generated:**\n\n{prompt}\n\n" + \
               "💡 **Next Step:** Copy this prompt to Claude Desktop for instant blog post creation!"
    except Exception as e:
        return f"Error generating blog conversion prompt: {e}"

@mcp.tool()
def quick_weekly_digest() -> str:
    """
    🚀 ONE-CLICK: Generate weekly research digest
    Automatically creates newsletter-style digest based on your recent work and research areas
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        prompt = quick_actions.generate_weekly_digest_prompt()
        return f"📰 **Weekly Digest Prompt Generated:**\n\n{prompt}\n\n" + \
               "💡 **Next Step:** Copy this prompt to Claude Desktop for instant weekly digest!"
    except Exception as e:
        return f"Error generating weekly digest prompt: {e}"

@mcp.tool()
def remember_insight(content: str, insight_type: str = "general", importance: float = 0.5) -> str:
    """
    🧠 UNIQUE: Store insights across conversations for permanent memory
    
    Args:
        content: The insight or key information to remember
        insight_type: Type of insight (research, idea, connection, discovery)
        importance: Importance score 0.0-1.0
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        success = persistent_memory.store_conversation_insight(content, insight_type, importance)
        if success:
            concepts = persistent_memory.extract_concepts(content)
            for concept in concepts:
                persistent_memory.store_concept(concept)
            
            return f"✅ **Insight Stored in Permanent Memory**\n" + \
                   f"📝 Content: {content[:200]}...\n" + \
                   f"🏷️ Type: {insight_type}\n" + \
                   f"⭐ Importance: {importance}\n" + \
                   f"🧩 Concepts: {', '.join(concepts[:5])}\n\n" + \
                   "💡 This insight will be available across all future conversations!"
        else:
            return "❌ Failed to store insight"
    except Exception as e:
        return f"Error storing insight: {e}"

@mcp.tool()
def recall_concept_memory(concept: str, days_back: int = 30) -> str:
    """
    🧠 UNIQUE: Recall everything about a concept across all past conversations
    
    Args:
        concept: Concept to recall (e.g., "machine learning", "transformers")
        days_back: How many days back to search
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        history = persistent_memory.recall_concept_history(concept, days_back)
        
        if "error" in history:
            return f"🔍 No memory found for '{concept}'"
        
        concept_info = history["concept"]
        relationships = history["relationships"]
        insights = history["recent_insights"]
        
        response = f"🧠 **Memory Recall: {concept}**\n\n"
        response += f"📊 Stats: {concept_info['access_count']} accesses, importance {concept_info['importance_score']:.2f}\n\n"
        
        if relationships:
            response += f"🔗 **Connected Concepts:**\n"
            for rel in relationships[:5]:
                response += f"- {rel['concepts'][0]} ↔ {rel['concepts'][1]} ({rel['strength']:.2f})\n"
            response += "\n"
        
        if insights:
            response += f"💡 **Recent Insights ({len(insights)}):**\n"
            for insight in insights[:3]:
                response += f"- {insight['content'][:100]}...\n"
        
        return response
        
    except Exception as e:
        return f"Error recalling concept memory: {e}"

@mcp.tool()
def find_similar_notes(note_path: str, threshold: float = 0.3) -> str:
    """
    🧠 UNIQUE: Find notes similar to the given note using content analysis
    
    Args:
        note_path: Path to note to find similar notes for
        threshold: Similarity threshold (0.0-1.0)
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        similar = vault_intelligence.find_similar_notes(note_path, threshold)
        
        response = f"🔍 **Similar Notes to: {note_path}**\n\n"
        
        if similar:
            for note in similar[:6]:
                response += f"📝 **{note['title']}** (similarity: {note['similarity']:.2f})\n"
                response += f"   Path: {note['path']}\n"
                response += f"   Preview: {note['preview'][:100]}...\n"
                response += f"   Common tags: {', '.join(note['common_tags']) if note['common_tags'] else 'none'}\n\n"
        else:
            response += "No similar notes found - this appears to be unique content!\n"
        
        return response
        
    except Exception as e:
        return f"Error finding similar notes: {e}"

@mcp.tool()
def analyze_vault_health() -> str:
    """
    🧠 UNIQUE: Deep health analysis of your entire vault
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        health_report = vault_intelligence.get_vault_health_report()
        
        overview = health_report['overview']
        health_scores = health_report['health_scores']
        
        response = f"📊 **Vault Health Report**\n\n"
        response += f"📈 **Overview:** {overview['total_notes']} notes, {overview['connectivity_ratio']:.2%} connected\n"
        response += f"🏥 **Health Scores:** Connectivity {health_scores['connectivity']}/100, Organization {health_scores['organization']}/100\n\n"
        
        recommendations = health_report['recommendations']
        if recommendations:
            response += f"💡 **Recommendations:**\n"
            for rec in recommendations[:3]:
                response += f"- {rec}\n"
        
        return response
        
    except Exception as e:
        return f"Error analyzing vault health: {e}"

@mcp.tool()
def surface_forgotten_insights() -> str:
    """
    🧠 UNIQUE: Surface forgotten insights and patterns from your knowledge
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        insights = proactive_assistant.surface_forgotten_insights()
        
        response = f"💡 **Forgotten Insights**\n\n"
        
        if insights:
            for insight in insights[:5]:
                response += f"🔍 **{insight['type'].replace('_', ' ').title()}**\n"
                response += f"   {insight['insight']}\n"
                response += f"   Relevance: {insight['relevance_score']:.2f}\n\n"
        else:
            response += "No forgotten insights found - you're on top of your knowledge!\n"
        
        return response
        
    except Exception as e:
        return f"Error surfacing forgotten insights: {e}"

@mcp.tool()
def get_knowledge_summary() -> str:
    """
    🧠 UNIQUE: Get summary of your persistent knowledge memory across all conversations
    """
    if not ensure_vault_exists():
        return "Error: Vault path not found"
    
    try:
        summary = persistent_memory.get_knowledge_summary()
        
        response = f"🧠 **Knowledge Memory Summary**\n\n"
        response += f"📊 **Stats:** {summary['total_concepts']} concepts, {summary['total_relationships']} relationships, {summary['total_insights']} insights\n\n"
        
        if summary['top_concepts']:
            response += f"🌟 **Top Concepts:**\n"
            for concept in summary['top_concepts'][:6]:
                response += f"- {concept['name']} (accessed {concept['access_count']}x)\n"
        
        return response
        
    except Exception as e:
        return f"Error getting knowledge summary: {e}"


if __name__ == "__main__":
    print(f"Starting Obsidian MCP Server...")
    print(f"Vault path: {VAULT_PATH}")
    
    if ensure_vault_exists():
        print("✅ Vault found")
    else:
        print("⚠️  Vault not found - check OBSIDIAN_VAULT_PATH")
    
    mcp.run()