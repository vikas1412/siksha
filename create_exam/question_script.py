# from create_exam.models import Exam, ExamQuestion, QuestionOption
# from bulk_questions import questions
#
#
# def upload_new_questions():
#     for i in range(len(questions['results'])):
#         ques = questions['results'][i]['question']
#         o1 = questions['results'][i]['incorrect_answers'][0]
#         o2 = questions['results'][i]['incorrect_answers'][1]
#         o3 = questions['results'][i]['incorrect_answers'][2]
#         o4 = questions['results'][i]['correct_answer']
#
#         ex = Exam.objects.all()[0]
#         new_q = ExamQuestion(exam=ex, question=ques)
#         new_q.save()
#         QuestionOption(question=new_q, option=o1).save()
#         QuestionOption(question=new_q, option=o2).save()
#         QuestionOption(question=new_q, option=o3).save()
#         QuestionOption(question=new_q, option=o4).save()
#
