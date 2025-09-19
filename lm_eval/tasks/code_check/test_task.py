#!/usr/bin/env python3
"""
Test script for the Python Code Quality evaluation task.
This script tests the core functionality without running the full evaluation.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils import (
    load_dataset, 
    process_docs, 
    extract_python_code, 
    safe_execute, 
    analyze_code_quality,
    code_quality_score,
    functional_correctness,
    syntax_validity,
    code_style_score
)


def test_dataset_loading():
    """Test dataset loading functionality."""
    print("Testing dataset loading...")
    
    # Test the raw JSON loading first
    import json
    current_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(current_dir, "python_code_quality_dataset.json")
    
    with open(dataset_path, 'r') as f:
        raw_data = json.load(f)
    
    assert len(raw_data) == 20, f"Expected 20 problems, got {len(raw_data)}"
    
    # Check first problem structure
    first_problem = raw_data[0]
    required_keys = ['id', 'problem', 'description', 'test_cases', 'expected_solution']
    for key in required_keys:
        assert key in first_problem, f"Missing key: {key}"
    
    # Test the dataset loading function (if datasets is available)
    try:
        dataset_dict = load_dataset()
        assert "test" in dataset_dict, "Dataset should have 'test' split"
        test_dataset = dataset_dict["test"]
        assert len(test_dataset) == 20, f"Expected 20 problems in test split, got {len(test_dataset)}"
    except ImportError:
        print("  (Skipping datasets integration test - datasets library not available)")
    
    print("✓ Dataset loading works correctly")


def test_code_extraction():
    """Test code extraction from various formats."""
    print("Testing code extraction...")
    
    # Test code block extraction
    text_with_block = """
    Here's the solution:
    ```python
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n-1)
    ```
    """
    
    extracted = extract_python_code(text_with_block)
    assert "def factorial" in extracted, "Failed to extract from code block"
    
    # Test function detection
    text_with_function = """
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    This function checks if a number is prime.
    """
    
    extracted = extract_python_code(text_with_function)
    assert "def is_prime" in extracted, "Failed to extract function"
    
    print("✓ Code extraction works correctly")


def test_safe_execution():
    """Test safe code execution."""
    print("Testing safe code execution...")
    
    # Test valid code
    valid_code = """
def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
"""
    
    test_cases = ["assert factorial(5) == 120", "assert factorial(0) == 1"]
    result = safe_execute(valid_code, test_cases)
    
    assert result['syntax_valid'], "Valid code should have valid syntax"
    assert result['execution_successful'], "Valid code should execute successfully"
    assert result['tests_passed'] == 2, f"Expected 2 tests to pass, got {result['tests_passed']}"
    
    # Test invalid syntax
    invalid_code = "def broken_function(\n    return 'missing colon'"
    result = safe_execute(invalid_code, [])
    assert not result['syntax_valid'], "Invalid code should have invalid syntax"
    
    print("✓ Safe execution works correctly")


def test_quality_analysis():
    """Test code quality analysis."""
    print("Testing code quality analysis...")
    
    # Test high-quality code
    good_code = '''
def calculate_factorial(n):
    """Calculate the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):  # Iterate from 2 to n
        result *= i
    
    return result
'''
    
    quality = analyze_code_quality(good_code)
    assert quality['has_docstring'], "Should detect docstring"
    assert quality['has_comments'], "Should detect comments"
    assert quality['proper_naming'], "Should have proper naming"
    assert quality['has_error_handling'], "Should detect error handling"
    
    print("✓ Quality analysis works correctly")


def test_metrics():
    """Test the custom metrics."""
    print("Testing custom metrics...")
    
    # Sample predictions and references
    predictions = [
        ['''
def factorial(n):
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Negative input")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
'''],
        ['''
def is_palindrome(s):
    cleaned = ''.join(s.lower().split())
    return cleaned == cleaned[::-1]
''']
    ]
    
    references = ["dummy", "dummy"]  # Not used in our implementation
    
    # Test code quality score
    quality_result = code_quality_score(references, predictions)
    assert 'code_quality_score' in quality_result
    assert 0 <= quality_result['code_quality_score'] <= 1
    
    # Test functional correctness
    func_result = functional_correctness(references, predictions)
    assert 'functional_correctness' in func_result
    assert 0 <= func_result['functional_correctness'] <= 1
    
    # Test syntax validity
    syntax_result = syntax_validity(references, predictions)
    assert 'syntax_validity' in syntax_result
    assert 0 <= syntax_result['syntax_validity'] <= 1
    
    # Test code style score
    style_result = code_style_score(references, predictions)
    assert 'code_style_score' in style_result
    assert 0 <= style_result['code_style_score'] <= 1
    
    print("✓ Custom metrics work correctly")


def main():
    """Run all tests."""
    print("Running Python Code Quality Task Tests")
    print("=" * 50)
    
    try:
        test_dataset_loading()
        test_code_extraction()
        test_safe_execution()
        test_quality_analysis()
        test_metrics()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! The task is ready to use.")
        print("\nTo run the evaluation:")
        print("lm_eval --model hf --model_args pretrained=your_model --tasks python_code_quality")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()