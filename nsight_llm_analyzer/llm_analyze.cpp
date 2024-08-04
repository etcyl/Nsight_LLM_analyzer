#include "llm_analyze.h"
#include <fstream>
#include <sstream>
#include <curl/curl.h>

std::string llm_analyze(const nlohmann::json& data) {
    // Create the prompt
    std::stringstream prompt;
    prompt << "Analyze the following Nsight Systems data for performance bottlenecks and resource usage:\n";
    prompt << data.dump(2) << "\n\n";
    prompt << "Identify areas that should be inspected further for bottlenecks. Suggest areas taking up the most resources and provide general optimization advice.";

    // OpenAI API call setup
    std::string api_key = std::getenv("OPENAI_API_KEY");
    if (api_key.empty()) {
        throw std::runtime_error("OPENAI_API_KEY environment variable not set");
    }

    std::string url = "https://api.openai.com/v1/chat/completions";
    std::string model = "gpt-4";
    nlohmann::json request_body = {
        {"model", model},
        {"messages", {
            {{"role", "system"}, {"content", "You are a helpful assistant that analyzes performance data."}},
            {{"role", "user"}, {"content", prompt.str()}}
        }}
    };

    std::string request_data = request_body.dump();

    // CURL setup
    CURL* curl = curl_easy_init();
    CURLcode res;
    std::string response_string;
    std::string header_string;
    struct curl_slist* headers = NULL;

    if (curl) {
        headers = curl_slist_append(headers, ("Authorization: Bearer " + api_key).c_str());
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, request_data.c_str());

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, [](char* ptr, size_t size, size_t nmemb, std::string* data) {
            data->append(ptr, size * nmemb);
            return size * nmemb;
        });

        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &header_string);

        res = curl_easy_perform(curl);

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

        if (res != CURLE_OK) {
            throw std::runtime_error("CURL request failed: " + std::string(curl_easy_strerror(res)));
        }
    }

    nlohmann::json response_json = nlohmann::json::parse(response_string);
    return response_json["choices"][0]["message"]["content"];
}

nlohmann::json read_json_file(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open file: " + filepath);
    }

    nlohmann::json data;
    file >> data;
    return data;
}
