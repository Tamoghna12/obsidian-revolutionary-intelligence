# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This directory contains a **complete Research Intelligence and Content Creation System** built as an MCP server for Claude Desktop. It transforms Obsidian vaults into autonomous research intelligence that fetches papers from academic sources, generates multiple content formats, and manages knowledge workflows for researchers, content creators, and academics.

## Working Solution: Enhanced FastMCP Server

The active solution is in the `fastmcp-server/` directory, built with Python using the FastMCP library with extensive productivity enhancements.

### Quick Setup & Testing
```bash
cd fastmcp-server
./setup.sh                          # Setup and configure Claude Desktop
python test_enhanced_server.py      # Verify enhanced tools (12 tools)
python test_revolutionary_server.py # Verify AI research tools (5 tools)
python test_content_pipeline.py     # Verify content creation tools (6 tools)
```

### Development Commands
```bash
# Start server (for debugging)
python obsidian_server.py

# Test complete system (23 total tools)
python test_enhanced_server.py      # Core Obsidian functionality
python test_revolutionary_server.py # AI research capabilities  
python test_content_pipeline.py     # Content generation pipeline

# Environment management
source venv/bin/activate             # Activate virtual environment
pip install -r requirements.txt     # Install all dependencies
export OBSIDIAN_VAULT_PATH="/path/to/vault" # Set vault path

# Content generation testing
python -c "from content_creation_engine import get_content_creation_engine; print('Content engine ready')"
```

## Architecture

### Core Components

#### 1. FastMCP Server (`obsidian_server.py`)
- **Main Server**: 23 registered tools with @mcp.tool() decorator
- **Vault Integration**: File operations with frontmatter parsing
- **Search Engine**: Content-based search with relevance scoring
- **Template System**: Integration with enhanced template manager
- **AI Research Integration**: Revolutionary intelligence and content creation engines
- **Error Handling**: Comprehensive exception handling with user-friendly messages

#### 2. Enhanced Template System (`enhanced_templates.py`)
- **TemplateManager Class**: 12+ professional templates with variable substitution
- **ProductivityFeatures Class**: Analytics, insights, and workflow automation
- **Template Categories**: Organized by academic, technical, productivity, content, learning
- **Smart Defaults**: Auto-filled variables (date, time, status, priority)

#### 3. Revolutionary Intelligence (`revolutionary_intelligence.py`)
- **AutonomousResearchAgent**: Multi-source paper research (arXiv, Wikipedia, news)
- **SemanticKnowledgeGraph**: AI-powered concept relationships using embeddings
- **MultiModalProcessor**: PDF and document processing capabilities
- **PredictiveIntelligence**: Research pattern analysis and recommendations
- **RevolutionaryIntelligence**: Coordination hub for AI research features

#### 4. Content Creation Engine (`content_creation_engine.py`)
- **ResearchPaperFetcher**: Enhanced arXiv, bioRxiv, and medRxiv integration
- **ContentGenerator**: Multi-format content generation (blog posts, newsletters, scripts)
- **Template System**: 6 content templates (blog, newsletter, video script, Substack, thread, summary)
- **Field Classification**: Automatic research field identification and categorization
- **Academic Sources**: Real-time paper fetching with advanced filtering

#### 5. Configuration System
- **Environment Variables**: OBSIDIAN_VAULT_PATH for vault location
- **Claude Desktop Config**: Auto-generated JSON configuration
- **Setup Automation**: One-command installation via setup.sh
- **Dependency Management**: Graceful fallbacks for optional AI dependencies

### Available Tools (28 Total)

#### Core Note Management (6 tools)
1. `read_note(path)` - Read note content with metadata
2. `write_note(path, content, tags, title)` - Create/update notes with frontmatter
3. `search_notes(query, limit)` - Content search with excerpts and scoring
4. `list_notes(folder, recursive)` - Directory listing with file stats
5. `get_backlinks(note_path)` - Find wiki-style and markdown links
6. `vault_stats()` - Comprehensive vault analytics

#### Enhanced Productivity Tools (7 tools)
7. `create_structured_note(path, template, project, content, tags)` - Template-based note creation
8. `list_templates(category)` - Browse templates by category with descriptions
9. `create_daily_note(date)` - Smart daily note creation with productivity tracking
10. `create_weekly_review()` - Automated weekly review with reflection prompts
11. `get_productivity_insights()` - Analytics on activity patterns, task completion
12. `advanced_search(query, filters, limit)` - Multi-filter search (template, date, tags)
13. `create_project_workflow(project_name, project_type)` - Project workflow automation with milestones

