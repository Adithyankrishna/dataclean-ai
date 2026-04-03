from flask import Flask, request, jsonify, render_template, Response
import pandas as pd
import json
import os
from groq import Groq

app = Flask(__name__)
app.secret_key = "datacleaner_secret_key_2024"

dataframes = {}

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a data cleaning assistant.
Your job is to convert user instructions into structured JSON actions for cleaning a dataset.

AVAILABLE ACTIONS:
1. remove_duplicates
2. drop_missing
3. fill_missing
4. sort
5. rename_column

ACTION FORMATS:
1. {"action": "remove_duplicates"}
2. {"action": "drop_missing", "columns": ["column_name"]}
3. {"action": "fill_missing", "column": "column_name", "method": "mean|median|mode|zero"}
4. {"action": "sort", "column": "column_name", "order": "asc|desc"}
5. {"action": "rename_column", "old_name": "old", "new_name": "new"}

OUTPUT FORMAT:
Return ONLY a valid JSON array of actions. No explanations. No markdown. No code blocks.

EXAMPLE:
User: "remove duplicates and fill missing age with median"
Output: [{"action": "remove_duplicates"}, {"action": "fill_missing", "column": "age", "method": "median"}]
"""

def apply_actions(df, actions):
    log = []
    for action in actions:
        act = action.get("action")
        try:
            if act == "remove_duplicates":
                before = len(df)
                df = df.drop_duplicates()
                log.append(f"Removed {before - len(df)} duplicate rows.")

            elif act == "drop_missing":
                cols = action.get("columns", None)
                before = len(df)
                df = df.dropna(subset=cols) if cols else df.dropna()
                log.append(f"Dropped {before - len(df)} rows with missing values.")

            elif act == "fill_missing":
                col = action.get("column")
                method = action.get("method", "mean")
                if col not in df.columns:
                    log.append(f"Column '{col}' not found.")
                    continue
                if method == "mean":
                    df[col] = df[col].fillna(df[col].mean())
                elif method == "median":
                    df[col] = df[col].fillna(df[col].median())
                elif method == "mode":
                    df[col] = df[col].fillna(df[col].mode()[0])
                elif method == "zero":
                    df[col] = df[col].fillna(0)
                log.append(f"Filled missing values in '{col}' using {method}.")

            elif act == "sort":
                col = action.get("column")
                order = action.get("order", "asc")
                if col not in df.columns:
                    log.append(f"Column '{col}' not found.")
                    continue
                df = df.sort_values(by=col, ascending=(order == "asc"))
                log.append(f"Sorted by '{col}' in {order}ending order.")

            elif act == "rename_column":
                old = action.get("old_name")
                new = action.get("new_name")
                if old not in df.columns:
                    log.append(f"Column '{old}' not found.")
                    continue
                df = df.rename(columns={old: new})
                log.append(f"Renamed column '{old}' to '{new}'.")

            else:
                log.append(f"Unknown action: {act}")

        except Exception as e:
            log.append(f"Error on action '{act}': {str(e)}")

    return df, log


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported"}), 400

    try:
        df = pd.read_csv(file)
        session_id = request.remote_addr
        dataframes[session_id] = df
        return jsonify({
            "message": f"File uploaded successfully.",
            "columns": list(df.columns),
            "shape": [len(df), len(df.columns)],
            "preview": df.head(10).fillna("").to_dict(orient="records"),
            "missing": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clean", methods=["POST"])
def clean():
    session_id = request.remote_addr
    if session_id not in dataframes:
        return jsonify({"error": "No dataset loaded. Please upload a CSV first."}), 400

    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        actions = json.loads(raw)

    except json.JSONDecodeError:
        return jsonify({"error": "LLM returned invalid JSON. Try rephrasing your prompt."}), 500
    except Exception as e:
        return jsonify({"error": f"LLM error: {str(e)}"}), 500

    df = dataframes[session_id]
    df, log = apply_actions(df, actions)
    dataframes[session_id] = df

    return jsonify({
        "message": "Cleaning applied successfully.",
        "log": log,
        "actions": actions,
        "shape": [len(df), len(df.columns)],
        "preview": df.head(10).fillna("").to_dict(orient="records"),
        "columns": list(df.columns),
        "missing": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum())
    })


@app.route("/download", methods=["GET"])
def download():
    session_id = request.remote_addr
    if session_id not in dataframes:
        return jsonify({"error": "No dataset found"}), 400

    df = dataframes[session_id]
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=cleaned_data.csv"}
    )


@app.route("/reset", methods=["POST"])
def reset():
    session_id = request.remote_addr
    if session_id in dataframes:
        del dataframes[session_id]
    return jsonify({"message": "Session reset."})


if __name__ == "__main__":
    app.run(debug=True)