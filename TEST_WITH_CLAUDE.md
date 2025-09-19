# 🧪 Test Python Code Quality Task 

## ⚠️ **Anthropic Model Issue Detected**

There's currently an issue with the `anthropic-completions` model in this version of lm-eval. Let's use alternative testing methods.

## 🎯 **Primary Test: Dummy Model (Always Works)**

First, verify the task works with the dummy model:

```bash
lm_eval \
  --model dummy \
  --tasks python_code_quality \
  --output_path test_results/dummy_test.json \
  --log_samples \
  --limit 2 \
  --batch_size 1 \
  --predict_only
```

## 🔑 **Prerequisites**

Make sure you have your Anthropic API key set:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

Install the Anthropic package if needed:
```bash
pip install anthropic
```

## 🔄 **Alternative: Skip Hosted Model Testing**

Since the Anthropic integration has issues, you can skip directly to testing your local model:

```bash
# Test your local model directly
lm_eval \
  --model local-chat-completions \
  --model_args base_url=http://localhost:1234/v1/chat/completions,model=qwen/qwen3-1.7b \
  --tasks python_code_quality \
  --output_path output_code_results/qwen_test.json \
  --log_samples \
  --limit 2 \
  --batch_size 1 \
  --apply_chat_template
```

## 🔄 **Alternative: Local Completions API**

If chat completions don't work, try the completions endpoint:

```bash
lm_eval \
  --model local-completions \
  --model_args base_url=http://localhost:1234/v1/completions,model=qwen/qwen3-1.7b \
  --tasks python_code_quality \
  --output_path output_code_results/qwen_completions_test.json \
  --log_samples \
  --limit 2 \
  --batch_size 1
```

## 📊 **What This Test Will Do**

- **Verify task loading**: Confirms the task configuration is correct
- **Test dataset**: Ensures the 20 problems load properly
- **Validate metrics**: Checks all 4 custom metrics work
- **Test code execution**: Verifies safe code execution environment
- **Generate sample results**: Shows what output format to expect

## 🎯 **Test Problems (First 2)**

1. **Factorial Function**: Calculate n! with proper error handling
2. **Palindrome Checker**: Detect palindromes ignoring case/spaces

## 📁 **Expected Test Output**

```
test_results/
├── dummy_test.json                         # Dummy model test results
└── samples_python_code_quality.jsonl      # Dummy responses (for format verification)

output_code_results/
├── qwen_test.json                          # Your model's results
├── samples_python_code_quality.jsonl      # Your model's code responses
└── configs/
    └── python_code_quality.yaml           # Task configuration
```

## 🔍 **Verify Test Results**

After running, check the results:

```bash
# View dummy test results (confirms task works)
cat test_results/dummy_test.json

# View your model's actual results
cat output_code_results/qwen_test.json

# Check if all metrics are present in your model's results
grep -E "(code_quality_score|functional_correctness|syntax_validity|code_style_score)" output_code_results/qwen_test.json
```

## ✅ **Expected Metrics**

Your Qwen model should produce scores like:
- **Code Quality Score**: 0.7-0.9 (high quality code)
- **Functional Correctness**: 0.8-1.0 (passes most tests)
- **Syntax Validity**: 1.0 (always syntactically correct)
- **Code Style Score**: 0.6-0.9 (good practices)

## 🚀 **After Successful Test**

Once this test passes, you can confidently run with your local model:

```bash
# Your local model command (after test succeeds)
lm_eval \
  --model local-chat-completions \
  --model_args base_url=http://localhost:1234/v1/chat/completions,model=qwen/qwen3-1.7b \
  --tasks python_code_quality \
  --output_path output_code_results/qwen_code_quality_results.json \
  --log_samples \
  --limit 2 \
  --batch_size 1 \
  --apply_chat_template
```

## 🔧 **Troubleshooting**

If the test fails:
1. **API Key**: Ensure `ANTHROPIC_API_KEY` is set correctly
2. **Network**: Check internet connection for API access
3. **Dependencies**: Ensure `anthropic` package is installed: `pip install anthropic`
4. **Task Loading**: Verify you're in the correct directory with the task files

## 💡 **Why Test with Claude?**

- **Excellent code generation**: Claude is particularly strong at generating high-quality Python code
- **Validates task**: Confirms our evaluation metrics work correctly
- **Reference results**: Provides comparison point for your local model
- **Quick verification**: Faster than debugging local model issues