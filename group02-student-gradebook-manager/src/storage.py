"""
Object-oriented Student Gradebook Manager with classes:
- Student, Assignment, Gradebook classes
- Inheritance for different assessment types
- Special methods for equality/printing
- Custom exceptions for invalid grades
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Union
from abc import ABC, abstractmethod
import csv
import io

# Default data file (relative to project root -> ../data/data.json)
DEFAULT_DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.json"


class InvalidGradeError(ValueError):
    """Custom exception for invalid grades"""
    pass


class DuplicateStudentIDError(ValueError):
    """Custom exception for duplicate student IDs"""
    pass


class Student:
    """Represents a student with ID and name"""
    
    def __init__(self, student_id: int, name: str):
        self.id = student_id
        self.name = name
    
    def __str__(self):
        return f"Student({self.id}: {self.name})"
    
    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}')"
    
    def __eq__(self, other):
        if isinstance(other, Student):
            return self.id == other.id and self.name == other.name
        return False
    
    def __hash__(self):
        return hash((self.id, self.name))
    
    def to_dict(self):
        return {"id": self.id, "name": self.name}
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data["id"], data["name"])


class Assignment(ABC):
    """Abstract base class for assignments"""
    
    def __init__(self, assignment_id: int, title: str, weight: float = 1.0):
        self.id = assignment_id
        self.title = title
        self.weight = weight
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.id}: {self.title}, weight={self.weight})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, title='{self.title}', weight={self.weight})"
    
    def __eq__(self, other):
        if isinstance(other, Assignment):
            return (self.id == other.id and 
                   self.title == other.title and 
                   self.weight == other.weight)
        return False
    
    def __hash__(self):
        return hash((self.id, self.title, self.weight))
    
    @abstractmethod
    def get_assignment_type(self) -> str:
        """Return the type of assignment"""
        pass
    
    def to_dict(self):
        return {
            "id": self.id, 
            "title": self.title, 
            "weight": self.weight,
            "type": self.get_assignment_type()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        assignment_type = data.get("type", "exam")
        if assignment_type == "homework":
            return HomeworkAssignment(data["id"], data["title"], data["weight"])
        elif assignment_type == "quiz":
            return QuizAssignment(data["id"], data["title"], data["weight"])
        else:
            return ExamAssignment(data["id"], data["title"], data["weight"])


class ExamAssignment(Assignment):
    """Exam assignment type"""
    
    def get_assignment_type(self) -> str:
        return "exam"


class QuizAssignment(Assignment):
    """Quiz assignment type"""
    
    def get_assignment_type(self) -> str:
        return "quiz"


class HomeworkAssignment(Assignment):
    """Homework assignment type"""
    
    def get_assignment_type(self) -> str:
        return "homework"


class Grade:
    """Represents a grade for a student on an assignment"""
    
    def __init__(self, student_id: int, assignment_id: int, score: float):
        if score < 0 or score > 100:
            raise InvalidGradeError("Score must be between 0 and 100")
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.score = score
    
    def __str__(self):
        return f"Grade(student={self.student_id}, assignment={self.assignment_id}, score={self.score})"
    
    def __repr__(self):
        return f"Grade(student_id={self.student_id}, assignment_id={self.assignment_id}, score={self.score})"
    
    def __eq__(self, other):
        if isinstance(other, Grade):
            return (self.student_id == other.student_id and 
                   self.assignment_id == other.assignment_id and 
                   self.score == other.score)
        return False
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "assignment_id": self.assignment_id,
            "score": self.score
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data["student_id"], data["assignment_id"], data["score"])


class Gradebook:
    """Main gradebook class that manages students, assignments, and grades"""
    
    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = Path(file_path or DEFAULT_DATA_FILE)
        self.students: Dict[int, Student] = {}
        self.assignments: Dict[int, Assignment] = {}
        self.grades: List[Grade] = []
        self._load_data()
    
    def _ensure_file(self):
        """Ensure data file exists with default structure"""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            default_data = {
                "students": [],
                "assignments": [],
                "grades": []
            }
            self.file_path.write_text(json.dumps(default_data, indent=2))
    
    def _load_data(self):
        """Load data from JSON file"""
        self._ensure_file()
        data = json.loads(self.file_path.read_text())
        
        # Load students
        for student_data in data.get("students", []):
            student = Student.from_dict(student_data)
            self.students[student.id] = student
        
        # Load assignments
        for assignment_data in data.get("assignments", []):
            assignment = Assignment.from_dict(assignment_data)
            self.assignments[assignment.id] = assignment
        
        # Load grades
        for grade_data in data.get("grades", []):
            grade = Grade.from_dict(grade_data)
            self.grades.append(grade)
    
    def _save_data(self):
        """Save data to JSON file"""
        data = {
            "students": [student.to_dict() for student in self.students.values()],
            "assignments": [assignment.to_dict() for assignment in self.assignments.values()],
            "grades": [grade.to_dict() for grade in self.grades]
        }
        self.file_path.write_text(json.dumps(data, indent=2))
    
    def _next_student_id(self) -> int:
        """Get next available student ID"""
        if not self.students:
            return 1
        return max(self.students.keys()) + 1
    
    def _next_assignment_id(self) -> int:
        """Get next available assignment ID"""
        if not self.assignments:
            return 1
        return max(self.assignments.keys()) + 1
    
    def add_student(self, name: str, student_id: Optional[int] = None) -> Student:
        """Add a new student with manual or auto-generated ID"""
        if student_id is None:
            student_id = self._next_student_id()
        else:
            # Check if student ID already exists
            if student_id in self.students:
                raise DuplicateStudentIDError(f"Student ID {student_id} already exists")
            
            # Validate student ID is positive
            if student_id <= 0:
                raise ValueError("Student ID must be a positive number")
        
        student = Student(student_id, name)
        self.students[student_id] = student
        self._save_data()
        return student
    
    def add_assignment(self, title: str, weight: float = 1.0, 
                      assignment_type: str = "exam") -> Assignment:
        """Add a new assignment with specified type"""
        assignment_id = self._next_assignment_id()
        
        if assignment_type.lower() == "homework":
            assignment = HomeworkAssignment(assignment_id, title, weight)
        elif assignment_type.lower() == "quiz":
            assignment = QuizAssignment(assignment_id, title, weight)
        else:
            assignment = ExamAssignment(assignment_id, title, weight)
        
        self.assignments[assignment_id] = assignment
        self._save_data()
        return assignment
    
    def add_grade(self, student_id: int, assignment_id: int, score: float) -> Grade:
        """Add or update a grade"""
        # Verify student and assignment exist
        if student_id not in self.students:
            raise ValueError("Student not found")
        if assignment_id not in self.assignments:
            raise ValueError("Assignment not found")
        
        # Remove existing grade if it exists
        self.grades = [g for g in self.grades 
                      if not (g.student_id == student_id and g.assignment_id == assignment_id)]
        
        # Add new grade
        grade = Grade(student_id, assignment_id, score)
        self.grades.append(grade)
        self._save_data()
        return grade
    
    def get_students(self) -> List[Dict]:
        """Get all students as dictionaries (for compatibility with existing templates)"""
        return [student.to_dict() for student in self.students.values()]
    
    def get_assignments(self) -> List[Dict]:
        """Get all assignments as dictionaries (for compatibility with existing templates)"""
        return [assignment.to_dict() for assignment in self.assignments.values()]
    
    def get_grades(self) -> List[Dict]:
        """Get all grades as dictionaries (for compatibility with existing templates)"""
        return [grade.to_dict() for grade in self.grades]
    
    def compute_weighted_average_for_student(self, student_id: int) -> Optional[float]:
        """Compute weighted average for a student"""
        if student_id not in self.students:
            return None
        
        student_grades = [g for g in self.grades if g.student_id == student_id]
        if not student_grades:
            return None
        
        total_weighted = 0.0
        total_weight = 0.0
        
        for grade in student_grades:
            if grade.assignment_id in self.assignments:
                assignment = self.assignments[grade.assignment_id]
                total_weighted += grade.score * assignment.weight
                total_weight += assignment.weight
        
        if total_weight == 0:
            return None
        return total_weighted / total_weight
    
    def compute_gpa_for_student(self, student_id: int) -> Optional[float]:
        """Compute GPA for a student"""
        percent = self.compute_weighted_average_for_student(student_id)
        if percent is None:
            return None
        return self.percent_to_gpa(percent)
    
    @staticmethod
    def percent_to_gpa(percent: float) -> float:
        """Convert percentage to GPA on 4.0 scale"""
        if percent >= 90:
            return 4.0
        elif percent >= 80:
            return 3.0
        elif percent >= 70:
            return 2.0
        elif percent >= 60:
            return 1.0
        return 0.0
    
    def compute_class_average(self) -> Optional[float]:
        """Compute class average"""
        if not self.students:
            return None
        
        total = 0.0
        count = 0
        
        for student_id in self.students.keys():
            avg = self.compute_weighted_average_for_student(student_id)
            if avg is not None:
                total += avg
                count += 1
        
        if count == 0:
            return None
        return total / count
    
    def export_student_csv(self, student_id: int) -> str:
        """Export student report as CSV"""
        if student_id not in self.students:
            raise ValueError("Student not found")
        
        student = self.students[student_id]
        student_grades = [g for g in self.grades if g.student_id == student_id]
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Student ID", "Student Name", student.id, student.name])
        writer.writerow([])
        writer.writerow(["Assignment ID", "Title", "Type", "Weight", "Score"])
        
        # Grades
        for grade in student_grades:
            if grade.assignment_id in self.assignments:
                assignment = self.assignments[grade.assignment_id]
                writer.writerow([
                    assignment.id, 
                    assignment.title, 
                    assignment.get_assignment_type(),
                    assignment.weight, 
                    grade.score
                ])
        
        # Summary
        avg = self.compute_weighted_average_for_student(student_id)
        gpa = self.compute_gpa_for_student(student_id)
        writer.writerow([])
        writer.writerow(["Final Weighted Average", avg if avg is not None else "N/A"])
        writer.writerow(["GPA", gpa if gpa is not None else "N/A"])
        
        return output.getvalue()


# Global gradebook instance for backward compatibility with existing Flask app
_gradebook = Gradebook()

# Functions for backward compatibility with existing Flask app
def get_students(file_path: Optional[Path] = None) -> List[Dict]:
    return _gradebook.get_students()

def get_assignments(file_path: Optional[Path] = None) -> List[Dict]:
    return _gradebook.get_assignments()

def get_grades(file_path: Optional[Path] = None) -> List[Dict]:
    return _gradebook.get_grades()

def add_student(name: str, student_id: Optional[int] = None, file_path: Optional[Path] = None) -> Dict:
    return _gradebook.add_student(name, student_id).to_dict()

def add_assignment(title: str, weight: float = 1.0, file_path: Optional[Path] = None) -> Dict:
    return _gradebook.add_assignment(title, weight).to_dict()

def add_grade(student_id: int, assignment_id: int, score: float, file_path: Optional[Path] = None) -> Dict:
    return _gradebook.add_grade(student_id, assignment_id, score).to_dict()

def compute_weighted_average_for_student(student_id: int, file_path: Optional[Path] = None) -> Optional[float]:
    return _gradebook.compute_weighted_average_for_student(student_id)

def compute_gpa_for_student(student_id: int, file_path: Optional[Path] = None) -> Optional[float]:
    return _gradebook.compute_gpa_for_student(student_id)

def compute_class_average(file_path: Optional[Path] = None) -> Optional[float]:
    return _gradebook.compute_class_average()

def export_student_csv(student_id: int, file_path: Optional[Path] = None) -> str:
    return _gradebook.export_student_csv(student_id)