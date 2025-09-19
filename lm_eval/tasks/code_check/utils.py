import ast
import re
import sys
import io
import contextlib
import traceback
from typing import List, Dict, Any, Union
import json
import os

try:
    from datasets import Dataset
except ImportError:
    Dataset = None


def load_dataset(**kwargs):
    """Load the local Python code quality dataset."""
    current_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(current_dir, "python_code_quality_dataset.json")
    
    with open(dataset_path, 'r') as f:
        data = json.load(f)
    
    # Return in the format expected by lm-eval
    if Dataset is None:
        raise ImportError("datasets library is required but not installed")
    
    processed_data = []
    for item in data:
        doc = {
            'id': item['id'],
            'problem': item['problem'],
            'description': item['description'],
            'test_cases': item['test_cases'],
            'expected_solution': item['expected_solution']
        }
        processed_data.append(doc)
    
    dataset = Dataset.from_list(processed_data)
    return {"test": dataset}


def process_docs(dataset):
    """Process the dataset to match the expected format."""
    # The dataset is already in the right format from load_dataset
    return dataset


def extract_python_code(text: str) -> str:
    """Extract Python code from the generated text."""
    # Try to find code blocks first
    code_block_pattern = r'```(?:python)?\s*\n?(.*?)\n?```'
    matches = re.findall(code_block_pattern, text, re.DOTALL | re.IGNORECASE)
    
    if matches:
        # If multiple code blocks, return the last one (likely the actual solution)
        code = matches[-1].strip()
        # Remove any test cases or assertions from the extracted code
        return _clean_function_code(code)
    
    # If no code blocks, try to find ALL function definitions and return the last one
    lines = text.split('\n')
    all_functions = []
    current_function = []
    in_function = False
    
    for line in lines:
        if line.strip().startswith('def '):
            # If we were already in a function, save it
            if in_function and current_function:
                all_functions.append('\n'.join(current_function))
            # Start new function
            in_function = True
            current_function = [line]
        elif in_function:
            # Stop at assert statements or comments that look like test cases
            if (line.strip().startswith('assert ') or 
                line.strip().startswith('# Test') or
                line.strip().startswith('# test')):
                # End function here, don't include test cases
                if current_function:
                    all_functions.append('\n'.join(current_function))
                in_function = False
                current_function = []
            elif line.strip() == '' or line.startswith('    ') or line.startswith('\t'):
                current_function.append(line)
            else:
                # End of function - save it and stop tracking
                if current_function:
                    all_functions.append('\n'.join(current_function))
                in_function = False
                current_function = []
    
    # Don't forget the last function if the text ends while in a function
    if in_function and current_function:
        all_functions.append('\n'.join(current_function))
    
    if all_functions:
        # Return the LAST function found (should be the actual solution, not the few-shot example)
        return all_functions[-1].strip()
    
    # Fallback: return the entire text
    return text.strip()


def _clean_function_code(code: str) -> str:
    """Remove test cases and assertions from function code."""
    lines = code.split('\n')
    clean_lines = []
    
    for line in lines:
        # Skip assert statements and test comments
        if (line.strip().startswith('assert ') or 
            line.strip().startswith('# Test') or
            line.strip().startswith('# test')):
            continue
        clean_lines.append(line)
    
    return '\n'.join(clean_lines).strip()


