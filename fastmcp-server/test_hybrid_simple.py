#!/usr/bin/env python3
"""
Simple test for hybrid features to verify core functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_vault():
    """Create a temporary test vault"""
    vault_path = tempfile.mkdtemp(prefix="test_vault_")
    vault = Path(vault_path)
    
    # Create sample note
    research_note = vault / "ai_study.md"
    research_note.write_text("""---
title: AI Research Study
tags: [ai, machine-learning]
---

# AI Research Study

Research on transformer architectures and attention mechanisms.
""")
    
    return vault_path

def test_hybrid_features():
    """Test that all hybrid components work together"""
    print("🧪 Testing Hybrid Features Integration")
    
    vault_path = create_test_vault()
    os.environ["OBSIDIAN_VAULT_PATH"] = vault_path
    
    try:
        # Test individual components
        print("  Testing Quick Actions...")
        from quick_actions import get_quick_actions
        qa = get_quick_actions(vault_path)
        prompt = qa.generate_research_summary_prompt()
        assert len(prompt) > 50
        print("  ✓ Quick Actions working")
        
        print("  Testing Persistent Memory...")
        from persistent_memory import get_persistent_memory
        pm = get_persistent_memory(vault_path)
        success = pm.store_concept("Test Concept", "Test description")
        assert success > 0
        print("  ✓ Persistent Memory working")
        
        print("  Testing Vault Intelligence...")
        from vault_intelligence import get_vault_intelligence
        vi = get_vault_intelligence(vault_path)
        health = vi.get_vault_health_report()
        assert "overview" in health
        print("  ✓ Vault Intelligence working")
        
        print("  Testing Proactive Assistant...")
        from proactive_assistant import get_proactive_assistant
        pa = get_proactive_assistant(vault_path, pm, vi)
        suggestions = pa.generate_proactive_suggestions()
        assert isinstance(suggestions, list)
        print("  ✓ Proactive Assistant working")
        
        print("\n🎉 All hybrid features working correctly!")
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(vault_path)

if __name__ == "__main__":
    success = test_hybrid_features()
    if success:
        print("\n✅ Hybrid architecture is ready!")
        print("🚀 Server now has both convenience + unique intelligence")
    else:
        print("\n❌ Tests failed - check implementation")
        sys.exit(1)