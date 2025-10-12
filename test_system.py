"""
UNIfy System Test Script
Test the recommendation system and demonstrate its functionality.
"""

import os
import sys
import json
from typing import Dict, List


def test_ml_pipeline():
    """Test the ML pipeline functionality."""
    print("🧪 Testing ML Pipeline...")

    try:
        from ml_pipeline import UNIfyMLPipeline

        # Initialize pipeline
        pipeline = UNIfyMLPipeline()
        print("Pipeline initialized successfully")

        # Test data loading
        pipeline.load_data()
        print("Data loaded successfully")

        # Test preprocessing
        pipeline.preprocess_student_data()
        pipeline.preprocess_user_input()
        print("SData preprocessing completed")

        # Test training data creation
        pipeline.create_training_data()
        print("Training data created")

        # Test feature encoding
        pipeline.encode_categorical_features()
        print("Feature encoding completed")

        print("\n🎉 ML Pipeline test completed successfully!")
        return True

    except Exception as e:
        print(f"ML Pipeline test failed: {e}")
        return False


def test_recommendation_system():
    """Test the recommendation system with sample data."""
    print("\n🧪 Testing Recommendation System...")

    try:
        from ml_pipeline import UNIfyMLPipeline

        # Initialize pipeline
        pipeline = UNIfyMLPipeline()

        # Load data and build models
        pipeline.load_data()
        pipeline.preprocess_student_data()
        pipeline.preprocess_user_input()
        pipeline.create_training_data()
        pipeline.encode_categorical_features()

        # Test student profiles
        test_profiles = [
            {
                'mental_health': 'ADHD',
                'physical_health': 'None',
                'courses': 'Computer Science',
                'gpa': 3.8,
                'severity': 'moderate'
            },
            {
                'mental_health': 'None',
                'physical_health': 'Mobility',
                'courses': 'Mathematics',
                'gpa': 3.5,
                'severity': 'mild'
            },
            {
                'mental_health': 'Autism',
                'physical_health': 'Hearing',
                'courses': 'Arts',
                'gpa': 3.2,
                'severity': 'severe'
            }
        ]

        print("\n Testing with different student profiles:")

        for i, profile in enumerate(test_profiles, 1):
            print(f"\n--- Profile {i} ---")
            print(f"Mental Health: {profile['mental_health']}")
            print(f"Physical Health: {profile['physical_health']}")
            print(f"Courses: {profile['courses']}")
            print(f"GPA: {profile['gpa']}")
            print(f"Severity: {profile['severity']}")

            # Get recommendations
            recommendations = pipeline.recommend_universities(profile)

            if recommendations:
                print(f"Top 3 University Recommendations:")
                for j, (uni, score) in enumerate(recommendations[:3], 1):
                    print(f"  {j}. {uni} (Score: {score:.3f})")
            else:
                print("  No recommendations available")

        print("\n Recommendation System test completed successfully!")
        return True

    except Exception as e:
        print(f"Recommendation System test failed: {e}")
        return False


def test_api_function():
    """Test the API function for frontend integration."""
    print("\nTesting API Function...")

    try:
        from ml_pipeline import get_recommendations

        # Test student profiles
        test_profiles = [
            {
                'mental_health': 'ADHD',
                'physical_health': 'None',
                'courses': 'Computer Science',
                'gpa': 3.8,
                'severity': 'moderate'
            },
            {
                'mental_health': 'None',
                'physical_health': 'Mobility',
                'courses': 'Mathematics',
                'gpa': 3.5,
                'severity': 'mild'
            }
        ]

        print("\Testing API function with different profiles:")

        for i, profile in enumerate(test_profiles, 1):
            print(f"\n--- Profile {i} ---")
            print(f"Input: {profile}")

            # Get recommendations via API
            result = get_recommendations(profile)

            if result['success']:
                print("PI call successful")
                print(
                    f"Needed accommodations: {result['needed_accommodations']}")
                print(
                    f"Found {len(result['recommendations'])} university recommendations")

                # Show top recommendations
                for j, uni in enumerate(result['recommendations'][:3], 1):
                    print(f"  {j}. {uni['name']} (Score: {uni['score']})")
            else:
                print(f"API call failed: {result['error']}")

        print("\nAPI Function test completed successfully!")
        return True

    except Exception as e:
        print(f"API Function test failed: {e}")
        return False


def test_data_quality():
    """Test the quality and structure of the cleaned CSV data."""
    print("\nTesting Data Quality...")

    try:
        import pandas as pd

        # Test student info data
        if os.path.exists('data/clean/clean_student_info.csv'):
            student_df = pd.read_csv('data/clean/clean_student_info.csv')
            print(
                f"Student info data: {student_df.shape[0]} rows, {student_df.shape[1]} columns")

            # Check for missing values
            missing_data = student_df.isnull().sum()
            if missing_data.sum() > 0:
                print(
                    f"Missing data found: {missing_data.sum()} total missing values")
            else:
                print("No missing data in student info")

        # Test user input data
        if os.path.exists('data/clean/clean_user_input.csv'):
            user_df = pd.read_csv('data/clean/clean_user_input.csv')
            print(
                f"User input data: {user_df.shape[0]} rows, {user_df.shape[1]} columns")

            # Check for missing values
            missing_data = user_df.isnull().sum()
            if missing_data.sum() > 0:
                print(
                    f"Missing data found: {missing_data.sum()} total missing values")
            else:
                print("No missing data in user input")

        # Test university data
        if os.path.exists('data/clean/clean_uni_info.csv'):
            try:
                uni_df = pd.read_csv('data/clean/clean_uni_info.csv')
                print(
                    f"University data: {uni_df.shape[0]} rows, {uni_df.shape[1]} columns")
            except Exception as e:
                print(
                    f"University data file exists but couldn't be read: {e}")
        else:
            print("University data file not found (will use sample data)")

        print("\nData Quality test completed successfully!")
        return True

    except Exception as e:
        print(f"Data Quality test failed: {e}")
        return False


def run_demo():
    """Run a complete demonstration of the UNIfy system."""
    print("UNIfy System Demonstration")
    print("=" * 50)

    # Run all tests
    tests = [
        ("Data Quality", test_data_quality),
        ("ML Pipeline", test_ml_pipeline),
        ("Recommendation System", test_recommendation_system),
        ("API Function", test_api_function)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"{test_name} test crashed: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! UNIfy ML system is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python ml_pipeline.py' to train the models")
        print("2. Use the 'get_recommendations()' function in your frontend")
        print("3. Models will be saved to the 'models/' directory")
        print("\nFrontend Integration:")
        print("- Import: from ml_pipeline import get_recommendations")
        print("- Call: result = get_recommendations(student_profile)")
        print(
            "- Result format: {'success': bool, 'recommendations': [...], 'needed_accommodations': [...]}")
    else:
        print("Some tests failed. Check the output above for details.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that your CSV files are in the data/clean/ directory")
        print("3. Verify Python version (3.8+ required)")


if __name__ == "__main__":
    run_demo()
