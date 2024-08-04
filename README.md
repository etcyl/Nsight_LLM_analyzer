Nsight LLM Analyzer

Nsight LLM Analyzer is a tool that reads output from NVIDIA Nsight Systems, analyzes it using OpenAI's GPT-4, and provides insights on performance bottlenecks and resource usage. This repository includes a modular Python package for performing the analysis and a main script for running the tool.

Directory Structure


Nsight_LLM_analyzer/
    nsight_analyzer/
        __init__.py
        llm_analyze.py
    main.py
    mock_data/
        nsight_output.json
    tests/
        __init__.py
        test_llm_analyze.py

Files Description

    nsight_analyzer/: This directory contains the core analysis module.
        __init__.py: Makes the directory a package.
        llm_analyze.py: Contains functions to read mock data and analyze it using OpenAI's GPT-4.

    main.py: The main script that runs the tool by reading the mock data and invoking the analysis.

    mock_data/: Contains mock data files.
        nsight_output.json: Example JSON file representing Nsight Systems output.

    tests/: Contains unit tests for the analysis module.
        __init__.py: Makes the directory a package.
        test_llm_analyze.py: Unit tests for llm_analyze.py using unittest and unittest.mock.

Installation

Clone the repository:
    ```git clone <repository_url>```
    ```cd Nsight_LLM_analyzer```

Set up a virtual environment:
    ```python -m venv myenv```
    ```source myenv/bin/activate  # On Windows use `myenv\Scripts\activate` ```

Set the OpenAI API key as an environment variable:
    On Linux:
    ```export OPENAI_API_KEY="your_openai_api_key"```  
    On Windows:
    ```set OPENAI_API_KEY="your_openai_api_key"```


Run the main script:
    ```python main.py```

Running Tests

Ensure you have pytest installed:
    ```pip install pytest```

Run the tests:
    ```pytest tests/test_llm_analyze.py```

This will execute the unit tests and validate the functionality of the llm_analyze module.

Detailed Explanation
nsight_analyzer/llm_analyze.py

This module contains two main functions:

    read_mock_data(directory): Reads JSON files from the specified directory and returns a list of tuples containing filenames and their data.

    llm_analyze(data): Sends the provided data to OpenAI's GPT-4 for analysis. Constructs a prompt with the data and requests insights on performance bottlenecks and resource usage.

main.py

The main script that:

    Sets the OpenAI API key from the environment variable.
    Reads data files from the mock_data/ directory using read_mock_data.
    Analyzes each data file using llm_analyze.
    Prints the analysis results.

tests/test_llm_analyze.py

Unit tests for the llm_analyze module using unittest and unittest.mock:

    test_llm_analyze: Mocks the OpenAI API call and verifies that the llm_analyze function returns the expected analysis output.
    test_read_mock_data: Mocks file reading and verifies that the read_mock_data function correctly reads and parses the JSON files.