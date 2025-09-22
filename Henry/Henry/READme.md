# Student Gradebook Manager

A comprehensive Flask-based web application for managing student grades, assignments, and computing GPAs with role-based access control.

## Features

### Core Functionality
- **Student Management**: Add and view students
- **Assignment Management**: Create assignments with different types (Exam, Quiz, Homework) and weights
- **Grade Recording**: Record and update student grades with validation
- **GPA Calculation**: Automatic weighted average and GPA computation
- **Data Export**: Export individual student reports as CSV files
- **Class Analytics**: View class averages and statistics

### Object-Oriented Design
- **Student Class**: Represents individual students with ID and name
- **Assignment Classes**: Abstract base class with inheritance for ExamAssignment, QuizAssignment, and HomeworkAssignment
- **Grade Class**: Manages grade data with validation
- **Gradebook Class**: Main controller for all operations
- **Custom Exceptions**: InvalidGradeError for input validation

### Role-Based Access Control
- **Teacher Role**: Full access to create, read, update, and delete all data
- **Viewer Role**: Read-only access to view grades and reports
- **Dynamic Role Switching**: Switch between roles during session

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version
   # Should show Python 3.8.x or higher
   ```

2. **pip (Python package installer)**
   ```bash
   pip --version
   # Should show pip version
   ```

3. **pipenv (for virtual environment management)**
   ```bash
   pip install pipenv
   ```

## Installation Instructions

### Step 1: Download/Clone the Project
```bash
# If using git:
git clone <your-repository-url>
cd group02_studentgradebook

# If downloaded as zip:
# Extract the zip file and navigate to the project folder
cd group02_studentgradebook
```

### Step 2: Set Up Project Structure
Ensure your project has this exact structure:
```
group02_studentgradebook/
├── src/
│   ├── __init__.py          # Empty file (create if missing)
│   ├── app.py               # Main Flask application
│   └── storage.py           # Data models and storage logic
├── templates/
│   ├── layout.html          # Base template
│   ├── index.html           # Main dashboard
│   ├── students.html        # Student management
│   └── assignments.html     # Assignment management
├── static/
│   └── style.css           # Application styling
├── data/                    # Will be created automatically
│   └── data.json           # Will be created automatically
├── README.md               # This file
├── Pipfile                 # Will be created by pipenv
└── Pipfile.lock           # Will be created by pipenv
```

### Step 3: Create Virtual Environment and Install Dependencies
```bash
# Navigate to project root directory
cd group02_studentgradebook

# Create virtual environment and install Flask
pipenv install flask

# Activate the virtual environment
pipenv shell
```

### Step 4: Create Missing Files (if needed)

If any files are missing, create them:

**src/__init__.py** (empty file):
```bash
# On Windows:
type nul > src\__init__.py

# On Mac/Linux:
touch src/__init__.py
```

**data directory** (will be created automatically when app runs)

## Running the Application

### Method 1: Using pipenv (Recommended)
```bash
# Make sure you're in the project root directory
cd group02_studentgradebook

# Activate virtual environment (if not already active)
pipenv shell

# Run the application
pipenv run python -m src.app
```

### Method 2: Direct Python execution
```bash
# Make sure you're in the project root directory
cd group02_studentgradebook

# Activate virtual environment
pipenv shell

# Run the application directly
python -m src.app
```

### Expected Output
When successful, you should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * WARNING: This is a development server. Do not use it in a production deployment.
```

### Step 5: Access the Application
1. Open your web browser
2. Navigate to: `http://127.0.0.1:5000` or `http://localhost:5000`
3. You should see the Student Gradebook Manager interface

## Using the Application

### Getting Started
1. **Default Role**: You start as a "Teacher" with full editing permissions
2. **Switch Roles**: Use the role buttons in the sidebar to switch between Teacher and Viewer modes

### Teacher Mode (Full Access)
- **Add Students**: Go to "Students" page and use the form to add new students
- **Create Assignments**: Go to "Assignments" page, select type (Exam/Quiz/Homework), set title and weight
- **Record Grades**: On the main "Grades" page, select student, assignment, and enter score (0-100)
- **View Reports**: Check student summaries, class averages, and export individual CSV reports

### Viewer Mode (Read-Only)
- **View Data**: Browse all students, assignments, and grades
- **No Editing**: Forms and input fields are hidden
- **Export Only**: Can still export CSV reports for students

### Key Features
- **Grade Validation**: Scores must be between 0-100
- **Automatic Calculations**: Weighted averages and GPAs update automatically
- **Data Persistence**: All data saves to `data/data.json` automatically
- **CSV Export**: Download detailed reports for individual students

## Data Storage

The application uses a simple JSON file (`data/data.json`) to store all data. This file:
- Is created automatically on first run
- Stores students, assignments, and grades
- Updates automatically when you make changes
- Can be backed up by copying the file

## Troubleshooting

### Common Issues and Solutions

1. **"Module not found" error**
   ```bash
   # Make sure you're running from the correct directory
   cd group02_studentgradebook
   # Run with the module flag
   pipenv run python -m src.app
   ```

2. **"Template not found" error**
   - Ensure all HTML files are in the `templates/` folder
   - Check that Flask app.py has the correct template_folder path

3. **CSS not loading**
   - Ensure `style.css` is in the `static/` folder
   - Check that Flask app.py has the correct static_folder path
   - Try hard refresh (Ctrl+F5) in browser

4. **Permission errors**
   ```bash
   # Make sure pipenv is installed
   pip install pipenv
   # Try creating a new virtual environment
   pipenv --rm
   pipenv install flask
   ```

5. **Port already in use**
   - Flask default port 5000 might be busy
   - Kill other processes or restart your computer
   - Flask will automatically try port 5001, 5002, etc.

### Getting Help
- Check the browser's Developer Tools (F12) for error messages
- Look at the terminal/command prompt for Python error messages
- Ensure all files are in the correct locations as shown in the project structure

## Development Notes

### File Descriptions
- **app.py**: Main Flask application with routes and role management
- **storage.py**: Object-oriented classes for data management and persistence
- **layout.html**: Base template with navigation and role switching
- **index.html**: Main dashboard showing grades and class statistics
- **students.html**: Student management interface
- **assignments.html**: Assignment creation and management
- **style.css**: Complete styling for modern UI with role-based colors

### Technical Architecture
- **MVC Pattern**: Models (storage.py), Views (templates), Controllers (app.py routes)
- **Object-Oriented**: Uses classes with inheritance and special methods
- **Type Annotations**: Full type hints for better code quality
- **Role-Based Security**: Session-based role management
- **Responsive Design**: Mobile-friendly CSS layout

### Customization
- Modify CSS variables in `style.css` to change colors
- Add new assignment types by extending the Assignment class
- Adjust GPA scale in the `percent_to_gpa` method
- Change data storage format by modifying the Gradebook class

## Project Requirements Fulfilled

✅ **Student, Assignment, Gradebook classes with inheritance**  
✅ **Special methods for equality/printing (__str__, __repr__, __eq__)**  
✅ **Custom exceptions for invalid grades**  
✅ **CRUD operations for students and assignments**  
✅ **Grade recording and weighted average computation**  
✅ **CSV report export functionality**  
✅ **Role-based UI (Teacher vs Viewer)**  
✅ **Modern web interface with responsive design**  
✅ **Type annotations throughout codebase**  
✅ **Git-ready structure with virtual environment**

## License
This is a educational project for learning object-oriented programming and web development with Flask.