from django.db import models
from django.conf import settings
from django.utils.timezone import now

class OnlineCourse(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    pub_date = models.DateField(default=now)
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(OnlineCourse, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'beta'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(OnlineCourse, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return "Enrollment " + str(self.id)

class Question(models.Model):
    course = models.ForeignKey(OnlineCourse, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    grade = models.FloatField(default=50.0)

    def __str__(self):
        return "Question: " + self.content[:20]

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_correct == len(selected_ids):
            return True
        else:
            return False

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
