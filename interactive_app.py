import os
import json
import openai
from flask import Flask, render_template, request, redirect, url_for
from nsight_analyzer.llm_analyze import llm_analyze
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = (
        "Analyze the following Nsight Systems data for performance bottlenecks and resource usage:\n"
        "{data}\n\n"
        "Identify areas that should be inspected further for bottlenecks. Suggest areas taking up the most resources and provide general optimization advice."
    )
    results = None

    if request.method == "POST":
        save_output = "save_output" in request.form
        prompt = request.form["prompt"]

        file = request.files["file"]
        if file:
            data = json.load(file)
            formatted_prompt = prompt.format(data=json.dumps(data, indent=2))
            analysis = llm_analyze(data)
            results = f"Prompt:\n{formatted_prompt}\n\nAnalysis Output:\n{analysis}"

            if save_output:
                output_folder = "nsight_llm_analyzer/output/"
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"output_{timestamp}_{file.filename}.txt"
                os.makedirs(output_folder, exist_ok=True)
                with open(os.path.join(output_folder, output_filename), "w") as f:
                    f.write(results)

    return render_template("index.html", prompt=prompt, results=results)

if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    app.run(debug=True)