#### Knowledge Organization Tools (4 tools)
14. `organize_knowledge_base()` - Automatic categorization and mapping
15. `generate_progress_report()` - Task and project progress tracking
16. `convert_note_to_blog_post(note_path)` - Repurpose notes as blog posts
17. `create_summary_from_note(note_path)` - Create summaries of existing notes

#### Revolutionary AI Research Tools (5 tools)
18. `autonomous_research(topic, depth)` - Launch independent multi-source research
19. `semantic_analysis(concept)` - Analyze knowledge graph relationships
20. `process_multimodal_content(file_path)` - AI-powered PDF and content processing
21. `predictive_insights()` - Research pattern analysis and recommendations
22. `knowledge_graph_status()` - Semantic network analytics and central concepts

#### Research-to-Content Pipeline Tools (7 tools)
23. `search_latest_papers(query, fields, days_back, max_results)` - Enhanced arXiv/bioRxiv search
24. `generate_blog_post(paper_title, style)` - Automated blog post creation
25. `generate_newsletter(fields, week_date)` - Research roundup newsletters
26. `generate_video_script(paper_title, duration_minutes)` - YouTube/educational scripts
27. `generate_substack_post(paper_title, personal_commentary)` - Long-form analysis posts
28. `generate_podcast_script(episode_title, topic, duration_minutes)` - Podcast episode scripts
29. `content_pipeline_summary()` - Content creation pipeline status and statistics

### Template System Architecture

#### Template Categories & Organization
```python
categories = {
    'academic': ['research', 'literature-review', 'course-notes', 'book-notes'],
    'technical': ['pipeline', 'troubleshooting'], 
    'productivity': ['daily-note', 'weekly-review', 'project-brief', 'meeting-notes'],
    'content': ['blog-post', 'book-notes'],
    'learning': ['course-notes', 'book-notes']
}
```

#### Variable Substitution System
- **Auto Variables**: `{date}`, `{time}`, `{week_date}`, `{status}`, `{priority}`
- **Custom Variables**: Project-specific fields for each template type
- **Smart Defaults**: Callable functions for dynamic values
- **Error Handling**: Graceful handling of missing variables

### Data Flow & Integration Points

#### Note Creation Pipeline
1. **Template Selection** → TemplateManager.get_template()
2. **Variable Processing** → fill_template() with defaults
3. **Frontmatter Generation** → Metadata creation with timestamps
4. **File Writing** → Path creation and UTF-8 encoding
5. **Error Response** → User-friendly error messages

#### Research-to-Content Pipeline
1. **Paper Discovery** → ResearchPaperFetcher searches arXiv/bioRxiv/medRxiv
2. **Field Classification** → ContentGenerator._identify_field() categorizes research
3. **Content Generation** → Template-based generation using ContentGenerator.templates
4. **Metadata Enrichment** → Automatic frontmatter with source paper details
5. **Vault Integration** → Saved to /Generated Content/ with organized structure

#### AI Research Pipeline
1. **Query Processing** → AutonomousResearchAgent processes research topics
2. **Multi-Source Fetching** → Async gathering from arXiv, Wikipedia, news sources
3. **Semantic Analysis** → SemanticKnowledgeGraph builds concept relationships
4. **Knowledge Synthesis** → Cross-source analysis and insights generation
5. **Graph Integration** → Updates knowledge graph with new concepts and connections

#### Search & Analytics Pipeline
1. **File Discovery** → glob.glob() recursive file finding
2. **Content Parsing** → frontmatter.load() for metadata extraction
3. **Scoring Algorithm** → Filename + content match scoring
4. **Result Ranking** → Sort by relevance with excerpt extraction
5. **Filter Application** → Multi-criteria filtering (template, date, tags, source)

### Critical Implementation Details

#### FastMCP Limitations & Workarounds
- **No **kwargs Support**: Fixed parameter sets instead of flexible kwargs
- **Tool Registration**: All functions must use @mcp.tool() decorator  
- **Error Handling**: Return strings rather than raising exceptions
- **Async Integration**: Manual event loop management for async operations

#### Content Creation Engine Integration
- **Graceful Fallbacks**: Optional dependencies with HAS_* flags for feature detection
- **Template System**: 6 content templates with variable substitution
- **Multi-Source APIs**: arXiv XML parsing, bioRxiv JSON, async aiohttp sessions
- **Field Classification**: Keyword-based research field identification with extensible mapping