def safe_execute(code: str, test_cases: List[str]) -> Dict[str, Any]:
    """Safely execute code and run test cases."""
    result = {
        'syntax_valid': False,
        'execution_successful': False,
        'tests_passed': 0,
        'total_tests': len(test_cases),
        'error_message': '',
        'runtime_error': False
    }
    
    try:
        # Check syntax
        ast.parse(code)
        result['syntax_valid'] = True
    except SyntaxError as e:
        result['error_message'] = f"Syntax Error: {str(e)}"
        return result
    
    # Create a safe execution environment
    safe_globals = {
        '__builtins__': {
            'abs': abs, 'all': all, 'any': any, 'bin': bin, 'bool': bool,
            'chr': chr, 'dict': dict, 'enumerate': enumerate, 'filter': filter,
            'float': float, 'int': int, 'len': len, 'list': list, 'map': map,
            'max': max, 'min': min, 'ord': ord, 'range': range, 'reversed': reversed,
            'round': round, 'set': set, 'sorted': sorted, 'str': str, 'sum': sum,
            'tuple': tuple, 'zip': zip, 'isinstance': isinstance, 'ValueError': ValueError,
            'TypeError': TypeError, 'IndexError': IndexError, 'KeyError': KeyError
        }
    }
    
    try:
        # Execute the code
        exec(code, safe_globals)
        result['execution_successful'] = True
        
        # Run test cases
        for test_case in test_cases:
            try:
                exec(test_case, safe_globals)
                result['tests_passed'] += 1
            except Exception as e:
                if not result['error_message']:
                    result['error_message'] = f"Test failed: {str(e)}"
                
    except Exception as e:
        result['runtime_error'] = True
        result['error_message'] = f"Runtime Error: {str(e)}"
    
    return result


def analyze_code_quality(code: str) -> Dict[str, Any]:
    """Analyze various code quality metrics."""
    quality_metrics = {
        'has_docstring': False,
        'has_comments': False,
        'proper_naming': True,
        'line_count': 0,
        'complexity_score': 0,
        'has_error_handling': False,
        'follows_pep8_basics': True
    }
    
    if not code.strip():
        return quality_metrics
    
    lines = code.split('\n')
    quality_metrics['line_count'] = len([line for line in lines if line.strip()])
    
    try:
        tree = ast.parse(code)
        
        # Check for docstrings
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if (node.body and isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Str)):
                    quality_metrics['has_docstring'] = True
                
                # Check naming convention (snake_case)
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    quality_metrics['proper_naming'] = False
        
        # Check for comments
        if '#' in code:
            quality_metrics['has_comments'] = True
        
        # Check for error handling
        for node in ast.walk(tree):
            if isinstance(node, (ast.Try, ast.Raise)):
                quality_metrics['has_error_handling'] = True
                break
        
        # Simple complexity score based on control structures
        complexity = 1  # Base complexity
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
        
        quality_metrics['complexity_score'] = complexity
        
        # Basic PEP8 checks
        for line in lines:
            if len(line) > 79:  # Line too long
                quality_metrics['follows_pep8_basics'] = False
                break
    
    except SyntaxError:
        pass  # Already handled in safe_execute
    
    return quality_metrics


def code_quality_score(references: List[str], predictions: List[List[str]]) -> Dict[str, float]:
    """Calculate comprehensive code quality scores."""
    if not predictions:
        return {'code_quality_score': 0.0}
    
    total_scores = []
    
    for i, pred_list in enumerate(predictions):
        if not pred_list:
            total_scores.append(0.0)
            continue
        
        # Use the first prediction
        generated_code = extract_python_code(pred_list[0])
        
        # Get the corresponding test cases from the dataset
        try:
            current_dir = os.path.dirname(__file__)
            dataset_path = os.path.join(current_dir, "python_code_quality_dataset.json")
            with open(dataset_path, 'r') as f:
                raw_data = json.load(f)
            test_cases = raw_data[i]['test_cases'] if i < len(raw_data) else []
        except (FileNotFoundError, IndexError, KeyError):
            test_cases = []
        
        # Execute and test the code
        execution_result = safe_execute(generated_code, test_cases)
        
        # Analyze code quality
        quality_metrics = analyze_code_quality(generated_code)
        
        # Calculate composite score
        score = 0.0
        
        # Functional correctness (50% weight)
        if execution_result['syntax_valid']:
            score += 0.1  # 10% for valid syntax
            
            if execution_result['execution_successful']:
                score += 0.1  # 10% for successful execution
                
                # Test pass rate (30% weight)
                if execution_result['total_tests'] > 0:
                    test_score = execution_result['tests_passed'] / execution_result['total_tests']
                    score += 0.3 * test_score
        
        # Code quality metrics (50% weight)
        quality_score = 0.0
        
        # Proper naming (10%)
        if quality_metrics['proper_naming']:
            quality_score += 0.1
        
        # Has comments or docstring (10%)
        if quality_metrics['has_docstring'] or quality_metrics['has_comments']:
            quality_score += 0.1
        
        # Reasonable complexity (10%)
        if quality_metrics['complexity_score'] <= 5:  # Low complexity is good
            quality_score += 0.1
        elif quality_metrics['complexity_score'] <= 10:  # Medium complexity
            quality_score += 0.05
        
        # Error handling (10%)
        if quality_metrics['has_error_handling']:
            quality_score += 0.1
        
        # PEP8 basics (10%)
        if quality_metrics['follows_pep8_basics']:
            quality_score += 0.1
        
        score += quality_score
        total_scores.append(min(score, 1.0))  # Cap at 1.0
    
    return {'code_quality_score': sum(total_scores) / len(total_scores)}


