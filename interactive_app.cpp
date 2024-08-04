#include "crow_all.h"
#include "nsight_llm_analyzer/llm_analyze.h"
#include <fstream>
#include <sstream>
#include <ctime>

std::string get_current_timestamp() {
    std::time_t t = std::time(nullptr);
    char buffer[100];
    std::strftime(buffer, sizeof(buffer), "%Y%m%d_%H%M%S", std::localtime(&t));
    return std::string(buffer);
}

void save_to_file(const std::string& folder, const std::string& filename, const std::string& content) {
    std::ofstream file(folder + "/" + filename);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open file: " + filename);
    }
    file << content;
}

int main() {
    crow::SimpleApp app;

    CROW_ROUTE(app, "/")([]() {
        crow::mustache::context ctx;
        ctx["prompt"] = "Analyze the following Nsight Systems data for performance bottlenecks and resource usage:\n{data}\n\nIdentify areas that should be inspected further for bottlenecks. Suggest areas taking up the most resources and provide general optimization advice.";
        return crow::mustache::load("index.html").render(ctx);
    });

    CROW_ROUTE(app, "/analyze").methods("POST"_method)([](const crow::request& req) {
        auto multipart = crow::json::load(req.body);
        if (!multipart) {
            return crow::response(400, "Bad Request: Invalid JSON");
        }

        std::string file_content = multipart["file"]["content"];
        bool save_output = multipart["save_output"].b();
        std::string prompt = multipart["prompt"].s();

        nlohmann::json data = nlohmann::json::parse(file_content);
        std::string analysis_result = llm_analyze(data);

        std::stringstream results;
        results << "Prompt:\n" << prompt << "\n\nAnalysis Output:\n" << analysis_result;

        if (save_output) {
            std::string timestamp = get_current_timestamp();
            std::string output_folder = "nsight_llm_analyzer/output";
            std::string output_filename = "output_" + timestamp + ".txt";
            save_to_file(output_folder, output_filename, results.str());
        }

        crow::json::wvalue res;
        res["result"] = results.str();
        return crow::response(res);
    });

    app.port(8080).multithreaded().run();
    return 0;
}
