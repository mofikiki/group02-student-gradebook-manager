import pytest
from src.storage import Gradebook

def test_add_student_and_assignment(tmp_path):
    gb = Gradebook(file_path=tmp_path / "test.json")

    s = gb.add_student("Alice", 1)
    a = gb.add_assignment("Math Test", 1.0, "exam")

    assert s.id == 1
    assert s.name == "Alice"
    assert a.title == "Math Test"
    assert a.get_assignment_type() == "exam"

def test_record_and_average(tmp_path):
    gb = Gradebook(file_path=tmp_path / "test.json")

    gb.add_student("Alice", 1)
    gb.add_assignment("Math", 1.0, "exam")
    gb.add_assignment("Science", 1.0, "quiz")

    gb.add_grade(1, 1, 80)
    gb.add_grade(1, 2, 100)

    avg = gb.compute_weighted_average_for_student(1)
    gpa = gb.compute_gpa_for_student(1)

    assert avg == pytest.approx(90.0)
    assert gpa == 4.0
