from rest_framework import viewsets
from apps.surveys.models import Questionnaire, PlantSurvey, Question, AccessToken, Answer
from apps.subscriptions.models import SubscriptionPlan, CompanySubscription, Payment
from apps.employees.models import Plant, Department, Position, Employee
from apps.users.models import Company, Role, User
from .serializers import (
    QuestionnaireSerializer, PlantSurveySerializer, QuestionSerializer,
    AccessTokenSerializer, AnswerSerializer,
    SubscriptionPlanSerializer, CompanySubscriptionSerializer, PaymentSerializer,
    PlantSerializer, DepartmentSerializer, PositionSerializer, EmployeeSerializer,
    CompanySerializer, RoleSerializer, UserSerializer
)

class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class PlantSurveyViewSet(viewsets.ModelViewSet):
    queryset = PlantSurvey.objects.all()
    serializer_class = PlantSurveySerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AccessTokenViewSet(viewsets.ModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = AccessTokenSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class CompanySubscriptionViewSet(viewsets.ModelViewSet):
    queryset = CompanySubscription.objects.all()
    serializer_class = CompanySubscriptionSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer