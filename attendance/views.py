from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def index(request):
    cur = connection.cursor()
    cur.execute('SELECT id, class_date, question_of_the_day FROM classes;')
    class_list = dict_fetchall(cur)

    context = {'class_list': class_list}
    return render(request, "attendance/index.html", context)


def detail(request, class_id):
    cur = connection.cursor()
    cur.execute('SELECT id, class_date, question_of_the_day FROM classes WHERE id = %s;', [class_id])
    class_data = dict_fetchone(cur)

    cur.execute("""
        SELECT s.id, s.full_name, s.aka, t.answer_of_the_day, t.status
        FROM students AS s
        JOIN attendance AS t ON t.student_id = s.id
        WHERE t.class_id = %s
        """, [class_id])
    students = dict_fetchall(cur)

    context = {'class_data': class_data, 'students': students}
    return render(request, "attendance/detail.html", context)


def create(request):
    cur = connection.cursor()
    cur.execute("SELECT s.id, s.full_name, s.aka FROM students AS s")
    students = dict_fetchall(cur)

    context = {"students": students}
    return render(request, "attendance/create.html", context)


def store(request):
    cur = connection.cursor()
    cur.execute("SELECT s.id, s.full_name, s.aka FROM students AS s")
    students = dict_fetchall(cur)

    class_date = request.POST.get('class_date')
    class_id = request.POST.get('class_id')
    question_of_the_day = request.POST.get('question_of_the_day')
    attendance = []
    for student in students:
        status = request.POST.get(student['id'] + ".status")
        answer_of_the_day = request.POST.get(student['id'] + ".answer_of_the_day")
        attendance.append({'student_id': student['id'], 'status': status, 'answer_of_the_day': answer_of_the_day})

    cur.execute("""
        INSERT INTO classes (id, class_date, question_of_the_day)
        VALUES (%s, %s, %s)
        """, [class_id, class_date, question_of_the_day])
    for a in attendance:
        cur.execute("""
            INSERT INTO attendance (class_id, student_id, status, answer_of_the_day)
            VALUES (%s, %s, %s, %s)
            """, [class_id, a['student_id'], a['status'], a['answer_of_the_day']])

    connection.commit()

    return HttpResponseRedirect(reverse("attendance:index"))


# ---


def dict_fetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row))