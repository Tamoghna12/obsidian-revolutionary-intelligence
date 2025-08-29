#!/usr/bin/env python3
"""
Test script for the new podcast script generation feature
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_podcast_feature():
    """Test the new podcast script generation feature"""
    
    print("🎙️ Testing Podcast Script Generation Feature")
    print("=" * 50)
    
    # Test imports
    try:
        from src.content_creation_engine import get_content_creation_engine, ContentGenerator
        print("✅ Content creation engine imports successfully")
        
        engine = get_content_creation_engine()
        generator = engine["generator"]
        
        print("✅ Content engine components initialized")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test content generation templates
    try:
        templates = generator.templates
        print(f"✅ Content templates loaded: {len(templates)}")
        
        if "podcast_script" in templates:
            print("✅ Podcast script template found")
        else:
            print("❌ Podcast script template missing")
            return False
            
        template_types = list(templates.keys())
        print("   Available templates:")
        for template in template_types:
            print(f"   • {template}")
            
    except Exception as e:
        print(f"❌ Template loading error: {e}")
        return False
    
    # Test podcast script generation
    try:
        print("\n📝 Testing Podcast Script Generation...")
        
        # Test podcast script generation
        podcast_script = generator.generate_podcast_script("The Future of AI", 30)
        print(f"✅ Podcast script generated ({len(podcast_script)} characters)")
        print(f"   Preview: {podcast_script[:200]}...")
        
    except Exception as e:
        print(f"❌ Podcast script generation error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 PODCAST SCRIPT GENERATION TEST COMPLETE!")
    print("\n🚀 New Capability Available:")
    print("   🎧 Podcast script generation from research topics")
    print("\n💡 Usage Example:")
    print("   generate_podcast_script('The Future of Quantum Computing', 'Quantum Computing', 45)")
    
    return True

if __name__ == "__main__":
    success = test_podcast_feature()
    if success:
        print("\n🎊 Podcast script generation feature is working!")
    else:
        print("\n⚠️  Some tests failed.")
        sys.exit(1)