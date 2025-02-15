import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import random

# --- Data Structures and Classes ---

class Task:
    """Represents a single study task."""
    def __init__(self, subject, topic, duration, priority="Medium", due_date=None):
        self.subject = subject
        self.topic = topic
        self.duration = duration  # in minutes
        self.priority = priority  # "High", "Medium", "Low"
        self.due_date = due_date  # datetime.date object

    def __str__(self):
        return f"{self.subject} - {self.topic} ({self.duration} mins, Priority: {self.priority}, Due: {self.due_date})"

class StudentProfile:
    """Stores student-specific information used for plan generation."""
    def __init__(self, goals, strengths, weaknesses, preferences, available_hours_per_day):
        self.goals = goals  # e.g., "Improve grade in Math", "Pass Biology exam"
        self.strengths = strengths  # e.g., "Good at memorization", "Strong understanding of Physics concepts"
        self.weaknesses = weaknesses  # e.g., "Struggles with Calculus", "Poor time management"
        self.preferences = preferences  # e.g., "Prefers studying in the morning", "Likes group study"
        self.available_hours_per_day = available_hours_per_day #Dict, e.g., {"Monday": 2, "Tuesday":3, ...}

# --- BERT-based Task Prioritization (Simplified Placeholder) ---
# In a real application, this would use a BERT model.
# This is a very simplified version of the concept.

def prioritize_tasks_bert(tasks, student_profile):
    """
    Prioritizes tasks based on student goals, strengths, and weaknesses
    using a simplified BERT-like approach (placeholder).
    """
    prioritized_tasks = []
    for task in tasks:
        priority = "Medium"  # Default priority

        # Increase priority if task relates to a weakness
        for weakness in student_profile.weaknesses:
            if weakness.lower() in task.topic.lower() or weakness.lower() in task.subject.lower():
                priority = "High"
                break  # Don't keep increasing priority

        # Decrease priority if task relates to a strength
        if priority == "Medium" or priority == "Low":
            for strength in student_profile.strengths:
                if strength.lower() in task.topic.lower() or strength.lower() in task.subject.lower():
                    if task.due_date and task.due_date <= datetime.date.today() + datetime.timedelta(days=2):
                        pass  # Leave priority as is if due date is urgent
                    else:
                        priority = "Low"  # Reduce priority

        task.priority = priority
        prioritized_tasks.append(task)

    # Sort tasks by priority (High > Medium > Low) and then by due date (earliest first)
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    prioritized_tasks.sort(key=lambda task: (priority_order[task.priority], task.due_date if task.due_date else datetime.date.max))
    return prioritized_tasks

# --- Study Schedule Generation ---

def generate_study_schedule(prioritized_tasks, student_profile, start_date, end_date, start_time, break_days, study_preference):
    """
    Generates a study schedule, allotting all tasks to preparation slots
    from start_date to end_date, ensuring every day has some task assigned.
    """
    schedule = {}  # {date: [list of tasks for that day]}
    current_date = start_date
    all_tasks = prioritized_tasks[:]  # Create a copy of the tasks

    while current_date <= end_date:
        if current_date.strftime("%A") in break_days:
            schedule[current_date] = ["Break Day"]
        else:
            schedule[current_date] = []
            available_time_today = student_profile.available_hours_per_day.get(current_date.strftime("%A"), 0) * 60  # Convert to minutes

            while available_time_today > 0 and all_tasks:
                # Find the task that fits in the available time
                best_task = None
                for task in all_tasks:
                    if task.duration <= available_time_today:
                        best_task = task
                        break

                if best_task:
                    schedule[current_date].append(best_task)
                    available_time_today -= best_task.duration
                    all_tasks.remove(best_task)
                else:
                    break

        current_date += datetime.timedelta(days=1)

    return schedule

# --- GUI Functions ---

