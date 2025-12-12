cd toolbench/tooleval

RAW_ANSWER_PATH=../../data/answer
CONVERTED_ANSWER_PATH=../../data/model_predictions_converted
MODEL_NAME=toolllama
test_set=G1_instruction

mkdir -p ${CONVERTED_ANSWER_PATH}/${MODEL_NAME}
answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json

python convert_to_answer_format.py\
    --answer_dir ${answer_dir} \
    --method CoT@1 \
    --output ${output_file}

 # DFS_woFilter_w2 for DFS
