# Project Context: Obsidian Revolutionary Intelligence MCP Server

## Project Overview

This is a **complete Research Intelligence and Content Creation System** built as an MCP (Model Context Protocol) server for Claude Desktop. It transforms Obsidian vaults into an autonomous research intelligence that can fetch papers from academic sources, generate multiple content formats, and manage knowledge workflows for researchers, content creators, and academics.

The system enables Claude Desktop to directly read, write, and manage Obsidian vault notes during conversations, creating true bidirectional integration between Claude and your knowledge base.

## Core Technologies

- **Python** with FastMCP framework
- **Sentence Transformers** for semantic analysis
- **NetworkX** for knowledge graph processing
- **AsyncIO** for concurrent research operations
- **arXiv, bioRxiv, medRxiv APIs** for academic paper fetching
- **Wikipedia API** for background knowledge
- **RSS feeds** for news monitoring

## Project Structure

```
obsidian_integration/
├── README.md                            # User documentation
├── CLAUDE.md                            # Developer documentation
├── connector.jsx                        # Original React connector (reference only)
├── QWEN.md                              # This file
├── fastmcp-server/                      # Complete research intelligence system
│   ├── obsidian_server.py               # Main MCP server with 23 tools
│   ├── enhanced_templates.py            # Template system & productivity features
│   ├── revolutionary_intelligence.py     # AI research & knowledge graph system
│   ├── content_creation_engine.py        # Research-to-content pipeline
│   ├── test_enhanced_server.py          # Test core Obsidian functionality (12 tools)
│   ├── test_revolutionary_server.py     # Test AI research capabilities (5 tools)
│   ├── test_content_pipeline.py         # Test content generation pipeline (6 tools)
│   ├── requirements.txt                 # All Python dependencies
│   ├── setup.sh                         # Automated Claude Desktop installation
│   ├── README.md                        # User setup guide
│   ├── ENHANCED_FEATURES.md             # Core feature documentation
│   ├── RESEARCH_TO_CONTENT_GUIDE.md     # Complete content pipeline guide
│   ├── REVOLUTIONARY_USAGE_GUIDE.md     # AI research features guide
│   ├── claude_desktop_config.json       # Generated Claude Desktop config
│   └── venv/                            # Python virtual environment
└── revolutionary-mcp-server/            # Alternative implementation directory
```

## Key Features & Capabilities

### 1. Core Obsidian Management (6 tools)
- `read_note(path)` - Read note content with metadata
- `write_note(path, content, tags, title)` - Create/update notes with frontmatter
- `search_notes(query, limit)` - Content search with excerpts and scoring
- `list_notes(folder, recursive)` - Directory listing with file stats
- `get_backlinks(note_path)` - Find wiki-style and markdown links
- `vault_stats()` - Comprehensive vault analytics

### 2. Enhanced Productivity Tools (6 tools)
- `create_structured_note(path, template, project, content, tags)` - Template-based note creation
- `list_templates(category)` - Browse templates by category with descriptions
- `create_daily_note(date)` - Smart daily note creation with productivity tracking
- `create_weekly_review()` - Automated weekly review with reflection prompts
- `get_productivity_insights()` - Analytics on activity patterns, task completion
- `advanced_search(query, filters, limit)` - Multi-filter search (template, date, tags)

### 3. Revolutionary AI Research Tools (5 tools)
- `autonomous_research(topic, depth)` - Launch independent multi-source research
- `semantic_analysis(concept)` - Analyze knowledge graph relationships
- `process_multimodal_content(file_path)` - AI-powered PDF and content processing
- `predictive_insights()` - Research pattern analysis and recommendations
- `knowledge_graph_status()` - Semantic network analytics and central concepts

### 4. Research-to-Content Pipeline Tools (6 tools)
- `process_research_paper(paper_title, paper_url, paper_abstract, authors)` - Process research papers
- `generate_blog_post(paper_title, style)` - Automated blog post creation
- `generate_newsletter(theme, week_date)` - Research roundup newsletters
- `generate_video_script(paper_title, duration_minutes)` - YouTube/educational scripts
- `generate_substack_post(paper_title, personal_commentary)` - Long-form analysis posts
- `content_pipeline_summary()` - Content creation pipeline status and statistics

## Template System

The system includes an enhanced template manager with 12+ professional templates organized by category:
- **Academic**: research, literature-review, course-notes, book-notes
- **Technical**: pipeline, troubleshooting
- **Productivity**: daily-note, weekly-review, project-brief, meeting-notes
- **Content**: blog-post, book-notes
- **Learning**: course-notes, book-notes

## Revolutionary Intelligence Architecture

### Autonomous Research Agent
AI agent that independently researches topics across multiple sources:
- arXiv for academic papers
- Wikipedia for background knowledge
- RSS feeds for news monitoring
- General web research (simulated)

### Semantic Knowledge Graph
AI-powered semantic understanding of concept relationships:
- Maps semantic relationships using embeddings
- Identifies unexpected connections across disciplines
- Calculates similarity scores with AI
- Tracks concept evolution over time

### Multi-Modal Processor
Process any content type with full AI understanding:
- PDF text extraction with PyPDF2
- Extensible architecture for images, audio, video
- Web content processing capabilities
- Structured data parsing support

