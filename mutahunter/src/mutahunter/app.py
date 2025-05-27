from flask import Flask, render_template
import json
import os
import difflib

app = Flask(__name__)


def generate_diff(original_path, mutant_path):
    with open(original_path, 'r') as f1, open(mutant_path, 'r') as f2:
        original_lines = f1.readlines()
        mutant_lines = f2.readlines()

    diff = difflib.HtmlDiff().make_table(
        original_lines,
        mutant_lines,
        fromdesc='Original',
        todesc='Mutant',
        context=True,
        numlines=5
    )
    return diff

def generate_diff_1(original_path, mutant_path):
    with open(original_path, 'r') as f1, open(mutant_path, 'r') as f2:
        original_lines = f1.readlines()
        mutant_lines = f2.readlines()

    diff = difflib.HtmlDiff().make_table(
        original_lines,
        mutant_lines,
        fromdesc='Original',
        todesc='Mutant',
        context=True,
        numlines=5
    )
    return diff


@app.route('/diff/<mutant_filename>')
def show_diff(mutant_filename):
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    original_file = os.path.join(
        os.path.dirname(os.path.dirname(parent_dir)),
        "examples/java_maven/src/main/java/com/example/BankAccount.java"
    )

    mutant_folder_dir = os.path.join(
        os.path.dirname(os.path.dirname(parent_dir)),
        "examples/java_maven/logs/_latest/mutants"
    )

    mutant_file = os.path.join(mutant_folder_dir, mutant_filename)

    if not os.path.exists(mutant_file):
        return "Mutant not found", 404

    diff_html = generate_diff(original_file, mutant_file)
    return render_template('diff_view.html', diff=diff_html)


@app.route('/')
def report():
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    report_path = os.path.join(parent_dir, "report/mut_report.json")
    status_path = os.path.join(parent_dir, "report/mutant_status.json")

    mutant_folder_dir = os.path.join(
        os.path.dirname(os.path.dirname(parent_dir)),
        "examples/java_maven/logs/_latest/mutants"
    )
   

    with open(report_path) as f:
        report_data = json.load(f)

    # Convert list of {file, status} into a dict
    mutant_statuses = {}
    if os.path.exists(status_path):
        with open(status_path) as f:
            status_list = json.load(f)
            print(f"Loaded mutant statuses: {status_list}")
            mutant_statuses = {entry['file']: entry['status'] for entry in status_list}

    return render_template(
        "report.html",
        report=report_data,
        mutant_statuses=mutant_statuses
     
   )

@app.route('/view-source/<file_key>')
def view_source(file_key):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(parent_dir))

    file_map = {
        'original': os.path.join(root_dir, "examples/java_maven/src/main/java/com/example/BankAccount.java"),
        'test': os.path.join(root_dir, "examples/java_maven/src/test/java/BankAccountTest.java")
    }

    file_path = file_map.get(file_key)

    if not file_path or not os.path.exists(file_path):
        return "File not found", 404

    with open(file_path, 'r') as f:
        code = f.read()

    return render_template('source_view.html', code=code, filename=os.path.basename(file_path))


if __name__ == '__main__':
    app.run(debug=True)
