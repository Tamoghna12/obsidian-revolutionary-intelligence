# Obsidian Revolutionary Intelligence MCP Server

A **FastMCP server** that enables Claude Desktop to directly read, write, and manage your Obsidian vault notes during conversations. This creates true bidirectional integration between Claude and your knowledge base, transforming it into an autonomous research intelligence.

## 🎯 What This Does

Transform Claude Desktop from a simple chatbot into your **AI research assistant** that:

- **Reads your notes** during conversations for context
- **Creates structured notes** from discussions  
- **Searches your knowledge base** to find relevant information
- **Manages your vault** with proper organization and templates
- **Builds upon** your existing knowledge over time
- **Generates multiple content formats** from research (blogs, newsletters, videos, podcasts, Substack posts)

## 🚀 Quick Start

```bash
cd fastmcp-server
./setup.sh
```

Enter your Obsidian vault path when prompted, then restart Claude Desktop.

**Test it:** Ask Claude "*Can you list all notes in my Obsidian vault?*"

## 📁 Project Structure

```
fastmcp-server/
├── obsidian_server.py     # Main FastMCP server
├── enhanced_templates.py  # Template system & productivity features
├── revolutionary_intelligence.py # AI research & knowledge graph system
├── content_creation_engine.py    # Research-to-content pipeline
├── requirements.txt       # Python dependencies
├── setup.sh              # One-command setup
├── README.md             # This file
└── venv/                 # Python environment
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Claude Desktop installed
- Obsidian vault

### Setup Process

1. **Clone or download this repository**

2. **Run the setup script:**
   ```bash
   cd fastmcp-server
   ./setup.sh
   ```
   
   The setup script will:
   - Create a Python virtual environment
   - Install all required dependencies
   - Configure Claude Desktop to connect to this server
   - Ask for your Obsidian vault path

3. **Alternative manual setup:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set your Obsidian vault path
   export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"
   
   # Run the server
   python obsidian_server.py
   ```

4. **Restart Claude Desktop** to load the new MCP server

## ▶️ Running the Server

### Method 1: Using the setup script (Recommended)
```bash
./setup.sh
```

### Method 2: Manual execution
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Set your Obsidian vault path
export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"

# Run the server
python obsidian_server.py
```

### Method 3: As a background service
```bash
# Run in background
nohup python obsidian_server.py > server.log 2>&1 &
```

## 🎛️ Available Tools

Once connected, Claude Desktop has these capabilities:

### Core Note Management (6 tools)
- `read_note(path)` - Read any note from your vault
- `write_note(path, content, tags, title)` - Create/update notes with metadata
- `search_notes(query, limit)` - Search through your entire vault
- `list_notes(folder, recursive)` - Browse notes by folder
- `get_backlinks(note_path)` - Find note connections
- `vault_stats()` - Get vault analytics

### Enhanced Productivity Tools (7 tools)
- `create_structured_note(path, template, project, content, tags)` - Use templates
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

## 📝 Content Generation Examples

### Podcast Script Generation
```
"Generate a 30-minute podcast script about the future of quantum computing"
→ generate_podcast_script("The Future of Quantum Computing", "quantum computing", 30)

"Create a podcast episode about AI ethics in healthcare"
→ generate_podcast_script("AI Ethics in Healthcare", "AI ethics", 45)
```

### Blog Post Generation
```
"Create a blog post about recent advances in neural networks"
→ generate_blog_post("Neural Network Advances", "accessible")

"Write a technical blog post about transformer architectures"
→ generate_blog_post("Transformer Architectures", "technical")
```

### Newsletter Generation
```
"Create this week's research newsletter"
→ generate_newsletter("Weekly Research Update", "")

"Generate a newsletter focused on AI and biology"
→ generate_newsletter("AI/Biology Research", "August 2024")
```

### Video Script Generation
```
"Make a 10-minute video script about CRISPR gene editing"
→ generate_video_script("CRISPR Gene Editing", 10)

"Create a YouTube video script explaining machine learning basics"
→ generate_video_script("Machine Learning Basics", 8)
```

### Substack Post Generation
```
"Write a Substack post about recent AI breakthroughs with my commentary"
→ generate_substack_post("AI Breakthroughs", "These developments are particularly exciting because...")

"Create a Substack post about climate change research"
→ generate_substack_post("Climate Change Research", "")
```

## 📁 Generated Content Organization

All generated content is automatically saved to your Obsidian vault in organized directories:

```
Your Obsidian Vault/
├── Generated Content/
│   ├── Blog Posts/
│   ├── Newsletters/
│   ├── Video Scripts/
│   ├── Substack Posts/
│   └── Podcast Scripts/
├── Research Papers/
├── Daily Notes/
├── Weekly Reviews/
└── ... (your existing notes)
```

## 🧪 Testing the System

### Run All Tests
```bash
# Test enhanced features
python test_enhanced_server.py

# Test revolutionary AI features
python test_revolutionary_server.py

