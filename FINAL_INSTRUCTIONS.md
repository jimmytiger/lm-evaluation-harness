# 🎯 Final Instructions: Python Code Quality Evaluation

## ✅ **WORKING COMMAND (Issue Fixed)**

The `AssertionError: chat-completions require the --apply_chat_template flag` has been resolved!

### 🚀 **Option 1: Chat Completions API (Recommended)**

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

### 🔄 **Option 2: Completions API (Alternative)**

If your server doesn't support chat templates or you prefer the completions endpoint:

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

## 🔧 **What Was Fixed**

1. **Added `--apply_chat_template` flag** for chat completions API
2. **Provided alternative completions API** option
3. **Verified task loads and runs successfully**

## 📊 **Expected Results**

After running either command, you'll get:

```
output_code_results/
├── qwen_code_quality_results.json           # Main evaluation metrics (specified filename)
├── samples_python_code_quality.jsonl       # Individual model responses
└── configs/                                 # Task configuration
    └── python_code_quality.yaml
```

**Metrics provided:**
- **Code Quality Score** (0-1): Composite quality assessment
- **Functional Correctness** (0-1): Test pass rate  
- **Syntax Validity** (0-1): Syntactically correct code percentage
- **Code Style Score** (0-1): Best practices adherence

## 🎯 **Test Problems (First 2 with --limit 2)**

1. **Factorial Function**: Calculate n! with edge case handling
2. **Palindrome Checker**: Detect palindromes ignoring case/spaces

## ✅ **Status: Ready to Execute**

- ✅ Task verified working with lm-eval
- ✅ Dataset loads properly (20 problems total)
- ✅ Custom metrics functional
- ✅ Safe code execution environment ready
- ✅ Both API options tested

## 🚀 **Just Run It!**

Copy either command above and execute. Your evaluation will complete quickly and provide comprehensive code quality metrics for your Qwen model on 2 Python programming problems.

**Choose based on your server setup:**
- Use **Option 1** if `/v1/chat/completions` endpoint available
- Use **Option 2** if `/v1/completions` endpoint available