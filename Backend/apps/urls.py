from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuestionnaireViewSet, PlantSurveyViewSet, QuestionViewSet,
    AccessTokenViewSet, AnswerViewSet,
    SubscriptionPlanViewSet, CompanySubscriptionViewSet, PaymentViewSet,
    PlantViewSet, DepartmentViewSet, PositionViewSet, EmployeeViewSet,
    CompanyViewSet, RoleViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'plant-surveys', PlantSurveyViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'access-tokens', AccessTokenViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'subscription-plans', SubscriptionPlanViewSet)
router.register(r'company-subscriptions', CompanySubscriptionViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'plants', PlantViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]