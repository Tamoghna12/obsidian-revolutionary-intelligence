#!/usr/bin/env python3
"""
Test suite for Productivity Enhancer features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.productivity_enhancer import get_productivity_enhancer
import tempfile
import shutil
from src.datetime import datetime

def test_productivity_enhancer():
    """Test all productivity enhancer features"""
    
    print("🎯 Testing Productivity Enhancer Features")
    print("=" * 50)
    
    # Create temporary vault directory for testing
    temp_vault = tempfile.mkdtemp()
    print(f"📁 Using temporary vault: {temp_vault}")
    
    try:
        # Get productivity enhancer components
        components = get_productivity_enhancer(temp_vault)
        workflow_automation = components["workflow_automation"]
        goal_tracker = components["goal_tracker"]
        focus_manager = components["focus_session_manager"]
        resource_optimizer = components["resource_optimizer"]
        
        print("✅ Productivity enhancer components loaded successfully")
        
        # Test 1: Project Workflow Creation
        print("\n📝 Testing Project Workflow Creation...")
        workflow_result = workflow_automation.create_project_workflow(
            "AI Research Project", 
            "research"
        )
        print(f"✅ Workflow created: {workflow_result['message']}")
        
        # Test 2: Project Progress Tracking
        print("\n📊 Testing Project Progress Tracking...")
        progress_result = workflow_automation.track_project_progress("AI Research Project")
        print(f"✅ Progress tracked: {progress_result['status']} ({progress_result['completion_rate']}%)")
        
        # Test 3: OKR Creation
        print("\n🎯 Testing OKR Creation...")
        objectives = [
            {
                "name": "Complete AI Research Paper",
                "description": "Publish findings on neural network optimization",
                "priority": "high",
                "key_results": [
                    {"name": "Literature review complete", "target": 100, "current": 75, "unit": "%"},
                    {"name": "Experiments conducted", "target": 5, "current": 3, "unit": "experiments"},
                    {"name": "Draft written", "target": 1, "current": 0, "unit": "draft"}
                ]
            }
        ]
        okr_result = goal_tracker.create_objectives_and_key_results(
            "Q3 2024", 
            objectives
        )
        print(f"✅ OKRs created: {okr_result['message']}")
        
        # Test 4: Focus Session Management
        print("\n⚡ Testing Focus Session Management...")
        session_result = focus_manager.start_focus_session(
            "Neural Network Research", 
            25, 
            "home_office"
        )
        session_id = session_result['session']['session_id']
        print(f"✅ Focus session started: {session_id}")
        
        # End session
        end_result = focus_manager.end_focus_session(
            session_id, 
            ["Reviewed 3 papers", "Designed experiment framework"]
        )
        print(f"✅ Focus session ended: {end_result['message']}")
        
        # Test 5: Productivity Pattern Analysis
        print("\n📈 Testing Productivity Pattern Analysis...")
        # Create mock notes data for testing
        mock_notes = [
            {
                "created": datetime.now().isoformat(),
                "tags": ["research", "ai", "neural-networks"],
                "template": "research"
            },
            {
                "created": datetime.now().isoformat(),
                "tags": ["writing", "blog"],
                "template": "blog-post"
            }
        ]
        
        patterns = resource_optimizer.analyze_productivity_patterns(mock_notes)
        suggestions = resource_optimizer.suggest_optimal_schedule({})
        
        print(f"✅ Productivity patterns analyzed")
        print(f"   Peak hour: {patterns['peak_productivity_hour']['hour']}:00")
        print(f"   Peak day: {patterns['peak_productivity_day']['day']}")
        print(f"✅ Schedule suggestions generated")
        
        print("\n" + "=" * 50)
        print("🎉 ALL PRODUCTIVITY ENHANCER TESTS PASSED!")
        print("\n🚀 New Capabilities Available:")
        print("   📋 Project workflow automation")
        print("   🎯 Objectives and Key Results (OKRs)")
        print("   ⚡ Deep work focus session tracking")
        print("   📊 Productivity pattern analysis")
        print("   🕐 Schedule optimization suggestions")
        print("\n💡 Usage Examples:")
        print("   1. create_project_workflow('My Research Project', 'research')")
        print("   2. create_objectives_and_key_results('Q3 2024', objectives)")
        print("   3. start_focus_session('Deep Learning Research', 30)")
        print("   4. get_productivity_optimization_suggestions()")
        print("   5. track_project_progress('My Research Project')")
        
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
    success = test_productivity_enhancer()
    sys.exit(0 if success else 1)