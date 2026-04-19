from django.contrib import admin
from .models import Course,Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'is_free', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Lesson)