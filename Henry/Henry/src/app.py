from flask import Flask, render_template, request, redirect, url_for, Response, flash, session
from pathlib import Path
from typing import Dict, Any, Optional, Union
import src.storage as storage

# Tell Flask where to find templates (one level up from src folder)
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "dev-secret-for-flask"  # for simple flash messages (change for production)

# Simple role system
ROLES: Dict[str, Dict[str, bool]] = {
    'teacher': {'can_edit': True, 'can_view': True},
    'viewer': {'can_edit': False, 'can_view': True}
}

def get_current_role() -> str:
    """Get current user role from session, default to teacher"""
    return session.get('role', 'teacher')

def can_edit() -> bool:
    """Check if current user can edit"""
    role: str = get_current_role()
    return ROLES.get(role, {}).get('can_edit', False)

def require_edit_permission() -> Optional[Response]:
    """Redirect if user doesn't have edit permissions"""
    if not can_edit():
        flash("You don't have permission to edit. Switch to teacher role.", "error")
        return redirect(url_for('index'))
    return None

@app.route("/")
def index() -> str:
    students: list[Dict[str, Any]] = storage.get_students()
    assignments: list[Dict[str, Any]] = storage.get_assignments()
    grades: list[Dict[str, Any]] = storage.get_grades()
    
    # build a table of rows: student, assignment, score
    # also compute final grades for display
    students_with_summary: list[Dict[str, Any]] = []
    for s in students:
        avg: Optional[float] = storage.compute_weighted_average_for_student(s["id"])
        gpa: Optional[float] = storage.compute_gpa_for_student(s["id"])
        students_with_summary.append({"id": s["id"], "name": s["name"], "avg": avg, "gpa": gpa})
    
    class_avg: Optional[float] = storage.compute_class_average()
    
    return render_template(
        "index.html",
        students=students,
        assignments=assignments,
        grades=grades,
        students_with_summary=students_with_summary,
        class_avg=class_avg,
        current_role=get_current_role(),
        can_edit=can_edit()
    )

@app.route("/role/<role_name>")
def switch_role(role_name: str) -> Response:
    """Switch user role"""
    if role_name in ROLES:
        session['role'] = role_name
        flash(f"Switched to {role_name} role", "success")
    else:
        flash("Invalid role", "error")
    return redirect(url_for('index'))

@app.route("/students", methods=["GET", "POST"])
def students() -> Union[str, Response]:
    if request.method == "POST":
        # Check permissions
        permission_check: Optional[Response] = require_edit_permission()
        if permission_check:
            return permission_check
            
        name: str = request.form.get("name", "").strip()
        student_id_str: str = request.form.get("student_id", "").strip()
        
        if not name:
            flash("Student name is required", "error")
            return redirect(url_for("students"))
        
        student_id: Optional[int] = None
        if student_id_str:
            try:
                student_id = int(student_id_str)
                if student_id <= 0:
                    flash("Student ID must be a positive number", "error")
                    return redirect(url_for("students"))
            except ValueError:
                flash("Student ID must be a valid number", "error")
                return redirect(url_for("students"))
        
        try:
            storage.add_student(name, student_id)
            if student_id:
                flash(f"Added student: {name} (ID: {student_id})", "success")
            else:
                flash(f"Added student: {name} (ID auto-assigned)", "success")
        except storage.DuplicateStudentIDError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Error adding student: {str(e)}", "error")
            
        return redirect(url_for("students"))
    
    all_students: list[Dict[str, Any]] = storage.get_students()
    return render_template("students.html", 
                         students=all_students,
                         current_role=get_current_role(),
                         can_edit=can_edit())

@app.route("/assignments", methods=["GET", "POST"])
def assignments() -> Union[str, Response]:
    if request.method == "POST":
        # Check permissions
        permission_check: Optional[Response] = require_edit_permission()
        if permission_check:
            return permission_check
            
        title: str = request.form.get("title", "").strip()
        weight: str = request.form.get("weight", "1").strip()
        assignment_type: str = request.form.get("type", "exam").strip().lower()
        
        try:
            w: float = float(weight)
            if not title:
                flash("Assignment title required", "error")
            else:
                # Use the new assignment type parameter
                storage._gradebook.add_assignment(title, w, assignment_type)
                flash(f"Added {assignment_type}: {title}", "success")
        except ValueError:
            flash("Weight must be a number", "error")
        return redirect(url_for("assignments"))
    
    all_assignments: list[Dict[str, Any]] = storage.get_assignments()
    return render_template("assignments.html", 
                         assignments=all_assignments,
                         current_role=get_current_role(),
                         can_edit=can_edit())

@app.route("/add_grade", methods=["POST"])
def add_grade() -> Response:
    # Check permissions
    permission_check: Optional[Response] = require_edit_permission()
    if permission_check:
        return permission_check
        
    try:
        student_id: int = int(request.form["student_id"])
        assignment_id: int = int(request.form["assignment_id"])
        score: float = float(request.form["score"])
        storage.add_grade(student_id, assignment_id, score)
        flash("Grade recorded", "success")
    except storage.InvalidGradeError as e:
        flash(str(e), "error")
    except Exception as e:
        flash("Error saving grade: " + str(e), "error")
    return redirect(url_for("index"))

@app.route("/export_csv/<int:student_id>")
def export_csv(student_id: int) -> Response:
    csv_text: str = storage.export_student_csv(student_id)
    # return as attachment
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=student_{student_id}_grades.csv"}
    )

if __name__ == "__main__":
    # Run with: pipenv run python -m src.app
    app.run(debug=True)