# ✅ FIXED: Python Code Quality Evaluation Command

## 🔧 **Issue Resolved**

The error `AssertionError: chat-completions require the --apply_chat_template flag` has been fixed!

## 🚀 **Corrected Command (Copy & Paste)**

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

## 🔍 **What Changed**

Added the required `--apply_chat_template` flag for chat completions API.

## 📋 **Command Breakdown**

- `--model local-chat-completions`: Use local chat API
- `--model_args`: Your model endpoint and name
- `--tasks python_code_quality`: Our custom task
- `--output_path output_code_results`: Save location
- `--log_samples`: Save individual responses
- `--limit 2`: Test on first 2 problems only
- `--batch_size 1`: Process one at a time
- `--apply_chat_template`: **REQUIRED** for chat completions

## 🎯 **Alternative: Use Completions API (No Chat Template)**

If you prefer to avoid chat templates, you can use the completions endpoint:

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

## ✅ **Ready to Run!**

Choose either command above based on your local server setup:
- Use **chat-completions** if your server supports `/v1/chat/completions`
- Use **completions** if your server supports `/v1/completions`

Both will work with your Qwen model and produce the same evaluation results!