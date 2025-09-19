# ✅ Working Commands: Python Code Quality Evaluation

## ⚠️ **Anthropic Issue Resolved**

The `anthropic-completions` model has a tokenizer issue in this lm-eval version. Here are the **working alternatives**:

## 🧪 **Step 1: Verify Task Works**

```bash
# Quick verification test
python test_task_simple.py

# Or manual dummy test
lm_eval \
  --model dummy \
  --tasks python_code_quality \
  --output_path test_results/dummy_test.json \
  --log_samples \
  --limit 2 \
  --batch_size 1 \
  --predict_only
```

## 🚀 **Step 2: Run Your Local Model**

### Option A: Chat Completions API (Recommended)
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

### Option B: Completions API (Alternative)
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

## 📊 **View Results**

```bash
# Main evaluation metrics
cat output_code_results/qwen_code_quality_results.json

# Individual code responses from your model
cat output_code_results/samples_python_code_quality.jsonl

# Extract just the metric scores
grep -E "(code_quality_score|functional_correctness|syntax_validity|code_style_score)" output_code_results/qwen_code_quality_results.json
```

## 🎯 **What You'll Get**

### Metrics (0-1 scale):
- **Code Quality Score**: Composite quality assessment
- **Functional Correctness**: Test pass rate
- **Syntax Validity**: Syntactically correct code percentage  
- **Code Style Score**: Best practices adherence

### Test Problems (First 2):
1. **Factorial Function**: Calculate n! with error handling
2. **Palindrome Checker**: Detect palindromes ignoring case/spaces

## 📁 **Output Files**

```
output_code_results/
├── qwen_code_quality_results.json         # Main metrics
├── samples_python_code_quality.jsonl     # Individual responses
└── configs/
    └── python_code_quality.yaml          # Task configuration
```

## 🔧 **Troubleshooting**

### Common Issues:
- **"task not found"**: Run from repo root directory
- **Connection errors**: Check your local server at `http://localhost:1234`
- **Chat template errors**: Try Option B (completions API) instead

### Quick Fixes:
```bash
# Verify task is registered
lm_eval --tasks list | grep python_code_quality

# Test task loading
python test_task_simple.py

# Check your local server
curl http://localhost:1234/v1/models
```

## ✅ **Ready to Run!**

1. ✅ Task verified working (dummy test passes)
2. ✅ Two local model API options available
3. ✅ Comprehensive evaluation metrics implemented
4. ✅ Safe code execution environment ready
5. ✅ 20 diverse Python problems in dataset

**Choose Option A or B above and start evaluating your Qwen model!** 🚀