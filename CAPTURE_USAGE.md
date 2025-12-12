# 截获StableToolBench推理对话使用说明

## 功能说明

`capture_first_query.py` 脚本用于截获StableToolBench推理时第一个query的完整对话历史，包括：
- 系统提示（system message）
- 用户查询（user query）
- 模型回复（assistant responses）
- Function调用和响应（function calls and responses）
- 步骤信息（step-by-step information）

## 使用方法

### 基本用法

```bash
cd StableToolBench
python capture_first_query.py \
    --tool_root_dir data/toolenv/tools \
    --model_path ToolBench/ToolLLaMA-2-7b-v2 \
    --input_query_file solvable_queries/test_instruction/G1_instruction.json \
    --output_file captured_conversation.json \
    --service_url http://localhost:8080/virtual
```

### 参数说明

- `--tool_root_dir`: Tool根目录路径（必需）
- `--model_path`: 模型路径（必需）
- `--input_query_file`: 输入查询文件（必需）
- `--output_file`: 输出文件路径（默认：captured_conversation.json）
- `--backbone_model`: 骨干模型类型（默认：toolllama）
- `--max_observation_length`: 最大观察长度（默认：1024）
- `--method`: 推理方法（默认：CoT@1）
- `--max_sequence_length`: 最大序列长度（默认：8192）
- `--max_source_sequence_length`: 最大源序列长度（默认：4096）
- `--toolbench_key`: ToolBench API密钥（可选）
- `--service_url`: 服务URL（默认：http://localhost:8080/virtual）

### 输出格式

输出的JSON文件包含以下字段：

```json
{
  "query": "用户查询内容",
  "method": "CoT@1",
  "conversations": [
    {
      "from": "system",
      "value": "系统提示..."
    },
    {
      "from": "user",
      "value": "用户查询..."
    },
    {
      "from": "assistant",
      "value": "模型回复（包含Thought/Action/Action Input）..."
    },
    {
      "from": "function",
      "value": "{\"error\": \"\", \"response\": \"...\"}"
    }
  ],
  "full_messages": [...],
  "step_by_step": [
    {
      "node_type": "Thought",
      "description": "...",
      "observation": "...",
      "observation_code": null
    }
  ],
  "outputs": "最终输出"
}
```

### 示例

```bash
# 使用默认参数
python capture_first_query.py \
    --tool_root_dir data/toolenv/tools \
    --model_path ToolBench/ToolLLaMA-2-7b-v2 \
    --input_query_file solvable_queries/test_instruction/G1_instruction.json

# 指定输出文件
python capture_first_query.py \
    --tool_root_dir data/toolenv/tools \
    --model_path ToolBench/ToolLLaMA-2-7b-v2 \
    --input_query_file solvable_queries/test_instruction/G1_instruction.json \
    --output_file my_captured_conversation.json
```

## 注意事项

1. 确保ToolBench服务器正在运行（如果使用virtual模式）
2. 脚本只会处理第一个query，用于格式检查
3. 输出的对话格式与StableToolBench数据格式一致
4. 可以用于验证模型输入输出格式是否正确
