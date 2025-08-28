# Changelog

All notable changes to the Obsidian Revolutionary Intelligence MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-08-28

### Added
- Knowledge Organization Tools (4 new tools)
  - `organize_knowledge_base()` - Automatic categorization and mapping
  - `generate_progress_report()` - Task and project progress tracking
  - `convert_note_to_blog_post(note_path)` - Repurpose notes as blog posts
  - `create_summary_from_note(note_path)` - Create summaries of existing notes
- Knowledge Organizer module (`knowledge_organizer.py`)
- Test suite for knowledge organization features (`test_knowledge_organization.py`)
- GitHub repository setup files (LICENSE, CONTRIBUTING.md, CHANGELOG.md)
- Enhanced documentation and README files

### Changed
- Updated documentation to reflect new tools (29 total tools across 5 categories)
- Enhanced main README with comprehensive feature list and better structure
- Improved project structure with proper GitHub files
- Updated CLAUDE.md with new tool counts and categories

### Fixed
- Minor bug fixes in productivity features
- Improved test coverage for all functionality

## [1.0.0] - 2025-08-28

### Added
- Initial release of Obsidian Revolutionary Intelligence MCP Server
- Core Note Management (6 tools)
- Enhanced Productivity Tools (7 tools)
  - Project workflow automation
  - Objectives and Key Results (OKRs)
  - Deep work focus session tracking
  - Productivity pattern analysis
- Revolutionary AI Research Tools (5 tools)
- Research-to-Content Pipeline Tools (7 tools)
- One-command setup with `setup.sh`
- Comprehensive documentation
- Test suite for all functionality
- MIT License

### Features
- Bidirectional integration between Claude Desktop and Obsidian
- Autonomous research capabilities
- Semantic knowledge graph analysis
- Multi-format content generation (blogs, newsletters, videos, podcasts, Substack posts)
- Advanced note templates and productivity features
- Multi-modal content processing (PDFs, web content)
- Predictive insights and research pattern analysis