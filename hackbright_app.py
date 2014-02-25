import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    #add this as a prompt later
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def query_for_project(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title, ))
    row = DB.fetchone()
    print """\
    Project Title: %s \n
    Project Description: %s \n
    Project Max Grade: %s""" % (row[0], row[1], row[2])

def query_for_grade(*args):
    student_github = args[0]
    project_title_tokens = args[1:]
    project_title = " ".join(project_title_tokens)
    print project_title
    query = """SELECT grade FROM Grades WHERE student_github = ? AND project_title = ?"""
    DB.execute(query, (student_github, project_title))
    row = DB.fetchone()
    print """Grade: %d """ % row[0]

def assign_grade(*args):
    student_github = args[0]
    grade = args[1]
    title_tokens = args[2:]
    project_title = " ".join(title_tokens)
    query = """INSERT INTO Grades (student_github, grade, project_title) VALUES (?,?,?)"""
    DB.execute(query, (student_github, grade, project_title))
    CONN.commit()
    print "Successfully assigned grade: %s" % (grade)
    print "Project title is: %s" % (project_title) 

def add_project(*args):
    description_list = args[1:-1]
    title = args[0]
    max_grade = args[-1]
    description = " ".join(description_list)
    print description
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?,?,?)"""
    print query
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % (title)

def get_all_grades(student_github):
    query = """SELECT project_title, grade FROM Grades WHERE student_github == ?"""
    DB.execute(query, (student_github,))
    rows = DB.fetchall()
    print rows
    return rows

def get_grades_for_project(project_title):
    query = """SELECT Grades.project_title, Students.first_name, Students.last_name, Grades.student_github, Grades.grade 
    FROM Grades JOIN Students ON (Grades.student_github=Students.github) WHERE project_title == ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    print rows
    return rows

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "query_project":
            query_for_project(*args)
        elif command == "add_project":
            add_project(*args)
        elif command == "get_grade":
            query_for_grade(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "all_grades":
            get_all_grades(*args)
        elif command == "grades_for_project":
            get_grades_for_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
