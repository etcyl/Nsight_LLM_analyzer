cmake_minimum_required(VERSION 3.10)
project(NsightLLMAnalyzer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_executable(NsightLLMAnalyzer main.cpp nsight_llm_analyzer/llm_analyze.cpp)

target_include_directories(NsightLLMAnalyzer PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(NsightLLMAnalyzer PRIVATE curl)
