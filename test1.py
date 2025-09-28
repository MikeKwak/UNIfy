#!/usr/bin/env python3
"""
Comprehensive test runner that uses your existing tests + fixes the core issues
"""

import time
import subprocess
import sys
import os
import requests
import json
from pathlib import Path

def run_system_tests():
    """Run all your existing tests plus API endpoint tests."""
    
    print("🚀 UNIfy Comprehensive Test Suite")
    print("=" * 50)
    
    # Test 1: Run your ultra-fast test
    print("\n1️⃣ Running Ultra-Fast ML Pipeline Test")
    print("-" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, "ultra_fast_test.py"
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print("✅ Ultra-fast test PASSED")
            print(result.stdout)
        else:
            print("❌ Ultra-fast test FAILED")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Ultra-fast test TIMED OUT (should be < 1 minute!)")
    except FileNotFoundError:
        print("⚠️ ultra_fast_test.py not found - skipping")
    
    # Test 2: Run your performance test
    print("\n2️⃣ Running Performance Test")
    print("-" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, "quick_test.py"
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Performance test PASSED")
            print(result.stdout)
        else:
            print("❌ Performance test FAILED")  
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Performance test TIMED OUT (should be < 5 minutes!)")
    except FileNotFoundError:
        print("⚠️ quick_test.py not found - skipping")
    
    # Test 3: Test Gemini fallback
    print("\n3️⃣ Running Gemini Fallback Test")
    print("-" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, "test_gemini_fallback.py"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Gemini fallback test PASSED")
            print(result.stdout)
        else:
            print("❌ Gemini fallback test FAILED")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Gemini test TIMED OUT")
    except FileNotFoundError:
        print("⚠️ test_gemini_fallback.py not found - skipping")

def test_api_endpoints():
    """Test your Flask API endpoints with proper error handling."""
    
    print("\n4️⃣ Testing API Endpoints")
    print("-" * 40)
    
    base_url = "http://127.0.0.1:5000"
    
    # Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print("✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Please start with: python app.py")
        return False
    
    # Test cases from your requirements
    test_cases = [
        {
            "name": "ADHD Student",
            "data": {
                "mental_health": "ADHD",
                "physical_health": "None",
                "courses": "Computer Science",
                "gpa": 3.8,
                "severity": "moderate"
            }
        },
        {
            "name": "Engineering Student with Back Pain", 
            "data": {
                "mental_health": "None",
                "physical_health": "chronic back pain",
                "courses": "Mechanical Engineering",
                "gpa": 3.2,
                "severity": "mild"
            }
        },
        {
            "name": "Pre-med with Combined Issues",
            "data": {
                "mental_health": "anxiety and depression", 
                "physical_health": "sleep disorders, headaches",
                "courses": "Pre-medical Biology",
                "gpa": 2.9,
                "severity": "severe"
            }
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        
        # Test verification endpoint (this is what your curl commands use)
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/recommendations/verify",
                json=test_case['data'],
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()
            
            print(f"   ⏱️ Response time: {end_time - start_time:.2f}s")
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('success')}")
                print(f"   🏫 Recommendations: {len(data.get('final_recommendations', []))}")
                print(f"   🔧 Accommodations: {len(data.get('needed_accommodations', []))}")
                success_count += 1
            else:
                print(f"   ❌ Failed with: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    print(f"\n🎯 API Tests: {success_count}/{len(test_cases)} passed")
    return success_count == len(test_cases)

def diagnose_performance_issues():
    """Diagnose why the system is slow."""
    
    print("\n5️⃣ Performance Diagnosis")
    print("-" * 40)
    
    # Check if models are being cached
    print("🔍 Checking for model caching issues...")
    
    model_files = [
        "accommodation_model.h5",
        "university_model.pkl", 
        "label_encoder.pkl",
        "scaler.pkl"
    ]
    
    models_exist = []
    for model_file in model_files:
        if os.path.exists(model_file):
            models_exist.append(model_file)
            print(f"   ✅ Found: {model_file}")
        else:
            print(f"   ❌ Missing: {model_file}")
    
    if len(models_exist) == len(model_files):
        print("✅ All model files exist - caching should work")
    else:
        print("⚠️ Missing model files - will retrain each time")
    
    # Check data files
    print("\n🔍 Checking data files...")
    data_files = [
        "cleaned_student_data.csv",
        "cleaned_university_data.csv", 
        "cleaned_user_input_data.csv"
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            size = os.path.getsize(data_file)
            print(f"   ✅ {data_file}: {size:,} bytes")
        else:
            print(f"   ❌ Missing: {data_file}")

def main():
    """Main test runner."""
    
    start_time = time.time()
    
    # Run all tests
    run_system_tests()
    
    # Test API if server is running
    api_success = test_api_endpoints()
    
    # Diagnose performance 
    diagnose_performance_issues()
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"⏱️ Total test time: {total_time:.2f} seconds")
    
    if api_success:
        print("✅ API endpoints working correctly")
    else:
        print("❌ API endpoints have issues")
    
    print("\n🔧 RECOMMENDATIONS:")
    
    # Check for the main issue from your logs
    if not os.path.exists("accommodation_model.h5"):
        print("🚨 CRITICAL: Models not cached - this causes slow loading!")
        print("   → Run ultra_fast_test.py first to create model files")
    
    print("🚨 MAIN ISSUE: Your Flask app reloads models for each request")
    print("   → Implement model caching in your Flask app")
    print("   → Models should load once at startup, not per request")
    
    print("\n💡 NEXT STEPS:")
    print("1. Run: python3 ultra_fast_test.py  (creates cached models)")
    print("2. Modify your Flask app to load models once at startup")
    print("3. Test API endpoints again")
    print("4. Optional: Set GEMINI_API_KEY for AI enhancement")

if __name__ == "__main__":
    main()