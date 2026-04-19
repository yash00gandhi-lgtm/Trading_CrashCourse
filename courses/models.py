from django.db import models
from django.utils import timezone

class Course(models.Model):

    CATEGORY_CHOICES = [
        ('beginner', 'Beginner'),
        ('advanced', 'Advanced'),
        ('options', 'Options'),
        ('futures', 'Futures'),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)

    duration = models.CharField(max_length=100, blank=True)
    total_lessons = models.IntegerField(default=0)

    price = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)

    description = models.TextField(blank=True)

    # 🔥 NEW FIELDS
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='beginner')
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)

    # EXTRA (premium feel)
    duration = models.CharField(max_length=50, blank=True)   # e.g. "5h 30m"
    level = models.CharField(max_length=20, blank=True)      # Beginner / Advanced

    # SYSTEM
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'lesson']