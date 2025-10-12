"""
verify the performance fix for the ML pipeline

"""

import time
import os
from ml_pipeline import UNIfyMLPipeline


def quick_performance_test():
    """Test the pipeline performance with the new optimizations."""
    print("Quick Performance Test")
    print("=" * 40)

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

        # Create training data (this was the bottleneck)
        print("4. Creating training data...")
        pipeline.create_training_data()

        # Encode features
        print("5. Encoding features...")
        pipeline.encode_categorical_features()

        # Build and train accommodation predictor
        print("6. Building and training accommodation predictor...")
        pipeline.build_accommodation_predictor()

        # Build university recommender
        print("7. Building university recommender...")
        pipeline.build_university_recommender()

        # Save models
        print("8. Saving models...")
        pipeline.save_models()

        end_time = time.time()
        total_time = end_time - start_time

        print("\n" + "=" * 40)
        print("PERFORMANCE TEST COMPLETED!")
        print(
            f"Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")

        if total_time < 300:  # 5 minutes
            print("Excellent! Pipeline runs in under 5 minutes.")
        elif total_time < 600:  # 10 minutes
            print("Good! Pipeline runs in under 10 minutes.")
        else:
            print("Pipeline still taking longer than expected.")

        return True

    except Exception as e:
        end_time = time.time()
        total_time = end_time - start_time

        print(f"\nTest failed after {total_time:.2f} seconds: {e}")
        return False


if __name__ == "__main__":
    quick_performance_test()
