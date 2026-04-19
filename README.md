CoreV – Trading Academy Platform

CoreV is a full-stack web application designed to deliver structured trading education with secure access control, integrated payments, and a clean user experience.
The platform is built with a focus on real-world usability, scalability, and deployment readiness.

---

Overview

CoreV allows users to browse, purchase, and consume trading courses in a controlled environment.
Only verified users who have completed payments can access premium content, ensuring content protection and business integrity.

---

Key Features

Authentication System
Secure user login and session management with protected routes for authenticated access.

Course Management
Structured course and lesson system with restricted access for unpaid users.

Payment Integration
Razorpay-based payment system with order verification and duplicate purchase prevention.

Learning Experience
Smooth navigation between lessons with a clean, distraction-free interface.

Video Protection
Content is delivered using unlisted video sources with backend-controlled access, preventing direct exposure of video URLs.

Dashboard
Users can track purchased courses and monitor their learning progress through a minimal and intuitive dashboard.

Contact System
A multi-step, animated contact form integrated with the backend and accessible via the admin panel.

---

Tech Stack

Backend: Django
Frontend: HTML, CSS, JavaScript
Payments: Razorpay
Video Hosting: YouTube (Unlisted)
Deployment: Render

---

Project Structure

core/        → Project configuration
accounts/    → Authentication logic
courses/     → Course and lesson management
payments/    → Payment handling and verification
templates/   → Frontend templates
static/      → Static assets

---

Environment Configuration

The project uses environment variables for sensitive data and configuration.

Required variables:

SECRET_KEY
DEBUG
ALLOWED_HOSTS
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET

---

Deployment

The application is deployed using Render.

Steps:

1. Push code to GitHub
2. Connect repository to Render
3. Configure environment variables
4. Build and deploy

---

Notes

The free deployment tier is suitable for demonstration purposes.
For production use, it is recommended to use a paid instance along with a persistent database setup.

---

Status

The platform is fully functional and deployment-ready.
It can be directly used for client demonstration and further scaled for production usage.

---

Author

Developed with a focus on practical implementation, real-world deployment, and clean architecture.
