"""
Test script to demonstrate Gemini AI fallback functionality
"""

from ml_pipeline import get_recommendations
from gemini_recommender import get_gemini_recommendations


def test_gemini_fallback():
    """Test various scenarios to demonstrate Gemini AI fallback."""

    print("🧪 Testing Gemini AI Fallback System")
    print("=" * 50)

    # Test 1: Normal profile
    print("\n📊 Test 1: Normal Profile (ML Pipeline)")
    normal_profile = {
        'mental_health': 'ADHD',
        'physical_health': 'None',
        'courses': 'Computer Science',
        'gpa': 3.8,
        'severity': 'moderate'
    }

    result = get_recommendations(normal_profile)
    print(f"Source: {result.get('source', 'unknown')}")
    print(f"Success: {result['success']}")
    print(f"Recommendations: {len(result.get('recommendations', []))}")

    # Test 2: Edge case profile
    print("\n📊 Test 2: Edge Case Profile")
    edge_profile = {
        'mental_health': 'Autism',
        'physical_health': 'Mobility',
        'courses': 'Fine Arts',
        'gpa': 2.5,
        'severity': 'severe'
    }

    result = get_recommendations(edge_profile)
    print(f"Source: {result.get('source', 'unknown')}")
    print(f"Success: {result['success']}")
    print(f"Recommendations: {len(result.get('recommendations', []))}")

    # Test 3: Direct Gemini AI test (fallback mode)
    print("\n📊 Test 3: Direct Gemini AI Fallback")
    result = get_gemini_recommendations(normal_profile)
    print(f"Source: {result['source']}")
    print(f"Success: {result['success']}")
    print(f"Accommodations: {result['needed_accommodations']}")
    print(f"Universities: {len(result['recommendations'])}")

    # Show sample recommendations
    for i, uni in enumerate(result['recommendations'][:3], 1):
        print(f"  {i}. {uni['name']} (Score: {uni['score']})")
        print(f"     Reason: {uni['reason']}")

    print("\n Gemini AI Fallback System Test Complete")


def test_empty_scenario():
    """Test what happens with completely empty data."""
    print("\n📊 Test 4: Empty Data Scenario")

    empty_profile = {
        'mental_health': 'UnknownCondition',
        'physical_health': 'VeryRareDisability',
        'courses': 'NicheProgram',
        'gpa': 1.0,
        'severity': 'extreme'
    }

    result = get_recommendations(empty_profile)
    print(f"Source: {result.get('source', 'unknown')}")
    print(f"Success: {result['success']}")
    print(f"Recommendations: {len(result.get('recommendations', []))}")

    if result.get('fallback_reason'):
        print(f"Fallback reason: {result['fallback_reason']}")


if __name__ == "__main__":
    test_gemini_fallback()
    test_empty_scenario()
