from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

import create_exam.question_script
from create_exam.models import Exam, ExamQuestion, QuestionOption, UserResponse, Todo


def home(request):
    return render(request, 'create_exam/index.html')


class ExamListView(ListView):
    model = Exam
    ordering = '-timestamp'


def view_exam(request, id):
    exam = Exam.objects.get(id=id)
    all_question = ExamQuestion.objects.filter(exam_id=id)
    options = QuestionOption.objects.all()

    params = {
        'exam': exam,
        'questions': all_question,
        'options': options,
    }
    return render(request, 'create_exam/exam_details.html', params)


def upload_in_bulk(request, id):
    create_exam.question_script.upload_new_questions(id)
    return redirect(f"/exam/{id}/view/")


def preview_exam(request, id):
    exam = Exam.objects.get(id=id)
    all_question = ExamQuestion.objects.filter(exam_id=id)
    options = QuestionOption.objects.all()
    params = {
        'exam': exam,
        'questions': all_question,
        'options': options,
    }
    return render(request, 'create_exam/preview-demo.html', params)


def delete_all(request, id):
    exam = Exam.objects.get(id=id)
    questions = ExamQuestion.objects.filter(exam_id=exam)
    questions.delete()
    params = {

    }
    return redirect(f"/exam/{id}/view/")


def save_response(request):
    question_id = request.POST.get('questionId')
    selected_option_id = request.POST.get('selectedOptionId')

    question = ExamQuestion.objects.get(id=question_id)
    response = QuestionOption.objects.get(id=selected_option_id)

    user_response = UserResponse(question=question, user=request.user, selectedOption=response)
    print(user_response)
    user_response.save()

    print(question.question, "\n", response.option)

    return render(request, 'create_exam/index.html')


def save_todo(request):
    if request.method == 'POST':
        task=request.POST.get('task')
        print(task)
        new = Todo(task=task)
        new.save()
    return render(request,"create_exam/checkAutoSave.html")
