# ✅ Ready to Run: Python Code Quality Evaluation

## 🚀 **Working Command for Your Local Model**

The task has been **tested and verified working**. Use this command:

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

## 📊 **What This Will Do**

- **Evaluate your Qwen 3-1.7B model** on 2 Python coding problems
- **Generate comprehensive metrics**:
  - Code Quality Score (0-1)
  - Functional Correctness (0-1) 
  - Syntax Validity (0-1)
  - Code Style Score (0-1)
- **Save results** to `output_code_results/` directory
- **Log individual responses** for detailed analysis

## 🎯 **Test Problems (First 2)**

1. **Factorial Function**: Calculate factorial of a number
2. **Palindrome Checker**: Check if string reads same forwards/backwards

## 📁 **Expected Output Files**

```
output_code_results/
├── qwen_code_quality_results.json           # Main metrics summary (specified filename)
├── samples_python_code_quality.jsonl       # Individual model responses  
└── configs/                                 # Task configuration
    └── python_code_quality.yaml
```

## ✅ **Status: Verified Working**

- ✅ Task loads successfully in lm-eval
- ✅ Dataset loads properly (20 problems)
- ✅ Custom metrics work correctly
- ✅ Safe code execution environment ready
- ✅ All tests pass

## 🚀 **Ready to Execute!**

Just copy the command above and run it. Your evaluation will complete in minutes and provide comprehensive code quality metrics for your local Qwen model.