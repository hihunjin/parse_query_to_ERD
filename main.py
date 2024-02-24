import os
from glob import glob

from ios import load_html_template, save_html
from parse import parse_sqls_to_template


output_path = "output"
os.makedirs(output_path, exist_ok=True)
html_template_path = os.path.join("templates", "mermaid_template.html")
html_result_path = os.path.join(output_path, "mermaid_result.html")
relations_path = "relations.json"
queries_paths = glob(os.path.join("queries", "*.sql"))
html_template = load_html_template(html_template_path)

result_html = parse_sqls_to_template(queries_paths, html_template, relations_path)
save_html(result_html, html_result_path)