### Predictive Intelligence
Proactive intelligence that anticipates research needs:
- Analyzes research patterns and behavior
- Identifies knowledge gaps and trending topics
- Suggests research directions based on patterns
- Predicts research interests from activity

### Content Creation Engine
Complete academic paper to publication pipeline:
- Fetches papers from arXiv, bioRxiv, medRxiv in real-time
- Generates blogs, newsletters, video scripts, Substack posts
- Multi-format content creation with personal commentary
- Automated field classification and content optimization

## Development Guidelines

### Adding New MCP Tools
1. Use `@mcp.tool()` decorator with comprehensive docstring
2. Include Args section with parameter descriptions
3. Implement error handling with try/except blocks
4. Return user-friendly string messages (not exceptions)
5. Test with appropriate test script

### Adding Content Generation Templates
1. Add template to `ContentGenerator.templates` dictionary
2. Include variable placeholders with {variable_name} syntax
3. Update `_load_templates()` method
4. Add generation logic in appropriate `generate_*()` method
5. Test template rendering and variable substitution

### Extending AI Research Capabilities
1. Add new analysis methods to appropriate revolutionary intelligence class
2. Handle optional dependencies with graceful fallbacks
3. Implement async patterns with proper event loop management
4. Update knowledge graph integration if adding new concept types
5. Test with test_revolutionary_server.py

## Testing

The system includes three specialized test scripts:

1. **test_enhanced_server.py** - Tests core Obsidian functionality (12 tools)
2. **test_revolutionary_server.py** - Tests AI research capabilities (5 tools)
3. **test_content_pipeline.py** - Tests content generation pipeline (6 tools)

To run tests:
```bash
cd fastmcp-server
python test_enhanced_server.py
python test_revolutionary_server.py
python test_content_pipeline.py
```

## Setup and Configuration

### Quick Setup
```bash
cd fastmcp-server
./setup.sh
```

### Environment Configuration
The system uses the `OBSIDIAN_VAULT_PATH` environment variable to locate your Obsidian vault. This is set automatically during the setup process.

### Dependencies
Install all dependencies with:
```bash
cd fastmcp-server
pip install -r requirements.txt
```

## Running the Server

### Method 1: Using the setup script (Recommended)
```bash
./setup.sh
```

### Method 2: Using the startup script
```bash
cd fastmcp-server
./start_server.sh
```

### Method 3: Manual execution
```bash
# Activate virtual environment
source venv/bin/activate

# Set your Obsidian vault path
export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"

# Run the server
python obsidian_server.py
```

### Method 4: As a background service
```bash
# Run in background
nohup python obsidian_server.py > server.log 2>&1 &
```

## Usage Examples

### Research-to-Content Workflow
```
"Search for latest CRISPR papers from bioRxiv"
→ search_latest_papers("CRISPR", "Biology,Medicine", 7, 15)

"Generate a blog post about quantum computing breakthrough"
→ generate_blog_post("Quantum Computing Advances", "accessible")

"Create this week's research newsletter"
→ generate_newsletter("AI/ML,Biology,Physics", "")

"Make a video script explaining neural networks"
→ generate_video_script("Understanding Neural Networks", 5)
```

### AI Research Intelligence
```
"Research transformer attention mechanisms autonomously"
→ autonomous_research("transformer attention mechanisms", "comprehensive")

"Analyze semantic connections between AI and neuroscience concepts"
→ semantic_analysis("artificial intelligence")

"Show my knowledge graph status"
→ knowledge_graph_status()

"What research patterns suggest I explore next?"
→ predictive_insights()
```

### Enhanced Productivity Workflows
```
"Create a structured research note using the research template"
→ create_structured_note("AI Research/Transformers Study", "research", "PhD Project", "content", "ai,ml")

"Find all pipeline notes tagged with docker from 2024"
→ advanced_search(query="", filters="template:pipeline,tags:docker,created:2024")

"Show productivity insights for my research activity"
→ get_productivity_insights()
```

## Key Implementation Details

### FastMCP Integration
- All functions use `@mcp.tool()` decorator for tool registration
- Error handling returns user-friendly string messages
- Async operations managed with manual event loop handling
- No **kwargs support - fixed parameter sets required

### File System Integration
- Path resolution relative to VAULT_PATH with .md extension handling
- Auto-creation of parent directories including structured content directories
- UTF-8 encoding for international character support
- Frontmatter format using python-frontmatter library

### AI Dependencies
The system gracefully handles missing optional AI dependencies:
- Sentence transformers for semantic embeddings
- NetworkX for knowledge graph operations
- PyPDF2 for PDF processing
- aiohttp for async HTTP requests

## Development Status

✅ **FULLY OPERATIONAL RESEARCH INTELLIGENCE SYSTEM**

- **Total MCP Tools**: 23 (across 4 categories)
- **Research Sources**: arXiv, bioRxiv, medRxiv, Wikipedia, news feeds
- **Content Formats**: Blog posts, newsletters, video scripts, Substack posts, social threads
- **AI Capabilities**: Autonomous research, semantic analysis, predictive insights
- **Knowledge Management**: Enhanced templates, productivity analytics, advanced search
- **Multi-Modal Processing**: PDF extraction, extensible content processing

This represents a complete transformation from basic note management to autonomous research intelligence with full content creation capabilities. The system is production-ready and actively operational for researchers, academics, and content creators.