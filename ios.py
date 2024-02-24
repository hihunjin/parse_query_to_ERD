import os
import json


def load_html_template(html_path: str):
    with open(html_path, "r") as f:
        html = f.read()
    return html


def save_html(html_str: str, output_path: str):
    # os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html_str)


def load_sql(sql_path: str) -> str:
    with open(sql_path, "r") as f:
        sql = f.read()
    
    return sql


def load_json(json_path):
    with open(json_path, "r") as f:
        json_data = json.load(f)
    return json_data
