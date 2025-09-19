#!/usr/bin/env python3
"""
Example usage of the Python Code Quality evaluation task.
This script demonstrates how to use the task components independently.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils import (
    extract_python_code,
    safe_execute,
    analyze_code_quality,
    code_quality_score,
    functional_correctness,
    syntax_validity,
    code_style_score
)
import json


def demonstrate_evaluation():
    """Demonstrate the evaluation process with sample code."""
    print("Python Code Quality Evaluation - Example Usage")
    print("=" * 60)
    
    # Load a sample problem
    current_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(current_dir, "python_code_quality_dataset.json")
    
    with open(dataset_path, 'r') as f:
        problems = json.load(f)
    
    # Use the first problem (factorial)
    problem = problems[0]
    print(f"Problem: {problem['problem']}")
    print(f"Description: {problem['description']}")
    print(f"Test cases: {problem['test_cases']}")
    print()
    
    # Sample generated code responses (simulating different LLM outputs)
    sample_responses = [
        # Good quality code
        '''
```python
def factorial(n):
    """Calculate the factorial of a non-negative integer.
    
    Args:
        n (int): Non-negative integer
        
    Returns:
        int: Factorial of n
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):  # Calculate factorial iteratively
        result *= i
    
    return result
```
        ''',
        
        # Medium quality code
        '''
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
        ''',
        
        # Poor quality code
        '''
def f(x):
return x*f(x-1) if x>1 else 1
        ''',
        
        # Broken code
        '''
def factorial(n
    if n <= 1:
        return 1
    return n * factorial(n-1
        '''
    ]
    
    print("Evaluating different code samples:")
    print("-" * 40)
    
    for i, response in enumerate(sample_responses, 1):
        print(f"\nSample {i}:")
        print("Code:")
        print(response.strip())
        
        # Extract code
        extracted_code = extract_python_code(response)
        print(f"\nExtracted code: {repr(extracted_code[:50])}...")
        
        # Test execution
        execution_result = safe_execute(extracted_code, problem['test_cases'])
        print(f"Syntax valid: {execution_result['syntax_valid']}")
        print(f"Execution successful: {execution_result['execution_successful']}")
        print(f"Tests passed: {execution_result['tests_passed']}/{execution_result['total_tests']}")
        
        if execution_result['error_message']:
            print(f"Error: {execution_result['error_message']}")
        
        # Analyze quality
        quality_metrics = analyze_code_quality(extracted_code)
        print(f"Has docstring: {quality_metrics['has_docstring']}")
        print(f"Has comments: {quality_metrics['has_comments']}")
        print(f"Proper naming: {quality_metrics['proper_naming']}")
        print(f"Complexity score: {quality_metrics['complexity_score']}")
        print(f"Has error handling: {quality_metrics['has_error_handling']}")
        print(f"Follows PEP8 basics: {quality_metrics['follows_pep8_basics']}")
        
        print("-" * 40)
    
    # Demonstrate metric calculation
    print("\nCalculating aggregate metrics:")
    predictions = [[response] for response in sample_responses]
    references = ["dummy"] * len(sample_responses)  # Not used in our implementation
    
    # Calculate all metrics
    quality_result = code_quality_score(references, predictions)
    func_result = functional_correctness(references, predictions)
    syntax_result = syntax_validity(references, predictions)
    style_result = code_style_score(references, predictions)
    
    print(f"Overall Code Quality Score: {quality_result['code_quality_score']:.3f}")
    print(f"Functional Correctness: {func_result['functional_correctness']:.3f}")
    print(f"Syntax Validity: {syntax_result['syntax_validity']:.3f}")
    print(f"Code Style Score: {style_result['code_style_score']:.3f}")
    
    print("\n" + "=" * 60)
    print("Evaluation complete!")
    print("\nTo run the full evaluation with lm-eval:")
    print("lm_eval --model hf --model_args pretrained=your_model --tasks python_code_quality")


if __name__ == "__main__":
    demonstrate_evaluation()