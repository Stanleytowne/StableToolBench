#!/bin/bash
# 运行capture_first_query.py的便捷脚本
# 确保在StableToolBench根目录下运行

export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=./  # 关键：设置PYTHONPATH为当前目录
export SERVICE_URL="http://localhost:8080/virtual"

# 默认参数
TOOL_ROOT_DIR=${TOOL_ROOT_DIR:-"data/toolenv/tools"}
MODEL_PATH=${MODEL_PATH:-"ToolBench/ToolLLaMA-2-7b-v2"}
INPUT_QUERY_FILE=${INPUT_QUERY_FILE:-"solvable_queries_example/test_instruction/G1_instruction.json"}
OUTPUT_FILE=${OUTPUT_FILE:-"captured_conversation.json"}

python capture_first_query.py \
    --tool_root_dir "$TOOL_ROOT_DIR" \
    --model_path "$MODEL_PATH" \
    --input_query_file "$INPUT_QUERY_FILE" \
    --output_file "$OUTPUT_FILE" \
    --service_url "$SERVICE_URL" \
    "$@"
