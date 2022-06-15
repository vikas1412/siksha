import datetime

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

import create_exam.question_script
from create_exam.forms import StudentRegistrationForm, NewExamForm, BatchForm
from create_exam.models import Exam, ExamQuestion, QuestionOption, UserResponse, UserInfo, ExamReport, Batch


@login_required
def home(request):
    if request.user.is_staff:
        return render(request, 'create-exam/home.html')
    else:
        return render(request, 'non-staff/exam-list.html')


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    ordering = '-timestamp'
    template_name = 'create-exam/staff/exam-batch-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = Batch.objects.all().order_by('-timestamp')
        context['new_exam_form'] = NewExamForm()
        context['batch_form'] = BatchForm()
        return context


@login_required
def view_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    all_question = ExamQuestion.objects.filter(exam_id=exam_id)
    options = QuestionOption.objects.all()
    params = {
        'exam': exam,
        'questions': all_question,
        'options': options,
    }
    return render(request, 'create-exam/exam_details.html', params)


@login_required
def bulk_upload(request, exam_id):
    create_exam.question_script.upload_new_questions(exam_id)
    return redirect(f"/exam/{exam_id}/view/")


@login_required
def delete_all(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = ExamQuestion.objects.filter(exam_id=exam)
    questions.delete()
    params = {
    }
    return redirect(f"/exam/{exam_id}/view/")


@login_required
def save_response(request):
    question_id = request.POST.get('questionId')
    selected_option_id = request.POST.get('selectedOptionId')

    question = ExamQuestion.objects.get(id=question_id)
    response = QuestionOption.objects.get(id=selected_option_id)

    user_response = UserResponse(question=question, user=request.user, selectedOption=response)
    print(user_response)
    user_response.save()

    print(question.question, "\n", response.option)

    return render(request, 'create-exam/home.html')


@login_required
def save_user_response(request):
    if request.method == 'POST':
        question_id = request.POST['questionId']
        selected_option_id = request.POST['selectedOptionId']

        question_object = ExamQuestion.objects.get(id=question_id)

        response_object = QuestionOption.objects.get(id=selected_option_id)
        # check if option selected is correct
        correct_option_object = QuestionOption.objects.filter(question=question_object)

        time_remaining = request.POST.get('timeRemaining', 'None')

        exam_obj = Exam.objects.get(id=question_object.exam.id)

        # Save remaining time after answer selected
        time_list = time_remaining.split(":")
        for i in range(len(time_list)):
            time_list[i] = int(time_list[i])
        total_sec = time_list[2] + time_list[1]*60 + time_list[0]*60*60
        duration = datetime.timedelta(days=0, seconds=int(total_sec))

        # TODO:Save time remaining to User Instance
        exam_report_obj = ExamReport.objects.filter(exam=exam_obj, user=request.user)
        if exam_report_obj.exists():
            exam_report_obj = ExamReport.objects.get(exam=exam_obj, user=request.user)
            exam_report_obj.student_exam_duration_remaining = duration

            # Check if answer is correct & thus save to db.
            # if response_object.correctness is True:
            #     exam_report_obj.correct = exam_report_obj.correct + 1
            # else:
            #     exam_report_obj.incorrect = exam_report_obj.incorrect + 1
            exam_report_obj.save()
        else:
            pass

        if_already_answered = UserResponse.objects.filter(question_id=question_object.id, user=request.user).exists()

        if if_already_answered is True:
            existing_record = UserResponse.objects.get(question_id=question_object.id, user=request.user)
            existing_record.selectedOption = response_object
            existing_record.save()
        else:
            user_response = UserResponse(question=question_object, user=request.user, selectedOption=response_object)
            user_response.save()
        return JsonResponse({'status': 'Save'})


@login_required
def save_user_info(request):
    users = User.objects.all().order_by('-id')
    params = {
        'users': users,
    }
    return render(request, 'create-exam/staff/new-user/new-user.html', params)


@login_required
def add_user(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
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


def save_new_user(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = username

        try:
            user = User.objects.get(username=username)
            messages.warning(request, "User already exist with the username you entered.")
            return JsonResponse({'status': 'exists', 'message': 'User already exists'})
        except User.DoesNotExist:
            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = fullname
            new_user.last_name = ''
            new_user.save()
            curr_user = authenticate(username=username, password=password)
            users = User.objects.values().order_by('-id')

            if curr_user is not None:
                return JsonResponse({'status': 'save', 'users': list(users)})
    else:
        return JsonResponse({'status': -1})


@login_required
def preview_one_by_one(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    all_question = ExamQuestion.objects.filter(exam_id=exam_id)
    options = QuestionOption.objects.all()

    # batch_obj = Batch.objects.get(batch=exam.batch)
    if not ExamReport.objects.filter(exam=exam, user=request.user).exists():
        new_exam_report_prepare = ExamReport(exam=exam, user=request.user, has_started=True,
                                             total_questions=all_question.count(), correct=0, incorrect=0, unattempted=0,
                                             student_exam_duration_remaining=exam.duration, has_finished=False)
        new_exam_report_prepare.save()
    params = {
        'exam': exam,
        'questions': all_question,
        'options': options,
    }
    return render(request, 'preview/preview.html', params)


def add_no_of_questions_for_ajax(exam):
    for i in range(len(exam)):
        exam_id = int(exam[i]['id'])
        exam_obj = Exam.objects.get(id=exam_id)
        total_ques = ExamQuestion.objects.filter(exam=exam_obj)
        exam[i]['no_of_questions'] = len(total_ques)


@login_required
def submit_exam(request, exam_id):
    if request.method == 'POST':
        exam = Exam.objects.get(id=exam_id)
        user_response = UserResponse.objects.filter(user=request.user)

        user = request.user.username
        has_finished = request.POST['has-finished']
        student_exam_duration = '00:30:00'
        batch = ''
        total_questions = 10
        correct = 0
        incorrect = 0
        unattempted = 0
        print(user_response)
        # batch_obj = Batch.objects.get(exam=exam)
        # user_response = UserResponse.objects.filter(user=user, batch=batch_obj)
        #
        # exam_report_object = ExamReport(exam=exam, user=user, has_finished=has_finished,
        #                                 student_exam_duration=student_exam_duration, batch=batch,
        #                                 total_questions=total_questions, correct=correct, incorrect=incorrect)

        return HttpResponse('Exam submitted.')
    else:
        return HttpResponse('Exam not submitted.')


@login_required
def new_exam(request):
    if request.method == 'POST':
        form = NewExamForm(request.POST)
        if form.is_valid():
            form.save()
            exam = Exam.objects.values().order_by('-id')

            add_no_of_questions_for_ajax(exam)

            # exams = list(Exam.objects.values().order_by('-id'))
            # for exam in range(len(exams)):
            #     exams[exam]['questions'] = 12
            #     ques = exams[exam]
            #     print(ques['questions'])
            #     for x in exams[exam]:
            #         print(x)
            #     print('\n--')

            return JsonResponse({'status': 'save', 'exam_list': list(exam)})
        else:
            return JsonResponse({'status': 0})
    else:
        return HttpResponse("Form is not post")


@login_required
def new_batch(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user1 = request.POST.get('users')
            print("***** TYPE OF USERS")
            print(type(user1))
            for x in user1:
                print(x, '----------->')
            users_added = form.cleaned_data.get('users')
            form.save()

            print("********")
            batches = list(Batch.objects.all())
            return JsonResponse({'status': 'save', 'batches': batches})
        else:
            return JsonResponse({'status': 0, 'errors': form.errors})
    else:
        print('** Not a post')
