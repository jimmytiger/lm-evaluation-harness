#!/usr/bin/env python3
"""
Test script to validate the Python coding evaluation framework.
"""

import json
import yaml
import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
os.chdir(SCRIPT_DIR)

def test_jsonl_format():
    """Test that problems.jsonl is properly formatted."""
    print("Testing JSONL format...")
    
    categories = {
        'code_completion': 0,
        'code_repair': 0, 
        'code_translation': 0,
        'docstring_generation': 0,
        'function_generation': 0
    }
    
    with open('problems.jsonl', 'r') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            try:
                data = json.loads(line)
                category = data.get('category')
                if category in categories:
                    categories[category] += 1
                else:
                    print(f"  ❌ Line {i}: Unknown category '{category}'")
                    return False
            except json.JSONDecodeError as e:
                print(f"  ❌ Line {i}: Invalid JSON - {e}")
                return False
    
    # Check we have 5 problems per category
    for cat, count in categories.items():
        if count != 5:
            print(f"  ❌ Category '{cat}': Expected 5 problems, got {count}")
            return False
    
    print(f"  ✅ All 25 problems loaded correctly (5 per category)")
    return True

def test_yaml_configs():
    """Test that all YAML configs are valid."""
    print("Testing YAML configurations...")
    
    config_files = [
        'code_completion.yaml',
        'code_repair.yaml', 
        'code_translation.yaml',
        'docstring_generation.yaml',
        'function_generation.yaml',
        'python_coding_suite.yaml'
    ]
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Check for basic YAML structure and required fields
            if 'group:' in content:
                # Group config - different requirements
                required_patterns = ['group:', 'task:']
            else:
                # Individual task config
                required_patterns = [
                    'task:',
                    'output_type:',
                    'doc_to_text:',
                    'metric_list:',
                    'generation_kwargs:'
                ]
            
            missing_fields = []
            for pattern in required_patterns:
                if pattern not in content:
                    missing_fields.append(pattern.rstrip(':'))
            
            if missing_fields:
                print(f"  ❌ {config_file}: Missing required fields: {missing_fields}")
                return False
            
            # Check for proper !function syntax
            if '!function' in content:
                import re
                function_refs = re.findall(r'!function\s+(\S+)', content)
                for func_ref in function_refs:
                    if not func_ref.startswith('utils.'):
                        print(f"  ❌ {config_file}: Invalid function reference: {func_ref}")
                        return False
            
            print(f"  ✅ {config_file}: Valid configuration")
            
        except Exception as e:
            print(f"  ❌ {config_file}: Error reading - {e}")
            return False
    
    return True

def test_custom_metrics():
    """Test that custom metrics work correctly."""
    print("Testing custom metrics...")
    
    # Import utils from the current directory
    import utils
    
    # Test data
    refs = ["def add(a, b): return a + b"]
    preds = ["def add(x, y): return x + y"]
    
    # Test BLEU
    try:
        result = utils.bleu_score(refs, preds)
        assert 'bleu' in result
        assert 0 <= result['bleu'] <= 1
        print(f"  ✅ BLEU score: {result['bleu']:.3f}")
    except Exception as e:
        print(f"  ❌ BLEU metric failed: {e}")
        return False
    
    # Test ROUGE
    try:
        result = utils.rouge_score(refs, preds)
        assert 'rouge1' in result
        print(f"  ✅ ROUGE-1 score: {result['rouge1']:.3f}")
    except Exception as e:
        print(f"  ❌ ROUGE metric failed: {e}")
        return False
    
    # Test Edit Distance
    try:
        result = utils.edit_distance(refs, preds)
        assert 'edit_distance' in result
        print(f"  ✅ Edit distance: {result['edit_distance']:.3f}")
    except Exception as e:
        print(f"  ❌ Edit distance failed: {e}")
        return False
    
    # Test Pass@k (mock test)
    try:
        test_cases = ["assert add(2, 3) == 5"]
        pred_code = [["def add(a, b): return a + b"]]
        result = utils.pass_at_k(test_cases, pred_code, k=[1])
        assert 'pass@1' in result
        print(f"  ✅ Pass@1 score: {result['pass@1']:.3f}")
    except Exception as e:
        print(f"  ❌ Pass@k metric failed: {e}")
        return False
    
    return True

def test_problem_completeness():
    """Test that problems have all required fields."""
    print("Testing problem completeness...")
    
    required_fields_by_category = {
        'code_completion': ['category', 'incomplete_code', 'expected_completion'],
        'code_repair': ['category', 'buggy_code', 'error_description', 'fixed_code', 'test_cases'],
        'code_translation': ['category', 'source_language', 'source_code', 'target_code'],
        'docstring_generation': ['category', 'function_code', 'expected_docstring'],
        'function_generation': ['category', 'function_description', 'requirements', 'test_cases']
    }
    
    with open('problems.jsonl', 'r') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            data = json.loads(line)
            category = data['category']
            required_fields = required_fields_by_category[category]
            
            for field in required_fields:
                if field not in data:
                    print(f"  ❌ Line {i} ({category}): Missing field '{field}'")
                    return False
    
    print("  ✅ All problems have required fields")
    return True

def main():
    """Run all tests."""
    print("🧪 Testing Python Coding Evaluation Framework\n")
    
    tests = [
        test_jsonl_format,
        test_yaml_configs, 
        test_custom_metrics,
        test_problem_completeness
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Framework is ready to use.")
        print("\nTo run evaluations:")
        print("# Complete suite:")
        print("lm_eval --model anthropic-chat --model_args model=claude-3-5-haiku-20241022 --tasks python_coding_suite")
        print("\n# Single task:")
        print("lm_eval --model anthropic-chat --model_args model=claude-3-5-haiku-20241022 --tasks python_code_completion")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    main()