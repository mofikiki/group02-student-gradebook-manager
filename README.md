# Student Gradebook Manager

## Project Summary
A Python application to manage students, assignments, record grades, compute final grades, calculate class averages, and export CSV reports.

## Development Plan
As Group 2, our development plan began with a collective review of the project requirements. Each member was instructed to carefully study the specifications, after which we gathered and discussed different opinions on how best to approach the project. This ensured that every group member had a voice in shaping the development process and encouraged full participation.
Following the review, we agreed that the next step would be to divide the project into five major segments, covering all the core functionalities and deliverables. With an average of 4 active members out of 7 total, our initial strategy was to assign at least two members to each segment. This approach not only distributes the workload evenly but also provides backup and collaboration within each segment.
Project Segments
1. Core Classes & Data Models – Implementation of Student, Assignment, and Gradebook classes, with inheritance for different assessment types and special methods for equality and printing.
2. Grade Computation & GPA Logic – Weighted average calculations, GPA computation, class average calculations, and implementation of custom exceptions for invalid grades.
3. CRUD Operations – Create, Read, Update, and Delete functionality for students and assignments, along with grade entry and management.
4. GUI with Tkinter – User interface for displaying students and assignments, forms to add grades, and a summary panel for class averages.
5. Reports & Exporting – Generating reports in CSV (and optionally PDF), including student details, grades, final scores, and GPAs.
To ensure steady progress, we also adopted a strategy of staying one day ahead of schedule. This buffer allows us to handle unexpected challenges, ensure smooth integration of different parts, and stay aligned with the project deadline.
 
# Student Gradebook Manager (Group 02)

Simple tool for teachers to add students, record scores, handle weighted assignments, and compute final grades + class average. Exports per-student CSV reports.

## ✨ MVP Scope
- Add students and assignments
- Enter grades
- Compute each student’s final grade (weighted)
- Compute class average
- Export per-student CSV

## 🧱 Project Structure
├── .github/workflows/ci.yml
├── data/
├── src/
│ └── init.py
├── tests/
│ └── test_core.py
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md

