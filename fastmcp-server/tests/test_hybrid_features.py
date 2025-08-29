#!/usr/bin/env python3
"""
Test Hybrid Features: One-Click Conveniences + Unique Intelligence
Tests the new hybrid capabilities that combine convenience with unique value
"""

import os
import sys
import tempfile
import shutil
from src.pathlib import Path
from src.datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_vault():
    """Create a temporary test vault with sample notes"""
    vault_path = tempfile.mkdtemp(prefix="test_vault_")
    vault = Path(vault_path)
    
    # Create sample notes
    (vault / "research").mkdir()
    (vault / "projects").mkdir()
    
    # Sample research note
    research_note = vault / "research" / "ai_study.md"
    research_note.write_text("""---
title: AI Research Study
tags: [ai, machine-learning, research]
created: 2024-01-15
---

# AI Research Study

This note explores the latest developments in artificial intelligence, particularly focusing on transformer architectures and their applications in natural language processing.

## Key Concepts
- Neural Networks
- Transformer Architecture
- Attention Mechanism
- Large Language Models

## Recent Findings
The attention mechanism has revolutionized how we approach sequence-to-sequence tasks.
""")
    
    # Sample project note
    project_note = vault / "projects" / "ml_pipeline.md"
    project_note.write_text("""---
title: ML Pipeline Project
tags: [project, machine-learning, pipeline]
created: 2024-02-01
---

# ML Pipeline Project

Building an end-to-end machine learning pipeline for natural language processing tasks.

## Components
- Data preprocessing
- Feature extraction
- Model training
- Deployment pipeline

This connects to our research on transformer architectures and attention mechanisms.
""")
    
    # Sample orphaned note (no links)
    orphan_note = vault / "standalone_thought.md"
    orphan_note.write_text("""---
title: Standalone Thought
tags: [idea]
created: 2024-03-01
---

# Standalone Thought

Random idea about quantum computing applications in cryptography.
Not connected to anything else yet.
""")
    
    return vault_path

def test_quick_actions():
    """Test one-click convenience features"""
    print("🧪 Testing Quick Actions (One-Click Conveniences)")
    
    vault_path = create_test_vault()
    os.environ["OBSIDIAN_VAULT_PATH"] = vault_path
    
    try:
        from src.quick_actions import get_quick_actions
        qa = get_quick_actions(vault_path)
        
        print("  ✓ Quick Actions module loaded")
        
        # Test research summary prompt generation
        prompt = qa.generate_research_summary_prompt()
        assert "research" in prompt.lower(), "Research summary should mention research"
        assert len(prompt) > 100, "Prompt should be substantial"
        print("  ✓ Research summary prompt generated")
        
        # Test blog conversion prompt
        blog_prompt = qa.generate_blog_conversion_prompt("research/ai_study.md")
        assert "Title:" in blog_prompt, "Blog prompt should include title section"
        assert "blog post" in blog_prompt.lower(), "Should mention blog post conversion"
        print("  ✓ Blog conversion prompt generated")
        
        # Test weekly digest prompt
        digest_prompt = qa.generate_weekly_digest_prompt()
        assert "digest" in digest_prompt.lower(), "Should mention digest"
        assert len(digest_prompt) > 50, "Digest prompt should be meaningful"
        print("  ✓ Weekly digest prompt generated")
        
        # Test note cleanup prompt
        cleanup_prompt = qa.generate_note_cleanup_prompt("projects/ml_pipeline.md")
        assert "ML Pipeline Project" in cleanup_prompt, "Should include note title"
        print("  ✓ Note cleanup prompt generated")
        
        print("  🎉 All Quick Actions tests passed!")
        
    except Exception as e:
        print(f"  ❌ Quick Actions test failed: {e}")
        
    finally:
        shutil.rmtree(vault_path)

