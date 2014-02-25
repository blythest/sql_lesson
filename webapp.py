import hackbright_app
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/student")
def get_student_by_github():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    grades = hackbright_app.get_all_grades(student_github)

    html = render_template("student_info.html", grade_list=grades,
                                                first_name=row[0],
                                                last_name=row[1],
                                                github=row[2])
    return html

@app.route('/project/<project_title>')
def get_project_by_id(project_title):
    return "hello! %s" % project_title


@app.route("/projects")
def get_grades_for_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    rows = hackbright_app.get_grades_for_project(project_title)
    html = render_template("student_grades.html", project_titles = rows)

    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

if __name__ == "__main__":
    app.run(debug = True)