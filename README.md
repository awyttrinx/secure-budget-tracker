💸 GirlMath Budget Tracker

Empowering women to take control of their finances — one goal at a time.

⸻

🌟 Overview

The GirlMath Budget Tracker is a web application built to make financial planning, saving, and budgeting more approachable and fun — especially for women who want to understand their spending habits and start building wealth.

This project was created as part of the university modules:
	•	SE_01 – Software Development Basics
	•	SE_19 – Web Technologies Basics
	•	SE_09 – Security

It marks the foundation of a long-term personal initiative to make financial literacy and education for women more accessible and empowering.
Future versions will include educational features such as how to invest, stock market basics, and personal finance strategies.

⸻

Features

✅ User Authentication
	•	Secure registration and login via username or email.
	•	Passwords are hashed with werkzeug.security before storage.
	•	CSRF protection via Flask-WTF.
	•	Logout and session management handled with Flask-Login.

✅ Personalized Dashboard
	•	Each user has their own transactions, balance, and goals.
	•	Add, update, or delete transactions dynamically.
	•	Live balance updates — spending automatically reduces your account balance.

✅ Goal Tracking
	•	Set financial goals (e.g., “Trip to Paris” or “New Laptop”).
	•	Update your savings progress and visualize it with progress bars.
	•	Delete goals when achieved or no longer needed.

✅ Analytics Page
	•	Overview of your financial habits and transactions.
	•	Ready for future data visualizations (charts, summaries, etc.).

✅ Error Handling
	•	Custom 404 (Page Not Found) and 500 (Internal Server Error) pages for user-friendly error messages.

✅ Security Practices
	•	Form validation to prevent SQL injection and bad input.
	•	CSRF protection on all POST routes.
	•	Enforced authentication for private pages.
	•	Secure password storage with salted hashes.
	•	User-based database access (users can only access their own data).

✅ Responsive Design
	•	Fully mobile-optimized layout for smartphones and tablets.
	•	Clean and elegant UI using custom CSS and Poppins font.

⸻

##Technologies Used

Frontend:
	•	HTML5
	•	CSS3 (mobile responsive design)
	•	Jinja2 templates

Backend:
	•	Python (Flask Framework)
	•	SQLite (local database)

Security & Libraries:
	•	Flask-Login — Authentication
	•	Flask-WTF — CSRF protection
	•	Werkzeug — Password hashing
	•	SQLAlchemy — ORM for database
	•	gunicorn — Production server (for Render deployment)

Deployment:
	•	Hosted via Render.com
	•	Repository managed on GitHub

⸻

 Security & Privacy (SE_09)

The app implements several key security principles:
	•	Authentication & Authorization — users can only access their own transactions and goals.
	•	Input Validation — all form data is sanitized and type-checked.
	•	Password Hashing — no plaintext passwords are stored.
	•	CSRF Protection — all POST requests require a CSRF token.
	•	Error Handling — custom pages prevent exposure of sensitive debug info.
	•	Session Security — Flask sessions are protected with a secret key and automatic logout option.

⸻

 Mobile Optimization (SE_19)

The site is fully responsive and adjusts layout elements for mobile devices:
	•	Sidebar collapses into a top navigation bar.
	•	Text and buttons resize dynamically.
	•	Cards and forms stack vertically for easy mobile use.

⸻

🧩 Software Development Process (SE_01)

Throughout the project:
	•	Version control via Git & GitHub.
	•	Modularized Flask structure with routes, models, and templates.
	•	Code refactoring and debugging using Flask’s development server.
	•	Continuous deployment pipeline with Render (linked to GitHub).
	•	Error handling and testing with different user scenarios.

⸻

Future Plans

🚀 Phase 2:
	•	Add educational resources (articles, videos, and interactive finance tips).
	•	Introduce data visualization for analytics (using Chart.js or Plotly).
	•	Enable email verification and password reset features.
	•	Add investment tracker and financial literacy mini-courses.

⸻

Author

Antonia Wittrin
	•	🌍 Passionate about financial education & women empowerment.
	•	🎓 Project created as part of Software Engineering studies.
	•	💖 Long-term goal: Make financial literacy fun, inclusive, and powerful.
