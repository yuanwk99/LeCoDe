# LeCoDe: Legal Consultation Dialogue Benchmark
This repository contains the source code for LeCoDe, a comprehensive benchmark dataset for legal consultation dialogue evaluation.

## ✨ Overview
LeCoDe is designed to evaluate the capabilities of Large Language Models (LLMs) in legal consultation scenarios through multi-turn dialogues.


## 🚀 Getting Started

### Prerequisites
To embark on this journey, you’ll need:
- Python versions: 3.9 - 3.12
- A CUDA-compatible GPU is recommended for optimal performance.

### Installation

We recommend creating a new Python environment using either conda or [uv](https://docs.astral.sh/uv/) and first install vLLM.
For installing vLLM, follow the [official guide](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html).

```bash
# If you prefer conda
conda create -n lecode_env python=3.10 -y
conda activate lecode_env
conda install vllm

# Or try out uv
uv conda create -n lecode_env python=3.10 -y
uv conda activate lecode_env
uv conda install vllm
```


Next, install required dependencies refer to requirement.txt:




## 🗂️ Dataset Details

### Dataset
- **LeCoDe_trainset.jsonl**
- **LeCoDe_testset.jsonl**

### Statistics at a Glance

| Metric | Total | Train Set | Test Set |
|--------|--------|------------|-----------|
| Dialogue Samples | 3,696 | 2,956 | 740 |
| Total Turns | 110,008 | 88,342 | 21,666 |
| Avg Key Facts/Dialogue | 9.19 | 9.24 | 9.01 |

### Understanding Data Structure
```python
{
    'id': 'string',
    'dialogue': [
        ['user', "utterance"],
        ['lawyer', "response"],
        ...
    ],
    'initial_query': "string",
    'suggestion': "string",
    'key_fact_dict_hard_version': {
        'atomic_facts': {
            '0': 'F1.',
            '1': 'F2.',
            '2': 'F3.',
        },
        'importance_scores': {
            '0': 2.0,  # Secondary fact
            '1': 1.0,  # Non-critical fact
            '2': 3.0,  # Critical fact
        }
    },
    'case_type': ['Criminal'],  # Options: ['Criminal','Civil','Administrative']
    'charge_type': ['Theft'],
    'intention_annotation': [
        ['Client', 'text', '[1] Client Initial Query'],
        ...
    ]
}
```

## 🛠️ Evaluation Framework

### Configure Your Setup
Tailor the evaluation configuration in `args.py` to suit your needs:
```python
--input_data: Path to evaluation data
--output_file: Path for generated interaction data
--MAX_TURNS: Maximum interaction turns (default: 10)
--lawyer_mode: ["direct_ask","fewshot_ask","mediq_ask"]
--lawyer_model: LLM choice (API model version or absolute path for vLLM)
--user_mode: Default "direct_answer"
--user_model: Default "qwen-max"
```

### Running Evaluations

1. **LLM Setup**
   - If you're utilizing API-based LLMs (like GPT-series, qwen-max), ensure your API keys are adjusted in `src/lecode_util/call_llm.py`.
   
   - To deploy locally LLM with vLLM:
     ```bash
     vllm serve <model-path> --tensor-parallel-size <gpu-count> --max-model-len 2048 --enforce-eager
     ```
        where:
     - `<model-path>`: Absolute path to the model (strongly recommended)
     - `<gpu-count>`: Number of GPUs to utilize

2. **Run Evaluation**
   ```bash
   sh run.sh
   ```
   - Note: Parallel processing is enabled by default. To adjust the number of parallel workers, modify the max_worker parameter in lecode_main.py.


   For failed samples, retry unsuccessful samples with:
   ```bash
   python lecode_run_error.py
   ```

3. **Calculate Metrics**
   
   step1: run run_evaluation.sh
   ```bash
   sh run_evaluation.sh
   ```
   - This script will generate a CSV file at outputs/evaluation_output/xx.csv


   step2: 
   - Open LLM_evaluation.ipynb
   - Update the path variable:
        ```python
        path = "xx"  # like ""output_file_ask_q""
        ```
    - Run all cells to obtain the final evaluation results

## Ethical Consideration
Our work focuses on evaluating LLMs capability on legal consultation, rather than replacing human judges or being directly used in real-world decision-making applications. In practical use, human judges should act as the final safeguard to maintain fairness and mitigate the potential harms related to algorithms. **All resources are for scientific research only**.


## ❗️ Licenses
This work is licensed under a Creative Commons Attribution- NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0). **All resources are for scientific research only.**

