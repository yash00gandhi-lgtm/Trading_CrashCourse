from django.urls import path
from .views import course_detail, dashboard, course_learn, courses_list,mark_complete, watch_video

urlpatterns = [
    path('courses/<int:id>/', course_detail, name='course_detail'),
    path("dashboard/", dashboard, name="dashboard"),
    path('courses/', courses_list, name='courses'),
    path('course/<slug:slug>/learn/', course_learn, name='course_learn'),
    path('mark-complete/', mark_complete, name='mark_complete'),
    path('watch/<int:lesson_id>/', watch_video, name='watch_video'),
    path('course/<slug:slug>/', course_detail, name='course_detail'),
]