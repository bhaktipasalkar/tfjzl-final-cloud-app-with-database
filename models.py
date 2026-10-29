from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct and len(selected_ids) == all_answers:
            return True
        else:
            return False

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return "Enrollment: " + str(self.enrollment)
