cd  toolbench/tooleval

export API_POOL_FILE=../../openai_key.json
export CONVERTED_ANSWER_PATH=../../data/model_predictions_converted
export SAVE_PATH=../../data/pass_rate_results
export CANDIDATE_MODEL=toolllama
export EVAL_MODEL=gpt-3.5-turbo
export TEST_SET=G1_instruction

mkdir -p ${SAVE_PATH}/${CANDIDATE_MODEL}

python eval_pass_rate.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --save_path ${SAVE_PATH}/${CANDIDATE_MODEL} \
    --reference_model ${CANDIDATE_MODEL} \
    --test_ids ../../solvable_queries/test_query_ids \
    --max_eval_threads 30 \
    --evaluate_times 3 \
    --test_set $TEST_SET \
    --overwrite
