from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

import create_exam.question_script
from create_exam.forms import StudentRegistration
from create_exam.models import Exam, ExamQuestion, QuestionOption, UserResponse, UserInfo


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
    return render(request, 'preview/preview.html', params)


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


def save_user_response(request):
    if request.method == 'POST':
        question_id = request.POST['questionId']
        selected_option_id = request.POST['selectedOptionId']

        question_object = ExamQuestion.objects.get(id=question_id)
        response_object = QuestionOption.objects.get(id=selected_option_id)

        if_already_answered = UserResponse.objects.filter(question_id=question_object.id, user=request.user).exists()
        print(if_already_answered)
        if if_already_answered is True:
            existing_record = UserResponse.objects.get(question_id=question_object.id, user=request.user)
            existing_record.selectedOption = response_object
            existing_record.save()
        else:
            user_response = UserResponse(question=question_object, user=request.user, selectedOption=response_object)
            user_response.save()
        return JsonResponse({'status': 'Save'})


def save_user_info(request):
    users = UserInfo.objects.all().order_by('-id')
    form = StudentRegistration()
    params = {
        'users': users,
        'form': form,
    }
    return render(request, 'create_exam/user_info.html', params)


def add_user(request):
    if request.method == 'POST':
        form = StudentRegistration(request.POST)
        if form.is_valid():
            fullname = request.POST['fullname']
            email = request.POST['email']
            password = request.POST['password']
            new_user = UserInfo(fullname=fullname, email=email, password=password)
            new_user.save()
            users = UserInfo.objects.values().order_by('-id')
            return JsonResponse({'status': 'Save', 'users': list(users)})
        else:
            return JsonResponse({'status': 0})


def preview_one_by_one(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    all_question = ExamQuestion.objects.filter(exam_id=exam_id)
    options = QuestionOption.objects.all()
    params = {
        'exam': exam,
        'questions': all_question,
        'options': options,
    }
    return render(request, 'preview-one/preview.html', params)