#### AI Research System Integration
- **Embeddings**: Sentence-transformers with fallback handling
- **Knowledge Graph**: NetworkX with centrality calculations and semantic similarity
- **Async Coordination**: Event loop management between sync MCP tools and async research
- **Multi-Modal Processing**: PDF text extraction with PyPDF2, extensible to other formats

#### File System Integration
- **Path Resolution**: Relative to VAULT_PATH with .md extension handling
- **Directory Creation**: Auto-creation of parent directories including /Generated Content/
- **Content Organization**: Structured directories (Blog Posts/, Newsletters/, Video Scripts/, Substack Posts/)
- **Encoding**: UTF-8 for international character support
- **Frontmatter Format**: YAML metadata with python-frontmatter library

## Development Guidelines

### Adding New MCP Tools
1. Use `@mcp.tool()` decorator with comprehensive docstring
2. Include Args section with parameter descriptions
3. Implement error handling with try/except blocks
4. Return user-friendly string messages (not exceptions)
5. Test with appropriate test script (test_enhanced_server.py, test_revolutionary_server.py, test_content_pipeline.py)

### Adding Content Generation Templates
1. Add template to `ContentGenerator.templates` dictionary in content_creation_engine.py
2. Include variable placeholders with {variable_name} syntax
3. Update `_load_templates()` method with new template
4. Add generation logic in appropriate `generate_*()` method
5. Test template rendering and variable substitution

### Adding Research Paper Sources
1. Extend `ResearchPaperFetcher` class with new `search_*()` method
2. Implement async API integration following existing patterns
3. Add source to `get_trending_papers()` aggregation logic
4. Update field classification in `ContentGenerator._identify_field()`
5. Add source documentation to RESEARCH_TO_CONTENT_GUIDE.md

### Extending AI Research Capabilities
1. Add new analysis methods to appropriate revolutionary intelligence class
2. Handle optional dependencies with graceful fallbacks
3. Implement async patterns with proper event loop management
4. Update knowledge graph integration if adding new concept types
5. Test with test_revolutionary_server.py

### Common Debugging Commands
```bash
# Check vault path configuration
echo $OBSIDIAN_VAULT_PATH

# Verify Claude Desktop configuration  
cat ~/.config/Claude/claude_desktop_config.json

# Test core server imports
python -c "from obsidian_server import mcp; print('Core server ready')"

# Test revolutionary intelligence
python -c "from revolutionary_intelligence import get_revolutionary_intelligence; print('Revolutionary intelligence ready')"

# Test content creation engine
python -c "from content_creation_engine import get_content_creation_engine; print('Content engine ready')"

# Check available templates
python -c "from enhanced_templates import TemplateManager; tm = TemplateManager(); print('Enhanced templates:', list(tm.templates.keys()))"

# Check content templates
python -c "from content_creation_engine import ContentGenerator; cg = ContentGenerator(); print('Content templates:', list(cg.templates.keys()))"

# Test dependency availability
python -c "import aiohttp, feedparser, networkx, sentence_transformers; print('All major dependencies available')"

# Count total MCP tools
python -c "
import inspect
from obsidian_server import *
tools = [name for name, obj in globals().items() if hasattr(obj, '_mcp_tool')]
print(f'Total MCP tools: {len(tools)}')
"
```

## File Structure

```
obsidian_integration/
├── CLAUDE.md                            # This comprehensive development guide
├── README.md                            # User documentation  
├── fastmcp-server/                      # Complete research intelligence system
│   ├── obsidian_server.py               # Main MCP server with 23 tools
│   ├── enhanced_templates.py           # Template system & productivity features
│   ├── revolutionary_intelligence.py   # AI research & knowledge graph system
│   ├── content_creation_engine.py      # Research-to-content pipeline
│   ├── test_enhanced_server.py         # Test core Obsidian functionality (12 tools)
│   ├── test_revolutionary_server.py    # Test AI research capabilities (5 tools)
│   ├── test_content_pipeline.py        # Test content generation pipeline (6 tools)
│   ├── requirements.txt                # All Python dependencies
│   ├── setup.sh                        # Automated Claude Desktop installation
│   ├── README.md                       # User setup guide
│   ├── ENHANCED_FEATURES.md            # Core feature documentation
│   ├── RESEARCH_TO_CONTENT_GUIDE.md    # Complete content pipeline guide
│   ├── REVOLUTIONARY_USAGE_GUIDE.md    # AI research features guide
│   ├── claude_desktop_config.json      # Generated Claude Desktop config
│   └── venv/                           # Python virtual environment
└── connector.jsx                       # Original React connector (reference only)
```

