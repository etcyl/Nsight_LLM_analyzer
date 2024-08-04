import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nsight_analyzer.llm_analyze import read_mock_data, llm_analyze

class TestLlmAnalyze(unittest.TestCase):
    
    @patch('nsight_analyzer.llm_analyze.openai.ChatCompletion.create')
    def test_llm_analyze(self, mock_create):
        # Prepare mock response
        mock_response = {
            'choices': [{'message': {'content': "Mock analysis output"}}]
        }
        mock_create.return_value = mock_response
        
        # Sample input data
        sample_data = {
            "sessions": [
                {
                    "name": "Session 1",
                    "duration": 120.5,
                    "cpu_usage": 75.2,
                    "gpu_usage": 88.3,
                    "memory_usage": 62.5,
                    "disk_io": 15.2,
                    "network_io": 5.7,
                    "events": [
                        {"name": "event_1", "duration": 30.1, "cpu_usage": 50.3, "gpu_usage": 60.0},
                        {"name": "event_2", "duration": 40.2, "cpu_usage": 70.5, "gpu_usage": 85.7},
                        {"name": "event_3", "duration": 50.2, "cpu_usage": 90.1, "gpu_usage": 95.3}
                    ]
                }
            ]
        }
        
        # Call the function
        result = llm_analyze(sample_data)
        
        # Assertions
        self.assertEqual(result, "Mock analysis output")
        mock_create.assert_called_once()

    @patch('nsight_analyzer.llm_analyze.os.listdir')
    @patch('nsight_analyzer.llm_analyze.open', new_callable=mock_open, read_data=json.dumps({
        "sessions": [
            {
                "name": "Session 1",
                "duration": 120.5,
                "cpu_usage": 75.2,
                "gpu_usage": 88.3,
                "memory_usage": 62.5,
                "disk_io": 15.2,
                "network_io": 5.7,
                "events": [
                    {"name": "event_1", "duration": 30.1, "cpu_usage": 50.3, "gpu_usage": 60.0},
                    {"name": "event_2", "duration": 40.2, "cpu_usage": 70.5, "gpu_usage": 85.7},
                    {"name": "event_3", "duration": 50.2, "cpu_usage": 90.1, "gpu_usage": 95.3}
                ]
            }
        ]
    }))
    def test_read_mock_data(self, mock_open, mock_listdir):
        # Mock listdir to return a list of files
        mock_listdir.return_value = ['mock_file.json']
        
        # Call the function
        data = read_mock_data('mock_data/')
        
        # Assertions
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 'mock_file.json')
        self.assertIn('sessions', data[0][1])
        mock_listdir.assert_called_once_with('mock_data/')
        mock_open.assert_called_once_with(os.path.join('mock_data/', 'mock_file.json'), 'r')

if __name__ == '__main__':
    unittest.main()
