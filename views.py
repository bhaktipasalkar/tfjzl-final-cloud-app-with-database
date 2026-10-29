from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    if request.method == 'POST':
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
        
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_choice_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
            
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    earned_score = 0
    
    selected_ids = submission.choices.values_list('id', flat=True)
    
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            if question.is_get_score(selected_ids):
                earned_score += question.grade
                
    grade = (earned_score / total_score) * 100 if total_score > 0 else 0
    
    context['course'] = course
    context['grade'] = int(grade)
    context['submission'] = submission
    context['total_score'] = total_score
    context['earned_score'] = earned_score
    context['selected_ids'] = selected_ids
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