def get_all_topics(subject):
    """
    Returns a list of all topics for a particular subject, ranging from 10th grade to B.Tech.
    REPLACE THIS WITH YOUR ACTUAL DATA SOURCE!
    """
    subject = subject.lower() # Converting to lowercase

    # 10th Grade Subjects
    if subject == "10th grade math":
        return ["Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables",
                "Quadratic Equations", "Arithmetic Progressions", "Triangles", "Coordinate Geometry",
                "Introduction to Trigonometry", "Some Applications of Trigonometry", "Circles",
                "Constructions", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"]
    elif subject == "10th grade science":
        return ["Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals",
                "Carbon and Its Compounds", "Periodic Classification of Elements", "Life Processes",
                "Control and Coordination", "How do Organisms Reproduce?", "Heredity and Evolution",
                "Light- Reflection and Refraction", "Human Eye and Colourful World", "Electricity",
                "Magnetic Effects of Electric Current", "Sources of Energy", "Our Environment", "Management of Natural Resources"]

    # 11th/12th Grade Subjects
    elif subject == "11th grade physics" or subject == "12th grade physics":
        return ["Units and Measurements", "Motion in a Straight Line", "Motion in a Plane", "Laws of Motion",
                "Work, Energy and Power", "System of Particles and Rotational Motion", "Gravitation",
                "Mechanical Properties of Solids", "Mechanical Properties of Fluids", "Thermal Properties of Matter",
                "Thermodynamics", "Kinetic Theory", "Oscillations", "Waves", "Electrostatic Potential and Capacitance",
                "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter", "Electromagnetic Induction",
                "Alternating Current", "Electromagnetic Waves", "Ray Optics and Optical Instruments", "Wave Optics",
                "Dual Nature of Radiation and Matter", "Atoms", "Nuclei", "Semiconductor Electronics"]
    elif subject == "11th grade math" or subject == "12th grade math":
        return ["Sets", "Relations and Functions", "Trigonometric Functions", "Principle of Mathematical Induction",
                "Complex Numbers and Quadratic Equations", "Linear Inequalities", "Permutations and Combinations",
                "Binomial Theorem", "Sequence and Series", "Straight Lines", "Conic Sections",
                "Introduction to Three Dimensional Geometry", "Limits and Derivatives", "Mathematical Reasoning",
                "Statistics", "Probability", "Relations and Functions", "Inverse Trigonometric Functions",
                "Matrices", "Determinants", "Continuity and Differentiability", "Application of Derivatives",
                "Integrals", "Application of Integrals", "Differential Equations", "Vector Algebra",
                "Three Dimensional Geometry", "Linear Programming", "Probability"]

    # B.Tech Subjects (Computer Science - Example)
    elif subject == "btech computer science":
        return ["Data Structures", "Algorithms", "Operating Systems", "Computer Networks", "Databases",
                "Software Engineering", "Artificial Intelligence", "Machine Learning", "Computer Architecture",
                "Theory of Computation", "Compiler Design", "Web Development", "Mobile App Development", "Cloud Computing",
                "Cybersecurity", "Data Mining", "Big Data Analytics", "Distributed Systems"]

    # B.Tech Subjects (Electrical Engineering - Example)
    elif subject == "btech electrical engineering":
        return ["Circuit Theory", "Signals and Systems", "Control Systems", "Electromagnetic Fields",
                "Power Systems", "Electrical Machines", "Digital Electronics", "Analog Electronics",
                "Microprocessors", "Power Electronics", "Communication Systems", "Embedded Systems", "VLSI Design"]

    # Default Topics
    else:
        return ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]

def update_topic_list(subject):
    """Updates the topic listbox with topics for the selected subject."""
    topics = get_all_topics(subject)
    topic_listbox.delete(0, tk.END)
    for topic in topics:
        topic_listbox.insert(tk.END, topic)

def generate_schedule():
    """Handles schedule generation based on user input."""
    subject = subject_entry.get()
    current_date_str = current_date_entry.get()
    exam_date_str = exam_date_entry.get()
    start_time_str = start_time_entry.get()
    break_days_str = break_days_entry.get()
    study_preference = study_preference_var.get()

    try:
        current_date = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
        exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        break_days = [day.strip() for day in break_days_str.split(',')]
    except ValueError:
        messagebox.showerror("Error", "Invalid date, time format or break days.")
        return

    # Corrected Time availability calculation
    days_until_exam = (exam_date - current_date).days
    if days_until_exam <= 0:
        messagebox.showerror("Error", "Exam date must be in the future.")
        return

    end_date = exam_date - datetime.timedelta(days=1)

    all_topics = get_all_topics(subject)

    # Display all topics in the GUI
    topic_listbox.delete(0, tk.END)
    for topic in all_topics:
        topic_listbox.insert(tk.END, topic)

    # Create Task objects from all topics
    tasks = []
    for topic in all_topics:  # Use all topics
        duration = random.randint(30, 90)  # Random duration for each topic
        tasks.append(Task(subject, topic, duration, due_date=exam_date))

    # Placeholder Student Profile
    student_profile = StudentProfile(
        goals=["Pass the exam in " + subject],
        strengths=["Good at studying"],
        weaknesses=["Procrastination"],
        preferences=["Prefers studying in the morning"],
        available_hours_per_day={"Monday": 4, "Tuesday": 4, "Wednesday": 4, "Thursday": 4, "Friday": 4, "Saturday": 4, "Sunday": 4}
    )

    # Prioritize Tasks
    prioritized_tasks = prioritize_tasks_bert(tasks, student_profile)

    # Generate Study Schedule
    study_schedule = generate_study_schedule(prioritized_tasks, student_profile, current_date, end_date, start_time, break_days, study_preference)

    # Display Schedule in GUI
    schedule_text.delete("1.0", tk.END)  # Clear previous schedule
    for date, tasks in study_schedule.items():
        schedule_text.insert(tk.END, f"\n{date.strftime('%A, %Y-%m-%d')}:\n")
        if tasks == ["Break Day"]:
            schedule_text.insert(tk.END, "  Break Day\n")
        elif tasks:
            for task in tasks:
                schedule_text.insert(tk.END, f"  - {task}\n")
        else:
            schedule_text.insert(tk.END, "  Revise previous topics.\n")

