from django.db import models
from apps.users.models import Company

class SubscriptionPlan(models.Model):
    pk_subscription_plan = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

class CompanySubscription(models.Model):
    pk_company_subscription = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

class Payment(models.Model):
    pk_payment  = models.AutoField(primary_key=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    transaction_id = models.CharField(max_length=255)
    company_subscription = models.ForeignKey(CompanySubscription, on_delete=models.CASCADE)