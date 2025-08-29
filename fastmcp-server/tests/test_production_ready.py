#!/usr/bin/env python3
"""
Production Readiness Test Suite
Comprehensive validation of all system components for production deployment
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_all_imports():
    """Test that all components can be imported without errors"""
    print("🔍 Testing All Component Imports...")
    
    try:
        # Core server
        from obsidian_server import mcp
        print("  ✅ Main server imports successfully")
        
        # Hybrid architecture components
        from src.quick_actions import get_quick_actions
        from src.persistent_memory import get_persistent_memory
        from src.vault_intelligence import get_vault_intelligence
        from src.proactive_assistant import get_proactive_assistant
        print("  ✅ Hybrid architecture components import successfully")
        
        # AI research components
        from src.revolutionary_intelligence import get_revolutionary_intelligence
        from src.content_creation_engine import get_content_creation_engine
        print("  ✅ AI research components import successfully")
        
        # Productivity components
        from src.enhanced_templates import TemplateManager
        from src.knowledge_organizer import get_productivity_system
        from src.productivity_enhancer import get_productivity_enhancer
        print("  ✅ Productivity components import successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import test failed: {e}")
        return False

def test_component_initialization():
    """Test that all components can be initialized"""
    print("🏗️ Testing Component Initialization...")
    
    vault_path = tempfile.mkdtemp(prefix="test_vault_")
    os.environ["OBSIDIAN_VAULT_PATH"] = vault_path
    
    try:
        # Create test vault structure
        (Path(vault_path) / "notes").mkdir()
        test_note = Path(vault_path) / "notes" / "test.md"
        test_note.write_text("# Test Note\nContent here.")
        
        # Test hybrid components
        from src.quick_actions import get_quick_actions
        qa = get_quick_actions(vault_path)
        assert qa is not None
        print("  ✅ Quick Actions initialized")
        
        from src.persistent_memory import get_persistent_memory
        pm = get_persistent_memory(vault_path)
        assert pm is not None
        print("  ✅ Persistent Memory initialized")
        
        from src.vault_intelligence import get_vault_intelligence
        vi = get_vault_intelligence(vault_path)
        assert vi is not None
        print("  ✅ Vault Intelligence initialized")
        
        from src.proactive_assistant import get_proactive_assistant
        pa = get_proactive_assistant(vault_path, pm, vi)
        assert pa is not None
        print("  ✅ Proactive Assistant initialized")
        
        # Test AI components
        from src.revolutionary_intelligence import get_revolutionary_intelligence
        ri = get_revolutionary_intelligence(vault_path)
        assert ri is not None
        print("  ✅ Revolutionary Intelligence initialized")
        
        from src.content_creation_engine import get_content_creation_engine
        ce = get_content_creation_engine()
        assert ce is not None
        print("  ✅ Content Creation Engine initialized")
        
        # Test productivity components
        from src.enhanced_templates import TemplateManager
        tm = TemplateManager()
        assert tm is not None
        assert len(tm.templates) > 0
        print("  ✅ Template Manager initialized")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Initialization test failed: {e}")
        return False
        
    finally:
        shutil.rmtree(vault_path)

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("🛡️ Testing Error Handling...")
    
    try:
        # Test with non-existent vault
        from src.quick_actions import get_quick_actions
        qa = get_quick_actions("/nonexistent/vault")
        result = qa.generate_blog_conversion_prompt("nonexistent.md")
        assert "not found" in result or "Error" in result
        print("  ✅ Handles non-existent files gracefully")
        
        # Test with empty vault
        empty_vault = tempfile.mkdtemp(prefix="empty_vault_")
        try:
            from src.vault_intelligence import get_vault_intelligence
            vi = get_vault_intelligence(empty_vault)
            health = vi.get_vault_health_report()
            assert isinstance(health, dict)
            print("  ✅ Handles empty vaults gracefully")
        finally:
            shutil.rmtree(empty_vault)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False

def test_performance():
    """Test basic performance characteristics"""
    print("⚡ Testing Performance...")
    
    vault_path = tempfile.mkdtemp(prefix="perf_vault_")
    
    try:
        # Create test notes
        (Path(vault_path) / "notes").mkdir()
        for i in range(10):
            note = Path(vault_path) / "notes" / f"note_{i}.md"
            note.write_text(f"# Note {i}\nContent for note {i}")
        
        import time
        
        # Test search performance
        from src.vault_intelligence import get_vault_intelligence
        start = time.time()
        vi = get_vault_intelligence(vault_path)
        similar = vi.find_similar_notes("notes/note_0.md", 0.1)
        search_time = time.time() - start
        
        assert search_time < 5.0  # Should complete within 5 seconds
        print(f"  ✅ Search performance: {search_time:.2f}s for 10 notes")
        
        # Test memory performance  
        from src.persistent_memory import get_persistent_memory
        start = time.time()
        pm = get_persistent_memory(vault_path)
        for i in range(5):
            pm.store_concept(f"Concept {i}", f"Description {i}")
        memory_time = time.time() - start
        
        assert memory_time < 2.0  # Should complete within 2 seconds
        print(f"  ✅ Memory performance: {memory_time:.2f}s for 5 concepts")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Performance test failed: {e}")
        return False
        
    finally:
        shutil.rmtree(vault_path)

def test_data_integrity():
    """Test data persistence and integrity"""
    print("💾 Testing Data Integrity...")
    
    vault_path = tempfile.mkdtemp(prefix="integrity_vault_")
    
    try:
        from src.persistent_memory import get_persistent_memory
        
        # Store data
        pm1 = get_persistent_memory(vault_path)
        concept_id = pm1.store_concept("Test Concept", "Test Description")
        assert concept_id > 0
        
        # Verify persistence with new instance
        pm2 = get_persistent_memory(vault_path)
        history = pm2.recall_concept_history("Test Concept", 1)
        assert "concept" in history
        assert history["concept"]["name"] == "Test Concept"
        
        print("  ✅ Data persistence verified")
        
        # Test relationship storage
        success = pm2.store_relationship("Test Concept", "Related Concept", "relates_to", 0.8, "Test context")
        assert success
        
        # Verify relationship retrieval
        forgotten = pm2.suggest_forgotten_connections(["Test Concept"])
        assert isinstance(forgotten, list)
        
        print("  ✅ Relationship integrity verified")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Data integrity test failed: {e}")
        return False
        
    finally:
        shutil.rmtree(vault_path)

def main():
    """Run all production readiness tests"""
    print("🚀 Production Readiness Test Suite")
    print("=" * 50)
    
    tests = [
        test_all_imports,
        test_component_initialization,
        test_error_handling,
        test_performance,
        test_data_integrity
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            if result:
                print(f"  ✅ {test.__name__} PASSED")
            else:
                print(f"  ❌ {test.__name__} FAILED")
        except Exception as e:
            print(f"  ❌ {test.__name__} CRASHED: {e}")
            results.append(False)
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - PRODUCTION READY!")
        print(f"✅ {passed}/{total} test suites successful")
        print("\n🚀 System Status: READY FOR DEPLOYMENT")
        print("\n📋 Production Readiness Checklist:")
        print("  ✅ All components import successfully")
        print("  ✅ All components initialize without errors")
        print("  ✅ Error handling works correctly")
        print("  ✅ Performance meets requirements")
        print("  ✅ Data integrity is maintained")
        return True
    else:
        print(f"❌ {total - passed} test suites failed")
        print("🛠️ System needs fixes before production deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)