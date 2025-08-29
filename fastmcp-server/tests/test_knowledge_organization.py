#!/usr/bin/env python3
"""
Test suite for Knowledge Organization and Productivity System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.knowledge_organizer import get_productivity_system
import tempfile
import shutil
from src.datetime import datetime

def test_knowledge_organization_system():
    """Test all knowledge organization and productivity features"""
    
    print("🎯 Testing Knowledge Organization and Productivity System")
    print("=" * 60)
    
    # Create temporary vault directory for testing
    temp_vault = tempfile.mkdtemp()
    print(f"📁 Using temporary vault: {temp_vault}")
    
    try:
        # Create some test notes
        test_notes = {
            "Research/quantum_computing.md": """# Quantum Computing Research

## Research Question
How can we improve quantum error correction?

## Methodology
- Literature review of current approaches
- Simulation of error correction algorithms
- Analysis of results

## Tasks
- [x] Review recent papers
- [ ] Implement basic algorithm
- [ ] Run simulations
- [ ] Analyze results

## Tags: #research #quantum #computing
""",
            "Projects/ai_ethics.md": """# AI Ethics Project

## Project Goals
1. Define ethical guidelines for AI development
2. Create training materials for developers
3. Establish review process

## Milestones
- [ ] Complete literature review
- [ ] Draft guidelines document
- [ ] Review with stakeholders
- [ ] Publish final version

## Related Work
- See also [[Research/ai_bias]]
""",
            "Daily/daily_note_2024-01-15.md": """# Daily Note - 2024-01-15

## Today's Focus
- Work on quantum computing research
- Review AI ethics project

## Tasks
- [x] Read three research papers
- [ ] Write summary of findings
- [ ] Update project timeline

## Reflection
Made good progress on the literature review.
""",
            "Ideas/blockchain_applications.md": """# Blockchain Applications

## Ideas for blockchain use cases
- Supply chain tracking
- Digital identity verification
- Smart contracts for legal documents

## Research Needed
1. Current adoption rates
2. Technical limitations
3. Regulatory considerations

## Next Steps
- [ ] Research supply chain case studies
- [ ] Contact industry experts
"""
        }
        
        # Create test notes
        for note_path, content in test_notes.items():
            full_path = os.path.join(temp_vault, note_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print("✅ Created test notes")
        
        # Get productivity system components
        components = get_productivity_system(temp_vault)
        knowledge_organizer = components["knowledge_organizer"]
        progress_tracker = components["progress_tracker"]
        content_repurposer = components["content_repurposer"]
        
        print("✅ Productivity system components loaded successfully")
        
        # Test 1: Knowledge categorization
        print("\n📂 Testing Knowledge Categorization...")
        categories = knowledge_organizer.categorize_notes_by_content()
        print(f"✅ Notes categorized into {len([cat for cat in categories.values() if cat])} categories")
        for category, notes in categories.items():
            if notes:
                print(f"   - {category}: {len(notes)} notes")
        
        # Test 2: Tag hierarchy
        print("\n🏷️  Testing Tag Hierarchy Creation...")
        tag_hierarchy = knowledge_organizer.create_tag_hierarchy()
        print(f"✅ Tag hierarchy created with {len(tag_hierarchy)} unique tags")
        if tag_hierarchy:
            top_tag = max(tag_hierarchy.items(), key=lambda x: len(x[1]))
            print(f"   - Most used tag: #{top_tag[0]} ({len(top_tag[1])} notes)")
        
        # Test 3: Knowledge map generation
        print("\n🗺️  Testing Knowledge Map Generation...")
        knowledge_map = knowledge_organizer.generate_knowledge_map()
        print("✅ Knowledge map generated")
        print(f"   - Length: {len(knowledge_map)} characters")
        
        # Test 4: Progress tracking
        print("\n📊 Testing Progress Tracking...")
        tasks = progress_tracker.extract_tasks_from_notes()
        print(f"✅ Extracted {len(tasks)} tasks from notes")
        
        completed_tasks = sum(1 for task in tasks if task["completed"])
        total_tasks = len(tasks)
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        print(f"   - Completed: {completed_tasks}/{total_tasks} ({completion_rate:.1f}%)")
        
        # Test 5: Progress report generation
        print("\n📈 Testing Progress Report Generation...")
        progress_report = progress_tracker.generate_progress_report()
        print("✅ Progress report generated")
        print(f"   - Length: {len(progress_report)} characters")
        
        # Test 6: Content repurposing
        print("\n🔄 Testing Content Repurposing...")
        blog_post = content_repurposer.convert_note_to_blog_post("Research/quantum_computing.md")
        print("✅ Note converted to blog post format")
        print(f"   - Length: {len(blog_post)} characters")
        
        summary = content_repurposer.create_summary_from_note("Projects/ai_ethics.md")
        print("✅ Note summarized")
        print(f"   - Length: {len(summary)} characters")
        
        print("\n" + "=" * 60)
        print("🎉 ALL KNOWLEDGE ORGANIZATION TESTS PASSED!")
        print("\n🚀 New Capabilities Available:")
        print("   📂 Automatic knowledge categorization")
        print("   🏷️  Tag hierarchy creation")
        print("   🗺️  Visual knowledge mapping")
        print("   📊 Progress tracking and reporting")
        print("   🔄 Content repurposing")
        print("\n💡 Usage Examples:")
        print("   1. organize_knowledge_base()")
        print("   2. generate_progress_report()")
        print("   3. create_knowledge_map()")
        print("   4. convert_note_to_blog_post('Research/quantum_computing.md')")
        print("   5. create_summary_from_note('Projects/ai_ethics.md')")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_vault, ignore_errors=True)
    
    return True

if __name__ == "__main__":
    success = test_knowledge_organization_system()
    sys.exit(0 if success else 1)