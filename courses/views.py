from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Course, Lesson, LessonProgress
from payments.models import Payment


# =========================================
# 🚀 LANDING
# =========================================
def landing(request):
    courses = Course.objects.all()
    return render(request, "landing.html", {"courses": courses})


# =========================================
# 🚀 COURSE DETAIL
# =========================================
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)

    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = Payment.objects.filter(
            user=request.user,
            course=course,
            is_paid=True
        ).exists()

    return render(request, "course_detail.html", {
        "course": course,
        "is_purchased": is_purchased
    })


# =========================================
# 🚀 COURSE LEARN (FINAL 🔥)
# =========================================
@login_required(login_url='/login/')
def course_learn(request, slug):
    course = get_object_or_404(Course, slug=slug)

    # 🔒 Access Control
    if not Payment.objects.filter(
        user=request.user,
        course=course,
        is_paid=True
    ).exists():
        return redirect('course_detail', slug=course.slug)

    # 📚 Lessons (QuerySet — list nahi banayenge)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    if not lessons.exists():
        return render(request, "course_learn.html", {
            "course": course,
            "lesson": None,
            "lessons": [],
            "progress": 0,
            "prev_lesson": None,
            "next_lesson": None,
            "total_lessons": 0,
            "completed_ids": set()
        })

    # 🎯 Current lesson
    lesson_id = request.GET.get('lesson')

    if lesson_id:
        lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    else:
        lesson = lessons.first()

    # 🔁 Convert to list for navigation
    lesson_list = list(lessons)
    index = lesson_list.index(lesson)

    prev_lesson = lesson_list[index - 1] if index > 0 else None
    next_lesson = lesson_list[index + 1] if index < len(lesson_list) - 1 else None

    # ✅ Progress calculation
    completed_ids = set(
        LessonProgress.objects.filter(
            user=request.user,
            lesson__in=lesson_list,
            completed=True
        ).values_list('lesson_id', flat=True)
    )

    total = len(lesson_list)
    completed_count = len(completed_ids)

    progress = int((completed_count / total) * 100) if total > 0 else 0

    return render(request, "course_learn.html", {
        "course": course,
        "lesson": lesson,
        "lessons": lessons,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,
        "progress": progress,
        "completed_ids": completed_ids,
        "total_lessons": total   # ✅ IMPORTANT FIX
    })


# =========================================
# 🚀 MARK LESSON COMPLETE (AJAX)
# =========================================
@require_POST
@login_required
def mark_complete(request):
    lesson_id = request.POST.get("lesson_id")

    try:
        lesson = Lesson.objects.get(id=lesson_id)

        LessonProgress.objects.update_or_create(
            user=request.user,
            lesson=lesson,
            defaults={"completed": True}
        )

        return JsonResponse({"status": "ok"})

    except Lesson.DoesNotExist:
        return JsonResponse({"status": "error"}, status=400)


# =========================================
# 🚀 DASHBOARD
# =========================================
@login_required(login_url='/login/')
def dashboard(request):
    payments = Payment.objects.filter(
        user=request.user,
        is_paid=True
    ).select_related('course')

    courses = [p.course for p in payments]

    total_invested = sum(p.course.price for p in payments)

    return render(request, "dashboard.html", {
        "courses": courses,
        "payments": payments,
        "total_invested": total_invested,
        "in_progress": len(courses)
    })


# =========================================
# 🚀 ABOUT
# =========================================
def about(request):
    return render(request, 'about.html', {
        'title': 'About CoreV'
    })


# =========================================
# 🚀 COURSES LIST
# =========================================
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {
        'courses': courses
    })

@login_required
def watch_video(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # 🔒 payment check
    is_paid = Payment.objects.filter(
        user=request.user,
        course=lesson.course,
        is_paid=True
    ).exists()

    if not is_paid:
        return redirect('course_detail', slug=lesson.course.slug)

    # 👉 YouTube open
    return redirect(lesson.video_url)