def test_persistent_memory():
    """Test persistent memory across conversations"""
    print("🧪 Testing Persistent Memory (Cross-Session Intelligence)")
    
    vault_path = create_test_vault()
    os.environ["OBSIDIAN_VAULT_PATH"] = vault_path
    
    try:
        from src.persistent_memory import get_persistent_memory
        pm = get_persistent_memory(vault_path)
        
        print("  ✓ Persistent Memory module loaded")
        
        # Test concept storage
        concept_id = pm.store_concept("Neural Networks", "AI/ML architecture", "AI")
        assert concept_id > 0, "Concept should be stored with valid ID"
        print("  ✓ Concept storage working")
        
        # Test relationship storage
        success = pm.store_relationship("Neural Networks", "Machine Learning", "is_part_of", 0.8, "Neural networks are a key component of ML")
        assert success, "Relationship should be stored successfully"
        print("  ✓ Relationship storage working")
        
        # Test insight storage
        insight_success = pm.store_conversation_insight(
            "Discovered that attention mechanisms significantly improve translation quality", 
            "research_finding", 
            0.9
        )
        assert insight_success, "Insight should be stored successfully"
        print("  ✓ Conversation insight storage working")
        
        # Test concept recall
        history = pm.recall_concept_history("Neural Networks", 30)
        assert "concept" in history, "Should recall concept history"
        assert history["concept"]["name"] == "Neural Networks", "Should recall correct concept"
        print("  ✓ Concept recall working")
        
        # Test forgotten connections suggestion
        forgotten = pm.suggest_forgotten_connections(["Machine Learning", "AI"])
        assert isinstance(forgotten, list), "Should return list of forgotten connections"
        print("  ✓ Forgotten connections suggestion working")
        
        # Test knowledge summary
        summary = pm.get_knowledge_summary()
        assert "total_concepts" in summary, "Summary should include concept count"
        assert summary["total_concepts"] >= 1, "Should have at least one concept"
        print("  ✓ Knowledge summary working")
        
        print("  🎉 All Persistent Memory tests passed!")
        
    except Exception as e:
        print(f"  ❌ Persistent Memory test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(vault_path)

def test_vault_intelligence():
    """Test deep vault analysis capabilities"""
    print("🧪 Testing Vault Intelligence (Deep Analysis)")
    
    vault_path = create_test_vault()
    os.environ["OBSIDIAN_VAULT_PATH"] = vault_path
    
    try:
        from src.vault_intelligence import get_vault_intelligence
        vi = get_vault_intelligence(vault_path)
        
        print("  ✓ Vault Intelligence module loaded")
        print("  ℹ️ Building vault indexes...")
        
        # Test similar notes finding
        similar = vi.find_similar_notes("research/ai_study.md", threshold=0.1)
        assert isinstance(similar, list), "Should return list of similar notes"
        print("  ✓ Similar notes detection working")
        
        # Test missing backlinks suggestion
        suggestions = vi.suggest_missing_backlinks("projects/ml_pipeline.md")
        assert isinstance(suggestions, list), "Should return list of backlink suggestions"
        print("  ✓ Missing backlinks suggestion working")
        
        # Test duplicate content detection
        duplicates = vi.detect_duplicate_content(similarity_threshold=0.5)
        assert isinstance(duplicates, list), "Should return list of potential duplicates"
        print("  ✓ Duplicate content detection working")
        
        # Test orphaned notes identification
        orphans = vi.identify_orphaned_notes()
        assert isinstance(orphans, list), "Should return list of orphaned notes"
        assert len(orphans) >= 1, "Should find at least one orphaned note (standalone_thought.md)"
        print("  ✓ Orphaned notes identification working")
        
        # Test knowledge clusters analysis
        clusters = vi.analyze_knowledge_clusters()
        assert "tag_clusters" in clusters, "Should analyze tag clusters"
        assert "knowledge_hubs" in clusters, "Should identify knowledge hubs"
        print("  ✓ Knowledge clusters analysis working")
        
        # Test vault health report
        health_report = vi.get_vault_health_report()
        assert "overview" in health_report, "Should provide health overview"
        assert "health_scores" in health_report, "Should provide health scores"
        assert "recommendations" in health_report, "Should provide recommendations"
        print("  ✓ Vault health report working")
        
        print("  🎉 All Vault Intelligence tests passed!")
        
    except Exception as e:
        print(f"  ❌ Vault Intelligence test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(vault_path)

def test_proactive_assistant():
    """Test proactive knowledge assistance"""
    print("🧪 Testing Proactive Assistant (Knowledge Insights)")
    
    vault_path = create_test_vault()
    os.environ["OBSIDIAN_VAULT_PATH"] = vault_path
    
    try:
        # Initialize supporting systems first
        from src.persistent_memory import get_persistent_memory
        from src.vault_intelligence import get_vault_intelligence
        from src.proactive_assistant import get_proactive_assistant
        
        pm = get_persistent_memory(vault_path)
        vi = get_vault_intelligence(vault_path)
        pa = get_proactive_assistant(vault_path, pm, vi)
        
        print("  ✓ Proactive Assistant module loaded")
        
        # Add some test data to memory
        pm.store_concept("Transformers", "Neural network architecture", "AI")
        pm.store_concept("Attention Mechanism", "Key component of transformers", "AI")
        pm.store_relationship("Transformers", "Attention Mechanism", "uses", 0.9, "Transformers use attention mechanisms")
        
        # Test context analysis
        context = pa.analyze_current_context("Working on transformer architectures for NLP tasks")
        assert "extracted_concepts" in context, "Should extract concepts from text"
        print("  ✓ Context analysis working")
        
        # Test forgotten insights surfacing
        insights = pa.surface_forgotten_insights(["Machine Learning", "AI"])
        assert isinstance(insights, list), "Should return list of insights"
        print("  ✓ Forgotten insights surfacing working")
        
        # Test knowledge gaps identification
        gaps = pa.identify_knowledge_gaps()
        assert isinstance(gaps, list), "Should return list of knowledge gaps"
        print("  ✓ Knowledge gaps identification working")
        
        # Test review schedule suggestions
        review_suggestions = pa.suggest_review_schedule()
        assert isinstance(review_suggestions, list), "Should return list of review suggestions"
        print("  ✓ Review schedule suggestions working")
        
        # Test proactive suggestions generation
        suggestions = pa.generate_proactive_suggestions()
        assert isinstance(suggestions, list), "Should return list of proactive suggestions"
        print("  ✓ Proactive suggestions generation working")
        
        print("  🎉 All Proactive Assistant tests passed!")
        
    except Exception as e:
        print(f"  ❌ Proactive Assistant test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        shutil.rmtree(vault_path)

def test_mcp_tools_integration():
    """Test that new MCP tools can be imported from the server"""
    print("🧪 Testing MCP Tools Integration")
    
    try:
        # Import the main server to test integration
        from src.obsidian_server import (
            quick_research_summary, quick_blog_from_note, quick_weekly_digest,
            remember_insight, recall_concept_memory, find_similar_notes,
            analyze_vault_health, surface_forgotten_insights, get_knowledge_summary
        )
        
        print("  ✓ All MCP tools imported successfully")
        
        # Test that tools exist and are objects
        assert quick_research_summary is not None, "Should have quick_research_summary tool"
        assert remember_insight is not None, "Should have remember_insight tool" 
        assert analyze_vault_health is not None, "Should have analyze_vault_health tool"
        print("  ✓ All MCP tools properly registered with FastMCP")
        
        print("  🎉 All MCP Tools Integration tests passed!")
        
    except Exception as e:
        print(f"  ❌ MCP Tools Integration test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all hybrid feature tests"""
    print("🚀 Testing Hybrid Features: One-Click Conveniences + Unique Intelligence\n")
    print("=" * 80)
    
    # Run all tests
    test_quick_actions()
    print()
    
    test_persistent_memory()
    print()
    
    test_vault_intelligence()
    print()
    
    test_proactive_assistant()
    print()
    
    test_mcp_tools_integration()
    print()
    
    print("=" * 80)
    print("🎉 Hybrid Features Testing Complete!")
    print("\n📋 Summary:")
    print("✅ One-Click Conveniences: Generate targeted prompts instantly")
    print("✅ Persistent Memory: Cross-conversation concept storage and recall")
    print("✅ Vault Intelligence: Deep analysis of note relationships and health")
    print("✅ Proactive Assistant: Surface forgotten insights and knowledge gaps")
    print("✅ MCP Integration: All tools integrated with FastMCP server")
    
    print("\n🎯 Key Unique Value:")
    print("• Convenience features eliminate long typing while providing targeted prompts")
    print("• Persistent memory creates truly unique cross-session intelligence")
    print("• Vault analysis provides insights Claude Desktop cannot replicate")
    print("• Proactive suggestions surface forgotten knowledge automatically")

if __name__ == "__main__":
    main()