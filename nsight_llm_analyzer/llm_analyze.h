#ifndef LLM_ANALYZE_H
#define LLM_ANALYZE_H

#include <string>
#include <nlohmann/json.hpp>

std::string llm_analyze(const nlohmann::json& data);
nlohmann::json read_json_file(const std::string& filepath);

#endif // LLM_ANALYZE_H
