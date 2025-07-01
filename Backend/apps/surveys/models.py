from django.db import models
from apps.employees.models import Employee, Plant

class Questionnaire(models.Model):
    pk_questionnaire  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    creation_date = models.DateField()
    is_active = models.BooleanField(default=True)

class PlantSurvey(models.Model):
    pk_plant_survey  = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    participant_limit = models.IntegerField()
    is_active = models.BooleanField(default=True)
    evaluated_id = models.IntegerField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

class Question(models.Model):
    pk_question = models.AutoField(primary_key=True)
    question_text = models.TextField()
    question_type = models.CharField(max_length=100)
    is_required = models.BooleanField(default=True)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

class AccessToken(models.Model):
    pk_access_token  = models.AutoField(primary_key=True)
    generation_date = models.DateField()
    is_active = models.BooleanField(default=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    plant_survey = models.ForeignKey(PlantSurvey, on_delete=models.CASCADE)

class Answer(models.Model):
    pk_answer  = models.AutoField(primary_key=True)
    answer_value = models.TextField()
    answer_date = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    access_token = models.ForeignKey(AccessToken, on_delete=models.CASCADE)