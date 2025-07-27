GitHub Push Cheat Sheet (VS Code to GitHub)
STEP 0: One-Time Setup
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
STEP 1: Navigate to Your Project Folder
cd path/to/your/project
Example:
cd C:\Users\YourName\Downloads\your_project_folder
STEP 2: Initialize Git
git init
STEP 3: Connect to Your GitHub Repo
git remote add origin https://github.com/dhamakuldeep-lab/Sukverse.git
If remote already exists:
git remote set-url origin https://github.com/dhamakuldeep-lab/Sukverse.git
STEP 4: Stage All Files
git add .
STEP 5: Commit the Changes
git commit -m "Your commit message"
Example:
git commit -m "Initial commit of Sukverse platform"
STEP 6: Push to GitHub
First time:
git branch -M main
git push -u origin main
Next time:
GitHub Push Cheat Sheet (VS Code to GitHub)
git push
Optional: Add .gitignore
Create a .gitignore file with:
__pycache__/
*.pyc
*.pyo
*.sqlite3
*.log
.env
.idea/
.vscode/
venv/
node_modules/
dist/
Then:
git add .gitignore
git commit -m "Add .gitignore"
git push
Optional: Create README.md
# Sukverse Platform
AI + Education + Healthcare microservice-based platform.
## Features
- Trainer dashboard
- Workshop module (FastAPI backend)
- React frontend
- Quiz system + progress tracking
## How to Run
- Backend: FastAPI
GitHub Push Cheat Sheet (VS Code to GitHub)
- Frontend: Vite + React
Then:
git add README.md
git commit -m "Add README"
git push