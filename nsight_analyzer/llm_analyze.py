import json
import os
import openai

def read_mock_data(directory):
    data_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data_files.append((filename, json.load(file)))
    return data_files

def llm_analyze(data):
    prompt = f"""
    Analyze the following Nsight Systems data for performance bottlenecks and resource usage:
    {json.dumps(data, indent=2)}
    
    Identify areas that should be inspected further for bottlenecks. Suggest areas taking up the most resources and provide general optimization advice.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes performance data."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

