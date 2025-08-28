# Obsidian Revolutionary Intelligence MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0%2B-orange)](https://gofastmcp.com)

A **revolutionary FastMCP server** that transforms Claude Desktop into your personal AI research assistant and productivity powerhouse. This system enables true bidirectional integration between Claude and your Obsidian vault, creating an autonomous knowledge management system that can read, write, organize, and generate content from your notes.

## 🎯 What This Does

Transform Claude Desktop from a simple chatbot into your **AI research assistant** that:

- **Reads your notes** during conversations for context
- **Creates structured notes** from discussions  
- **Searches your knowledge base** to find relevant information
- **Manages your vault** with proper organization and templates
- **Builds upon** your existing knowledge over time
- **Generates multiple content formats** from research (blogs, newsletters, videos, podcasts, Substack posts)
- **Organizes your knowledge** automatically with categorization and mapping
- **Tracks your progress** on tasks and projects
- **Repurposes existing content** into new formats

## 🚀 Quick Demo

https://github.com/user-attachments/assets/placeholder-video-demo.mp4

*(Video showing Claude Desktop integrated with Obsidian, automatically creating notes, generating content, and organizing knowledge)*

## 📁 Project Structure

```
obsidian_integration/
├── README.md                            # This file
├── LICENSE                              # MIT License
├── .gitignore                           # Git ignore file
├── CLAUDE.md                            # Developer documentation
├── QWEN.md                              # AI assistant context
└── fastmcp-server/                      # Main implementation ⭐
    ├── obsidian_server.py               # Main FastMCP server
    ├── enhanced_templates.py            # Template system & productivity features
    ├── revolutionary_intelligence.py    # AI research & knowledge graph system
    ├── content_creation_engine.py       # Research-to-content pipeline
    ├── knowledge_organizer.py           # Knowledge organization system
    ├── requirements.txt                 # Python dependencies
    ├── setup.sh                         # One-command setup
    ├── start_server.sh                  # Server startup script
    ├── README.md                        # Detailed server docs
    └── venv/                            # Python environment
```

## 🛠️ Available Tools (29 Total)

### Core Note Management (6 tools)
- `read_note(path)` - Read any note from your vault
- `write_note(path, content, tags, title)` - Create/update notes with metadata
- `search_notes(query, limit)` - Search through your entire vault
- `list_notes(folder, recursive)` - Browse notes by folder
- `get_backlinks(note_path)` - Find note connections
- `vault_stats()` - Get vault analytics

### Enhanced Productivity Tools (7 tools)
- `create_structured_note(path, template, project, content, tags)` - Template-based note creation
- `list_templates(category)` - Browse templates by category
- `create_daily_note(date)` - Smart daily note creation
- `create_weekly_review()` - Automated weekly review
- `get_productivity_insights()` - Analytics on activity patterns
- `advanced_search(query, filters, limit)` - Multi-filter search
- `create_project_workflow(project_name, project_type)` - Project workflow automation

### Knowledge Organization Tools (4 tools)
- `organize_knowledge_base()` - Automatic categorization and mapping
- `generate_progress_report()` - Task and project progress tracking
- `convert_note_to_blog_post(note_path)` - Repurpose notes as blog posts
- `create_summary_from_note(note_path)` - Create summaries of existing notes

### Revolutionary AI Research Tools (5 tools)
- `autonomous_research(topic, depth)` - Launch independent multi-source research
- `semantic_analysis(concept)` - Analyze knowledge graph relationships
- `process_multimodal_content(file_path)` - AI-powered PDF/content processing
- `predictive_insights()` - Research pattern analysis and recommendations
- `knowledge_graph_status()` - Semantic network analytics

### Research-to-Content Pipeline Tools (7 tools)
- `process_research_paper(paper_title, paper_url, paper_abstract, authors)` - Process papers
- `generate_blog_post(paper_title, style)` - Automated blog post creation
- `generate_newsletter(theme, week_date)` - Research roundup newsletters
- `generate_video_script(paper_title, duration_minutes)` - YouTube/educational scripts
- `generate_substack_post(paper_title, personal_commentary)` - Long-form analysis posts
- `generate_podcast_script(episode_title, topic, duration_minutes)` - Podcast episode scripts
- `content_pipeline_summary()` - Content creation pipeline status

## 🚀 Quick Start

```bash
cd fastmcp-server
./setup.sh
```

Enter your Obsidian vault path when prompted, then restart Claude Desktop.

**Test it:** Ask Claude "*Can you list all notes in my Obsidian vault?*"

## 📖 Documentation

- **User Guide**: See `fastmcp-server/README.md` for detailed setup and usage
- **Developer Guide**: See `CLAUDE.md` for architecture and customization
- **AI Assistant Context**: See `QWEN.md` for development context

## 🎯 Example Use Cases

### Research Session
> *"Before we discuss AI, read my existing notes about machine learning"*
> 
> *"Create a research note summarizing our transformer discussion"*

### Content Creation Workflow
> *"Research the latest developments in quantum computing"*
> 
> *"Generate a blog post about quantum supremacy"*  
> 
> *"Create a podcast episode about quantum computing applications"*
> 
> *"Make a video script explaining quantum bits"*

### Project Planning
> *"List all notes in my current-projects folder"*
> 
> *"Create a pipeline design note for the data processing workflow"*
> 
> *"Create a project workflow for my AI research project"*
> 
> *"Track progress on my quantum computing research"*
> 
> *"Organize my knowledge base automatically"*

### Knowledge Discovery
> *"Search for notes mentioning 'python programming'"*
> 
> *"What notes link to my project planning document?"*
> 
> *"Show me my knowledge graph status"*
> 
> *"Organize my knowledge base and show me the map"*
> 
> *"Generate a progress report for all my tasks"*

## ✨ Why This is Powerful

- **Context Awareness** - Claude knows your existing knowledge
- **Persistent Memory** - Conversations become structured notes
- **Knowledge Building** - New insights connect to previous work
- **Zero Friction** - No manual copy/paste needed
- **Professional Output** - Structured templates and metadata
- **Multi-Format Content** - Generate blogs, newsletters, videos, podcasts from research
- **AI Research Assistant** - Autonomous research and content creation
- **Knowledge Organization** - Automatic categorization and mapping

## 📈 System Status

**🎉 FULLY OPERATIONAL RESEARCH INTELLIGENCE SYSTEM**

- **Total MCP Tools**: 29 (across 5 categories)
- **Research Sources**: arXiv, bioRxiv, medRxiv, Wikipedia, news feeds
- **Content Formats**: Blog posts, newsletters, video scripts, Substack posts, podcast scripts
- **AI Capabilities**: Autonomous research, semantic analysis, predictive insights
- **Knowledge Management**: Enhanced templates, productivity analytics, advanced search, project workflows, automatic organization
- **Multi-Modal Processing**: PDF extraction, extensible content processing

---

**Result**: Claude Desktop becomes your AI research partner that actually knows and manages your knowledge base! 🎉

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest enhancements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the [FastMCP](https://gofastmcp.com) team for the excellent framework
- Inspired by the Obsidian community's innovative workflows
- Built for researchers, content creators, and knowledge workers everywhere