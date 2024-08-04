import os
from nsight_analyzer.llm_analyze import read_mock_data, llm_analyze
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")
        
    data_directory = 'mock_data/'
    data_files = read_mock_data(data_directory)
    
    for filename, data in data_files:
        print(f"\n{'='*80}\nFile: {filename}\n{'='*80}")
        analysis = llm_analyze(data)
        print(f"Analysis Output:\n{analysis}\n{'='*80}")

if __name__ == "__main__":
    main()

