export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=./
export SERVICE_URL="http://localhost:8080/virtual"
export OUTPUT_DIR="data/answer/toolllama-cache"

group=G1_instruction

mkdir -p $OUTPUT_DIR; mkdir -p $OUTPUT_DIR/$group

python toolbench/inference/qa_pipeline.py \
    --tool_root_dir data/toolenv/tools \
    --backbone_model toolllama \
    --model_path ToolBench/ToolLLaMA-2-7b-v2 \
    --max_observation_length 1024 \
    --method CoT@1 \
    --input_query_file solvable_queries/test_instruction/${group}.json \
    --output_answer_file $OUTPUT_DIR/$group