## Key Usage Patterns

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

This system transforms Claude Desktop into a **complete research intelligence platform** that autonomously discovers papers, generates multi-format content, and manages knowledge workflows for researchers, academics, and content creators.

# Revolutionary Intelligence Development Context

## Project Evolution Journey
This MCP server evolved from a basic file manager to a revolutionary AI research intelligence system through several phases:

### Phase 1: Basic MCP (Completed)
- Basic file operations (read, write, search, list)
- Simple templates (research, pipeline, meeting)
- Standard productivity features

### Phase 2: Enhanced Productivity (Completed)
- 12+ professional templates with variable substitution
- Productivity analytics and insights
- Advanced search with filtering
- Template categorization system

### Phase 3: Revolutionary Intelligence (Completed)
**Achievement**: Successfully transformed into an Autonomous Research Intelligence that actively researches, discovers, connects, and evolves knowledge.

### Phase 4: Research-to-Content Pipeline (Completed)
**Achievement**: Complete content creation pipeline that transforms academic papers into publication-ready content for websites, blogs, newsletters, video scripts, and Substack posts.

## Revolutionary Features Designed

### 1. 🤖 Autonomous Research Agent
**Breakthrough**: AI that researches topics independently across multiple sources
- Searches arXiv for latest academic papers
- Pulls background from Wikipedia
- Monitors news and developments
- Cross-references multiple sources
- Generates comprehensive research synthesis
- Builds semantic knowledge graph connections

**Implementation Status**: ✅ **COMPLETED** - Fully implemented with arXiv, Wikipedia, news sources integration

### 2. 🧠 Semantic Knowledge Graph Engine  
**Breakthrough**: AI-powered semantic understanding of concept relationships
- Maps semantic relationships using embeddings
- Identifies unexpected connections across disciplines
- Calculates similarity scores with AI
- Tracks concept evolution over time
- Predicts future research directions

**Implementation Status**: ✅ **COMPLETED** - Fully operational with sentence-transformers and NetworkX

### 3. 📄 Multi-Modal Intelligence Hub
**Breakthrough**: Process any content type with full AI understanding
- Extract text from PDFs with PyPDF2
- Extensible architecture for images, audio, video
- Web content processing capabilities
- Structured data parsing support

**Implementation Status**: ✅ **COMPLETED** - PDF processing operational, extensible framework ready

### 4. 🔮 Predictive Research Intelligence
**Breakthrough**: Proactive intelligence that anticipates research needs
- Analyzes research patterns and behavior
- Identifies knowledge gaps and trending topics
- Suggests research directions based on patterns
- Predicts research interests from activity
- Provides personalized research recommendations

**Implementation Status**: ✅ **COMPLETED** - Pattern analysis and prediction algorithms operational

### 5. 🌐 Research-to-Content Pipeline
**Breakthrough**: Complete academic paper to publication pipeline
- Fetches papers from arXiv, bioRxiv, medRxiv in real-time
- Generates blogs, newsletters, video scripts, Substack posts
- Multi-format content creation with personal commentary
- Automated field classification and content optimization
- Publication-ready content for websites and platforms

**Implementation Status**: ✅ **COMPLETED** - Full pipeline operational with 6 content generation tools

## Revolutionary Architecture Files Created

### Core Revolutionary Intelligence (`revolutionary_intelligence.py`)
- `AutonomousResearchAgent`: Multi-source research automation
- `SemanticKnowledgeGraph`: AI-powered concept relationships
- `MultiModalProcessor`: Process any content type
- `PredictiveIntelligence`: Anticipate research needs
- `RevolutionaryIntelligence`: Coordination hub

### Revolutionary Tools Added to MCP Server
1. `autonomous_research(topic, depth)` - Launch independent research
2. `semantic_analysis(concept)` - Analyze knowledge graph relationships  
3. `process_multimodal_content(file_path)` - AI-powered content processing
4. `predictive_insights()` - Pattern analysis and recommendations
5. `knowledge_graph_status()` - Graph analytics and central concepts

### Revolutionary Dependencies
```
# AI and Machine Learning
sentence-transformers>=2.2.0
scikit-learn>=1.2.0
numpy>=1.23.0
torch>=1.13.0

# Web scraping and APIs
aiohttp>=3.8.0
requests>=2.28.0
beautifulsoup4>=4.11.0
feedparser>=6.0.10

# Knowledge graph
networkx>=2.8.0

# Multi-modal processing
PyPDF2>=3.0.0
pytesseract>=0.3.10
opencv-python>=4.7.0
```

