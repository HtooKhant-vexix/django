from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import OnlineCourse, Question, Choice, Submission, Enrollment

def course_details(request, course_id):
    course = get_object_or_404(OnlineCourse, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def submit(request, course_id):
    course = get_object_or_404(OnlineCourse, pk=course_id)
    if request.method == 'POST':
        # Get selected choice ids from request
        choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_ids.append(int(value))
            elif key == 'choice': # Handle simple radio/checkboxes if named 'choice'
                 # If multiple, getlist
                 pass
        
        # Better approach: Iterate over questions in course and check POST data
        # Assuming form sends specific choice IDs or lists
        # Let's assume the form sends 'choice_<question_id>' or similar, or just a list of 'choice'
        
        # Based on typical assignments, we might look for 'choice' as list
        choice_ids = request.POST.getlist('choice')
        
        # Create submission
        # Mock user/enrollment for now if not authenticated, or require login
        # If user is not authenticated, we can't get enrollment easily.
        # Let's assume user is superuser or we grab the first enrollment for testing
        user = request.user
        if not user.is_authenticated:
            # Fallback for testing purely logic if needed, but normally require auth
            # return redirect('login')
            pass
            
        # Try to find enrollment
        # For simplicity in this environment, create one if missing
        enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
        
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in choice_ids:
            try:
                choice = Choice.objects.get(pk=int(choice_id))
                submission.choices.add(choice)
            except Choice.DoesNotExist:
                pass
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(OnlineCourse, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate score
    total_score = 0
    # Logic: For each question in the course, check if submission choices match correct choices
    # This logic depends on Question.is_get_score implemented earlier
    
    # We can iterate over questions
    for question in course.question_set.all():
         selected_ids = [c.id for c in submission.choices.filter(question=question)]
         if question.is_get_score(selected_ids):
             total_score += question.grade

    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course,
        'submission': submission,
        'total_score': total_score
    })
