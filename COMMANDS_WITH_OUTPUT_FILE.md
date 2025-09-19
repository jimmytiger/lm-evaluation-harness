# 🎯 Commands with Specific Output File Names

## 🚀 **Option 1: Chat Completions API**

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

## 🔄 **Option 2: Completions API**

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

## 📁 **Output Files Created**

```
output_code_results/
├── qwen_code_quality_results.json           # Main results (your specified filename)
├── samples_python_code_quality.jsonl       # Individual model responses
└── configs/
    └── python_code_quality.yaml            # Task configuration used
```

## 📊 **View Results**

After running, check your results:

```bash
# View main results with specified filename
cat output_code_results/qwen_code_quality_results.json

# View detailed individual responses
cat output_code_results/samples_python_code_quality.jsonl
```

## 🎯 **Key Changes**

- **Specific output filename**: `qwen_code_quality_results.json` instead of default `results.json`
- **Fixed duplicate flag**: Removed duplicate `--apply_chat_template`
- **Clear file structure**: Shows exactly what files will be created

Choose either command based on your local server's API endpoint!