## Revolutionary Use Cases Designed

### Academic Researcher Transformation
**Old**: "Let me search for papers about transformers"
**Revolutionary**: "Research transformer architectures autonomously"
→ AI independently researches, analyzes, synthesizes from 10+ sources

### Technology Professional Evolution  
**Old**: "I'll take notes on this framework"
**Revolutionary**: "Analyze this framework and connect to my knowledge graph"
→ AI extracts insights and builds semantic relationships automatically

### Knowledge Worker Revolution
**Old**: "Let me organize these meeting notes"  
**Revolutionary**: "What research directions should I explore based on my patterns?"
→ Predictive intelligence analyzes behavior and suggests directions

## Implementation Challenges Encountered

### 1. Dependency Management
- Large AI dependencies (torch, transformers) cause installation timeouts
- Need graceful fallbacks when dependencies unavailable
- Balance between features and installation complexity

### 2. Async Integration with FastMCP
- FastMCP doesn't natively support async tools
- Need event loop management for async research
- Coordination between sync MCP tools and async research agents

### 3. Performance Optimization
- AI embeddings and similarity calculations are compute-intensive
- Knowledge graph operations need optimization for large datasets
- Multi-modal processing requires significant resources

## Next Implementation Strategy

### Approach: Clean Revolutionary Build
1. Create new clean implementation directory
2. Start with core revolutionary features
3. Progressive enhancement approach
4. Dependency management strategy
5. Performance optimization from start

### Priority Revolutionary Features
1. **Autonomous Research Agent** (highest impact)
2. **Semantic Knowledge Graph** (foundational)
3. **Multi-Modal PDF Processing** (immediate value)
4. **Predictive Insights** (user engagement)
5. **Live Data Integration** (future expansion)

## Revolutionary Impact Vision

This transforms Claude Desktop from a "smart notepad" into an **Autonomous Research Intelligence** that:

1. **Thinks Ahead**: Predicts what you'll need to know
2. **Researches Independently**: Investigates topics without human intervention  
3. **Connects Everything**: Links concepts across disciplines and platforms
4. **Evolves Continuously**: Gets smarter and more useful over time
5. **Bridges Worlds**: Connects human intuition with AI capability

**Revolutionary Outcome**: Not just a better note-taking system, but a fundamental transformation of how humans work with knowledge.

## Development Context for Future Claude Instances

### What's Been Accomplished
- ✅ Complete enhanced MCP server with 23 tools across 4 categories
- ✅ Revolutionary intelligence fully implemented and operational
- ✅ Research-to-content pipeline with 6 content generation tools
- ✅ Multi-source paper fetching (arXiv, bioRxiv, medRxiv)
- ✅ AI-powered semantic knowledge graph with embeddings
- ✅ Content generation system (blog posts, newsletters, video scripts, Substack)
- ✅ Comprehensive testing suite with 3 specialized test scripts
- ✅ Production-ready autonomous research workflows
- ✅ Optimized dependency management with graceful fallbacks

### System Capabilities Delivered
- **23 MCP Tools**: Complete research intelligence and content creation
- **Multi-source Research**: Real-time paper fetching and analysis
- **AI Knowledge Graph**: Semantic concept relationships and predictions
- **Content Pipeline**: Academic papers → publication-ready content
- **Template Systems**: Both productivity templates and content generation templates
- **Autonomous Intelligence**: Independent research, analysis, and content creation

### Key Technical Decisions Made
- FastMCP chosen over TypeScript MCP SDK (simpler, more reliable)
- Sentence transformers for semantic embeddings (good performance/size ratio)
- NetworkX for knowledge graph (mature, well-documented)
- Graceful degradation strategy for optional AI features
- Progressive enhancement approach for revolutionary features

## Current System Status

**🎉 FULLY OPERATIONAL RESEARCH INTELLIGENCE SYSTEM**

- **Total MCP Tools**: 29 (across 5 categories)
- **Research Sources**: arXiv, bioRxiv, medRxiv, Wikipedia, news feeds
- **Content Formats**: Blog posts, newsletters, video scripts, Substack posts, podcast scripts
- **AI Capabilities**: Autonomous research, semantic analysis, predictive insights
- **Knowledge Management**: Enhanced templates, productivity analytics, advanced search, project workflows, automatic organization
- **Multi-Modal Processing**: PDF extraction, extensible content processing

**Ready for immediate use with Claude Desktop integration.**

This represents a complete transformation from basic note management to autonomous research intelligence with full content creation capabilities. The system is production-ready and actively operational for researchers, academics, and content creators.