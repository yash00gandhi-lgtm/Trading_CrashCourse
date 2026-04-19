CoreV – Trading Academy Platform

CoreV is a full-stack trading academy platform designed to deliver premium course content with secure payments and controlled user access. The goal of this project was to build something that is not just a demo, but actually usable for real clients.

The platform includes a complete authentication system with secure login, signup, and session handling. Users can browse courses, view details, and only access content after purchasing, ensuring proper access control.

Payments are integrated using Razorpay, with order creation, verification, and protection against duplicate purchases. The money flow is designed to go directly to the client’s account.

Courses are structured into lessons with smooth navigation between them. The learning experience is kept clean and distraction-free.

For video delivery, YouTube unlisted videos are used, but direct links are hidden and access is controlled through the backend to prevent misuse.

Security is a key focus in this project. Users must be logged in to access content, payments are verified before unlocking courses, and a watermark system is included for added protection.

A dashboard is provided where users can see their purchased courses and track their activity in a simple and clean interface.

The project also includes a contact system with a modern multi-step form. All submitted data is stored in the backend and can be managed through the admin panel.

Tech stack used:
Django for backend
HTML, CSS, JavaScript for frontend
Razorpay for payments
YouTube (unlisted) for video hosting
Render for deployment

Deployment process is straightforward:
Push the project to GitHub, connect it to Render, set environment variables, and deploy.

Required environment variables:
SECRET_KEY
DEBUG
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET

Important notes:
Test keys do not process real payments. Always switch to live keys before going to production. Secret keys should never be exposed in frontend code.

Project status:
Production ready
Client demo ready
Deployment ready

This project reflects practical full-stack development skills and focuses on building something usable in real-world scenarios.