def functional_correctness(references: List[str], predictions: List[List[str]]) -> Dict[str, float]:
    """Calculate functional correctness score (test pass rate)."""
    if not predictions:
        return {'functional_correctness': 0.0}
    
    total_scores = []
    
    for i, pred_list in enumerate(predictions):
        if not pred_list:
            total_scores.append(0.0)
            continue
        
        generated_code = extract_python_code(pred_list[0])
        
        # Get test cases
        try:
            current_dir = os.path.dirname(__file__)
            dataset_path = os.path.join(current_dir, "python_code_quality_dataset.json")
            with open(dataset_path, 'r') as f:
                raw_data = json.load(f)
            test_cases = raw_data[i]['test_cases'] if i < len(raw_data) else []
        except (FileNotFoundError, IndexError, KeyError):
            test_cases = []
        
        execution_result = safe_execute(generated_code, test_cases)
        
        if execution_result['total_tests'] > 0:
            score = execution_result['tests_passed'] / execution_result['total_tests']
        else:
            score = 0.0
        
        total_scores.append(score)
    
    return {'functional_correctness': sum(total_scores) / len(total_scores)}


def syntax_validity(references: List[str], predictions: List[List[str]]) -> Dict[str, float]:
    """Calculate syntax validity score."""
    if not predictions:
        return {'syntax_validity': 0.0}
    
    valid_count = 0
    total_count = len(predictions)
    
    for pred_list in predictions:
        if not pred_list:
            continue
        
        generated_code = extract_python_code(pred_list[0])
        
        try:
            ast.parse(generated_code)
            valid_count += 1
        except SyntaxError:
            pass
    
    return {'syntax_validity': valid_count / total_count if total_count > 0 else 0.0}


def code_style_score(references: List[str], predictions: List[List[str]]) -> Dict[str, float]:
    """Calculate code style and quality score."""
    if not predictions:
        return {'code_style_score': 0.0}
    
    total_scores = []
    
    for pred_list in predictions:
        if not pred_list:
            total_scores.append(0.0)
            continue
        
        generated_code = extract_python_code(pred_list[0])
        quality_metrics = analyze_code_quality(generated_code)
        
        # Calculate style score
        style_score = 0.0
        
        if quality_metrics['proper_naming']:
            style_score += 0.25
        
        if quality_metrics['has_docstring'] or quality_metrics['has_comments']:
            style_score += 0.25
        
        if quality_metrics['follows_pep8_basics']:
            style_score += 0.25
        
        if quality_metrics['complexity_score'] <= 5:
            style_score += 0.25
        elif quality_metrics['complexity_score'] <= 10:
            style_score += 0.125
        
        total_scores.append(style_score)
    
    return {'code_style_score': sum(total_scores) / len(total_scores)}


def build_predictions(resps: List[List[str]], docs: List[Dict]) -> List[List[str]]:
    """Build predictions by extracting code from responses."""
    return [[extract_python_code(r) for r in resp] for resp in resps]