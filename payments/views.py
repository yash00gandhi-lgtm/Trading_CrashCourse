import razorpay

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from courses.models import Course
from .models import Payment


# =========================================================
# 🔌 Razorpay Client
# =========================================================
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# =========================================================
# 🚀 PAYMENT PAGE
# =========================================================
@login_required(login_url='/login/')
def buy_course_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # ✅ Already purchased → redirect
    already_paid = Payment.objects.filter(
        user=request.user,
        course=course,
        is_paid=True
    ).exists()

    if already_paid:
        return redirect('/dashboard/')

    # =====================================================
    # 🔥 Prevent duplicate orders
    # =====================================================
    payment_obj = Payment.objects.filter(
        user=request.user,
        course=course,
        is_paid=False
    ).first()

    if payment_obj:
        order_id = payment_obj.razorpay_order_id
        amount = int(course.price * 100)

    else:
        order = client.order.create({
            "amount": int(course.price * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment_obj = Payment.objects.create(
            user=request.user,
            course=course,
            razorpay_order_id=order["id"],
            is_paid=False
        )

        order_id = order["id"]
        amount = order["amount"]

    return render(request, "payment.html", {
        "course": course,
        "razorpay_key": str(settings.RAZORPAY_KEY_ID),
        "order_id": str(order_id),
        "amount": int(amount),
    })


# =========================================================
# 🔐 VERIFY PAYMENT (SECURE)
# =========================================================
@login_required(login_url='/login/')
def verify_payment(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    try:
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        if not order_id or not payment_id or not signature:
            return HttpResponseBadRequest("Missing payment data")

        # ✅ Verify signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

        # ✅ Secure fetch
        payment = Payment.objects.get(
            razorpay_order_id=order_id,
            user=request.user
        )

        # ✅ Prevent double payment update
        if payment.is_paid:
            return redirect('payment_success', course_id=payment.course.id)

        # ✅ Update DB
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.is_paid = True
        payment.save()

        return redirect('payment_success', course_id=payment.course.id)

    except Payment.DoesNotExist:
        return HttpResponseBadRequest("Payment not found")

    except Exception as e:
        print("PAYMENT ERROR:", str(e))

        Payment.objects.filter(
            razorpay_order_id=order_id,
            user=request.user
        ).update(is_paid=False)

        return redirect('payment_failed')


# =========================================================
# ✅ SUCCESS PAGE
# =========================================================
@login_required(login_url='/login/')
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    is_paid = Payment.objects.filter(
        user=request.user,
        course=course,
        is_paid=True
    ).exists()

    if not is_paid:
        return redirect('course_detail', slug=course.slug)

    return render(request, "payment_success.html", {"course": course})


# =========================================================
# ❌ FAILED PAGE
# =========================================================
@login_required(login_url='/login/')
def payment_failed(request):
    return render(request, "payment_failed.html")