# Test content creation pipeline (including podcast scripts)
python test_content_pipeline.py

# Test podcast script feature specifically
python test_podcast_feature.py
```

### Test Individual Components
```bash
# Test that server starts
python obsidian_server.py --help

# Test content engine
python -c "from content_creation_engine import ContentGenerator; cg = ContentGenerator(); print('Content engine ready')"

# Test template system
python -c "from enhanced_templates import TemplateManager; tm = TemplateManager(); print('Templates:', list(tm.templates.keys()))"
```

## 🎯 Usage Examples

### Research Session
- *"Before we discuss AI, read my existing notes about machine learning"*
- *"Create a research note summarizing our transformer discussion"*

### Content Creation Workflow
- *"Research the latest developments in quantum computing"*
- *"Generate a blog post about quantum supremacy"*  
- *"Create a podcast episode about quantum computing applications"*
- *"Make a video script explaining quantum bits"*

### Project Planning
- *"List all notes in my current-projects folder"*
- *"Create a pipeline design note for the data processing workflow"*
- *"Create a project workflow for my AI research"*
- *"Track progress on my quantum computing project"*
- *"Organize my knowledge base automatically"*

### Knowledge Discovery
- *"Search for notes mentioning 'python programming'"*
- *"What notes link to my project planning document?"*
- *"Show me my knowledge graph status"*
- *"Organize my knowledge base and show me the map"*
- *"Generate a progress report for all my tasks"*

## 🛠️ Development

### Adding New Templates
1. Add template to `TemplateManager.templates` in `enhanced_templates.py`
2. Update `TemplateManager.categories` to include the new template
3. Add description to `TemplateManager._get_template_description()`

### Adding New Content Types
1. Add template to `ContentGenerator.templates` in `content_creation_engine.py`
2. Add generation method to `ContentGenerator` class
3. Add MCP tool to `obsidian_server.py`
4. Update `test_content_pipeline.py` with new test
5. Update documentation

### Adding New Research Sources
1. Extend `ResearchPaperFetcher` class with new `search_*()` method
2. Implement async API integration following existing patterns
3. Add source to `get_trending_papers()` aggregation logic
4. Update field classification in `ContentGenerator._identify_field()`

## 📖 Documentation

- **User Guide**: This README file
- **Developer Guide**: See `CLAUDE.md` for architecture and customization
- **Enhanced Features**: See `ENHANCED_FEATURES.md`
- **Research-to-Content Pipeline**: See `RESEARCH_TO_CONTENT_GUIDE.md`
- **Revolutionary AI Features**: See `REVOLUTIONARY_USAGE_GUIDE.md`

## ✨ Why This is Powerful

- **Context Awareness** - Claude knows your existing knowledge
- **Persistent Memory** - Conversations become structured notes
- **Knowledge Building** - New insights connect to previous work
- **Zero Friction** - No manual copy/paste needed
- **Professional Output** - Structured templates and metadata
- **Multi-Format Content** - Generate blogs, newsletters, videos, podcasts from research
- **AI Research Assistant** - Autonomous research and content creation

## 🆘 Troubleshooting

### Common Issues

1. **Server won't start**
   - Check that dependencies are installed: `pip install -r requirements.txt`
   - Verify Python version is 3.8+
   - Ensure virtual environment is activated

2. **Claude Desktop not connecting**
   - Restart Claude Desktop completely
   - Check `~/.config/Claude/claude_desktop_config.json` for correct configuration
   - Verify server is running: `ps aux | grep obsidian_server.py`

3. **Obsidian vault not found**
   - Check `OBSIDIAN_VAULT_PATH` environment variable
   - Verify vault path exists and is accessible

4. **Content not saving to vault**
   - Check file permissions on vault directory
   - Verify there's sufficient disk space
   - Check server logs for errors

### Debug Commands
```bash
# Check vault path
echo $OBSIDIAN_VAULT_PATH

# Check Claude Desktop config
cat ~/.config/Claude/claude_desktop_config.json

# Test core imports
python -c "from obsidian_server import mcp; print('Server ready')"

# Count available tools
python -c "import inspect; from obsidian_server import *; tools = [name for name, obj in globals().items() if hasattr(obj, '_mcp_tool')]; print(f'Tools: {len(tools)}')"
```

## 📈 System Status

**🎉 FULLY OPERATIONAL RESEARCH INTELLIGENCE SYSTEM**

- **Total MCP Tools**: 28 (across 5 categories)
- **Research Sources**: arXiv, bioRxiv, medRxiv, Wikipedia, news feeds
- **Content Formats**: Blog posts, newsletters, video scripts, Substack posts, podcast scripts
- **AI Capabilities**: Autonomous research, semantic analysis, predictive insights
- **Knowledge Management**: Enhanced templates, productivity analytics, advanced search, project workflows, automatic organization

---

**Result**: Claude Desktop becomes your AI research partner that actually knows and manages your knowledge base! 🎉