# --- GUI Setup ---
try:
    root = tk.Tk()
    root.title("Studbud AI Study Planner")
    root.configure(bg="#add8e6")  # Background color

    # --- Input Frames ---
    input_frame = ttk.Frame(root, padding=10)
    input_frame.pack()

    # Subject Input
    subject_label = ttk.Label(input_frame, text="Subject:")
    subject_label.grid(row=0, column=0, sticky=tk.W)
    subject_entry = ttk.Entry(input_frame, width=30)
    subject_entry.grid(row=0, column=1, sticky=tk.E)
    subject_entry.bind("<KeyRelease>", lambda event: update_topic_list(subject_entry.get()))  # Update topics on key release

    # Current Date Input
    current_date_label = ttk.Label(input_frame, text="Current Date (YYYY-MM-DD):")
    current_date_label.grid(row=1, column=0, sticky=tk.W)
    current_date_entry = ttk.Entry(input_frame, width=30)
    current_date_entry.grid(row=1, column=1, sticky=tk.E)

    # Exam Date Input
    exam_date_label = ttk.Label(input_frame, text="Exam Date (YYYY-MM-DD):")
    exam_date_label.grid(row=2, column=0, sticky=tk.W)
    exam_date_entry = ttk.Entry(input_frame, width=30)
    exam_date_entry.grid(row=2, column=1, sticky=tk.E)

    # Start Time Input
    start_time_label = ttk.Label(input_frame, text="Start Time (HH:MM):")
    start_time_label.grid(row=3, column=0, sticky=tk.W)
    start_time_entry = ttk.Entry(input_frame, width=30)
    start_time_entry.grid(row=3, column=1, sticky=tk.E)

    # Break Days Input
    break_days_label = ttk.Label(input_frame, text="Break Days (comma-separated):")
    break_days_label.grid(row=4, column=0, sticky=tk.W)
    break_days_entry = ttk.Entry(input_frame, width=30)
    break_days_entry.grid(row=4, column=1, sticky=tk.E)

    # Study Preference Input
    study_preference_label = ttk.Label(input_frame, text="Study Preference:")
    study_preference_label.grid(row=5, column=0, sticky=tk.W)
    study_preference_var = tk.StringVar()
    study_preference_combobox = ttk.Combobox(input_frame, textvariable=study_preference_var, width=28)
    study_preference_combobox['values'] = ("Equal Distribution", "Prioritize Difficult Topics", "Include Revision Days")
    study_preference_combobox.grid(row=5, column=1, sticky=tk.E)

    # Generate Button
    generate_button = ttk.Button(input_frame, text="Generate Schedule", command=generate_schedule, style="TButton")
    generate_button.grid(row=6, column=0, columnspan=2, pady=10)

    # --- Topic Suggestions ---
    topic_label = ttk.Label(root, text="Suggested Topics:")
    topic_label.pack()
    topic_listbox = tk.Listbox(root, width=50, height=10, bg="#e0f7fa", fg="#00796b")
    topic_listbox.pack()

    # --- Schedule Display ---
    schedule_label = ttk.Label(root, text="Study Schedule:")
    schedule_label.pack()
    schedule_text = tk.Text(root, width=60, height=15, bg="#ffccbc", fg="#d84315")
    schedule_text.pack()

    # Style configuration
    style = ttk.Style()
    style.configure("TButton", background="white")

    root.mainloop()

except tk.TclError:
    print("Error: Unable to initialize Tkinter. No display found.  Running in non-GUI mode.")
    print("Please ensure a display server is running or run this code in an environment with a GUI.")
