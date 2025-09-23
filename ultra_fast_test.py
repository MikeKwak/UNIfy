"""
Ultra-fast test to verify the ML pipeline works in under 1 minute.
This is for testing the basic functionality only.
"""

import time
import os
from ml_pipeline import UNIfyMLPipeline

def ultra_fast_test():
    """Ultra-fast test with minimal data and models."""
    print("⚡ Ultra-Fast Test (Target: < 1 minute)")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # Initialize pipeline
        print("1. Initializing pipeline...")
        pipeline = UNIfyMLPipeline()
        
        # Load data
        print("2. Loading data...")
        pipeline.load_data()
        
        # Preprocess data
        print("3. Preprocessing data...")
        pipeline.preprocess_student_data()
        pipeline.preprocess_user_input()
        
        # Create minimal training data
        print("4. Creating minimal training data...")
        pipeline.create_training_data()
        
        # Encode features
        print("5. Encoding features...")
        pipeline.encode_categorical_features()
        
        # Build and train accommodation predictor (simplified)
        print("6. Building and training accommodation predictor...")
        pipeline.build_accommodation_predictor()
        
        # Build university recommender (simplified)
        print("7. Building university recommender...")
        pipeline.build_university_recommender()
        
        # Save models
        print("8. Saving models...")
        pipeline.save_models()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print("\n" + "=" * 50)
        print("✅ ULTRA-FAST TEST COMPLETED!")
        print(f"⏱️  Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        
        if total_time < 60:  # 1 minute
            print("🎉 Excellent! Pipeline runs in under 1 minute.")
        elif total_time < 120:  # 2 minutes
            print("👍 Good! Pipeline runs in under 2 minutes.")
        else:
            print("⚠️  Pipeline still taking longer than expected.")
        
        # Test a quick recommendation
        print("\n🧪 Testing quick recommendation...")
        test_profile = {
            'mental_health': 'ADHD',
            'physical_health': 'None',
            'courses': 'Computer Science',
            'gpa': 3.8,
            'severity': 'moderate'
        }
        
        recommendations = pipeline.recommend_universities(test_profile)
        if recommendations:
            print(f"✅ Got {len(recommendations)} recommendations!")
            for i, (uni, score) in enumerate(recommendations[:3], 1):
                print(f"  {i}. {uni} (Score: {score:.3f})")
        else:
            print("❌ No recommendations generated")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n❌ Test failed after {total_time:.2f} seconds: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    ultra_fast_test()



