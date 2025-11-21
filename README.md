#💸 GirlMath Budget Tracker

Empowering women to take control of their finances.

⸻

#🌟 Overview

The GirlMath Budget Tracker is a web application built to make financial planning, saving, and budgeting more approachable and fun. Especially for women who want to understand their spending habits and start building wealth.

This project was created as part of the university modules:
	•	SE_01 – Software Development Basics
	•	SE_19 – Web Technologies Basics
	•	SE_09 – Security

It marks the foundation of a long-term personal initiative to make financial literacy and education for women more accessible and empowering.
Future versions will include educational features such as how to invest, stock market basics, and personal finance strategies.

⸻

#Features:

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

🚀 Tech Stack:
	•	Frontend: HTML, CSS (custom responsive design)
	•	Backend: Flask (Python 3.13)
	•	Database: MongoDB Atlas
	•	Hosting: Render.com
	•	Authentication: Flask-Login + Werkzeug Security
	•	CSRF-Schutz: Flask-WTF

⸻
Local Development Setup
1.Clone the Repository
git clone https://github.com/<your-username>/secure-budget-tracker.git
cd secure-budget-tracker

2.Create & Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate

3.Install Dependencies
pip install -r requirements.txt

4.Set Environment Variables
Create a .env file in your project root and add:
SECRET_KEY=your-secret-key
MONGO_URI=mongodb+srv://antoniawittrin_db_user:Musikerin911%21@cluster0.1nyxnng.mongodb.net/girlmath?retryWrites=true&w=majority&appName=Cluster0

5.Run the Application
flask run or python app.py

⸻
Deployment on Render:
1.Push your latest code to GitHub:
git add .
git commit -m "MongoDB integration and Render deployment"
git push origin main

2.Go to Render.com → Create a New Web Service
→ Connect your GitHub repository
→ Select Python 3.13 as your environment

3.Add the following Environment Variables under “Environment”:
MONGO_URI=mongodb+srv://antoniawittrin_db_user:Musikerin911%21@cluster0.1nyxnng.mongodb.net/girlmath?retryWrites=true&w=majority&appName=Cluster0
SECRET_KEY=p9zK3D7sY2hQ1vJ8tR5mN4eX6aB0cL2fW3gU8oV9pS4qT7rH1z
PYTHON_VERSION=3.13.0

4.Save and Deploy 
Render will automatically build and launch your Flask app.

⸻
##Security & Privacy:

The app implements several key security principles:
	•	Authentication & Authorization — users can only access their own transactions and goals.
	•	Input Validation — all form data is sanitized and type-checked.
	•	Password Hashing — no plaintext passwords are stored.
	•	CSRF Protection — all POST requests require a CSRF token.
	•	Error Handling — custom pages prevent exposure of sensitive debug info.
	•	Session Security — Flask sessions are protected with a secret key and automatic logout option.

⸻
##Mobile Optimization:

The site is fully responsive and adjusts layout elements for mobile devices:
	•	Sidebar collapses into a top navigation bar.
	•	Text and buttons resize dynamically.
	•	Cards and forms stack vertically for easy mobile use.

⸻


Throughout the project:
	•	Version control via Git & GitHub.
	•	Modularized Flask structure with routes, models, and templates.
	•	Code refactoring and debugging using Flask’s development server.
	•	Continuous deployment pipeline with Render (linked to GitHub).
	•	Error handling and testing with different user scenarios.

⸻

Future Plans:

🚀 Phase 2:
	•	Add educational resources (articles, videos, and interactive finance tips).
	•	Introduce data visualization for analytics (using Chart.js or Plotly).
	•	Enable email verification and password reset features.
	•	Add investment tracker and financial literacy mini-courses.

⸻

Author:

Antonia Wittrin
	•	🌍 Passionate about financial education & women empowerment.
	•	🎓 Project created as part of Software Engineering studies.
	•	💖 Long-term goal: Make financial literacy fun, inclusive, and powerful.
