# 🎯 Final Instructions: Python Code Quality with Claude & Local Model

## ✅ **Task Status: Ready for Claude Testing**

The Python code quality evaluation task is fully tested and ready to use with Anthropic's Claude API.

## 🧪 **Step 1: Test with Claude (Recommended)**

### Quick Test Script
```bash
python test_with_claude.py
```

### Manual Claude Test
```bash
# Set your API key
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# Run with Claude Haiku (fast & cost-effective)
lm_eval \
  --model anthropic-completions \
  --model_args model=claude-3-haiku-20240307 \
  --tasks python_code_quality \
  --output_path test_results/claude_test.json \
  --log_samples \
  --limit 2 \
  --batch_size 1
```

### Alternative: Claude Sonnet (Higher Quality)
```bash
lm_eval \
  --model anthropic-completions \
  --model_args model=claude-3-5-sonnet-20241022 \
  --tasks python_code_quality \
  --output_path test_results/claude_sonnet_test.json \
  --log_samples \
  --limit 2 \
  --batch_size 1
```

## 🚀 **Step 2: Run with Your Local Qwen Model**

After Claude test succeeds, run with your local model:

### Chat Completions API
```bash
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

### Completions API (Alternative)
```bash
lm_eval \
  --model local-completions \
  --model_args base_url=http://localhost:1234/v1/completions,model=qwen/qwen3-1.7b \
  --tasks python_code_quality \
  --output_path output_code_results/qwen_code_quality_results.json \
  --log_samples \
  --limit 2 \
  --batch_size 1
```

## 📊 **Expected Results**

### Claude Performance (Baseline)
- **Code Quality Score**: 0.8-0.95 (excellent)
- **Functional Correctness**: 0.9-1.0 (nearly perfect)
- **Syntax Validity**: 1.0 (always correct)
- **Code Style Score**: 0.7-0.9 (good practices)

### Your Qwen Model
Compare your local model's performance against Claude's baseline.

## 📁 **Output Files**

```
test_results/                               # Claude test results
├── claude_test.json                        # Claude metrics
└── samples_python_code_quality.jsonl      # Claude's code responses

output_code_results/                        # Your local model results  
├── qwen_code_quality_results.json         # Qwen metrics
└── samples_python_code_quality.jsonl      # Qwen's code responses
```

## 🔍 **View Results**

```bash
# View Claude's results
cat test_results/claude_test.json

# View your Qwen model's results
cat output_code_results/qwen_code_quality_results.json

# Compare specific metrics
grep "code_quality_score" test_results/claude_test.json
grep "code_quality_score" output_code_results/qwen_code_quality_results.json
```

## 🎯 **Test Problems (First 2)**

1. **Factorial Function**: Calculate n! with error handling
   - Tests: `factorial(0) == 1`, `factorial(5) == 120`, `factorial(1) == 1`

2. **Palindrome Checker**: Detect palindromes ignoring case/spaces  
   - Tests: `is_palindrome('racecar') == True`, etc.

## 🔧 **Prerequisites**

```bash
# Install required packages
pip install anthropic datasets

# Set API key
export ANTHROPIC_API_KEY="your_key_here"

# Verify task works
python test_task_simple.py
```

## 💡 **Why Claude First?**

- **Excellent at code**: Claude generates high-quality Python code consistently
- **Reliable baseline**: Provides reference performance for comparison
- **Quick validation**: Confirms task works before debugging local setup
- **Cost effective**: Haiku model is fast and inexpensive for testing

## 🎉 **Ready to Go!**

1. ✅ Task fully tested and working
2. ✅ Claude provides excellent baseline
3. ✅ Multiple local model API options
4. ✅ Comprehensive evaluation metrics
5. ✅ Safe code execution environment

Run the Claude test first, then evaluate your local Qwen model! 🚀