from django.urls import path
from .views import  verify_payment, buy_course_page, payment_failed, payment_success

urlpatterns = [
    path('verify/', verify_payment, name='verify_payment'),
    path('buy/<int:course_id>/', buy_course_page, name='buy_course'),

    # ✅ ADD THESE
    path('success/<int:course_id>/', payment_success, name='payment_success'),
    path('failed/', payment_failed, name='payment_failed'),
]