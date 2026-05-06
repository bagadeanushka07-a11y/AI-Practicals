import tkinter as tk

# -------------------- Dataset --------------------
# List of student records
# list of dictionaries
students = [
    {"name": "Aarav Shah",   "marks": 92, "grade": "A", "subject": "Math",    "attendance": 95},
    {"name": "Priya Mehta",  "marks": 78, "grade": "B", "subject": "Science", "attendance": 88},
    {"name": "Rohit Verma",  "marks": 85, "grade": "A", "subject": "English", "attendance": 91},
    {"name": "Sneha Patil",  "marks": 55, "grade": "C", "subject": "Math",    "attendance": 70},
    {"name": "Karan Joshi",  "marks": 67, "grade": "B", "subject": "Science", "attendance": 80},
    {"name": "Ananya Singh", "marks": 90, "grade": "A", "subject": "English", "attendance": 97},
    {"name": "Dev Nair",     "marks": 45, "grade": "F", "subject": "Math",    "attendance": 60},
    {"name": "Meera Iyer",   "marks": 82, "grade": "A", "subject": "Science", "attendance": 85},
]


# -------------------- Knowledge Base stores all rule of expert systems 
# Stores all rules for querying student records

class KnowledgeBase:
    def __init__(self):
        self.rules = [
            {
                "id": "R01",
                "keywords": ["marks", "above", "high", "80", "good"],
                "description": "Show students with marks above 80",
                "action": lambda: [s for s in students if s["marks"] > 80]#A lambda function is a small anonymous function (function without a name).

#It is used to write short functions in a single line.
            },
            {
                "id": "R02",
                "keywords": ["marks", "below", "low", "60", "fail", "failed"],
                "description": "Show students with marks below 60",
                "action": lambda: [s for s in students if s["marks"] < 60]
            },
            {
                "id": "R03",
                "keywords": ["grade", "a", "top", "topper", "best", "excellent"],
                "description": "Show students with Grade A",
                "action": lambda: [s for s in students if s["grade"] == "A"]
            },
            {
                "id": "R04",
                "keywords": ["grade", "b"],
                "description": "Show students with Grade B",
                "action": lambda: [s for s in students if s["grade"] == "B"]
            },
            {
                "id": "R05",
                "keywords": ["attendance", "low", "poor", "less", "absent"],
                "description": "Show students with attendance below 75%",
                "action": lambda: [s for s in students if s["attendance"] < 75]
            },
            {
                "id": "R06",
                "keywords": ["attendance", "high", "good", "above", "90"],
                "description": "Show students with attendance above 90%",
                "action": lambda: [s for s in students if s["attendance"] > 90]
            },
            {
                "id": "R07",
                "keywords": ["math", "mathematics"],
                "description": "Show students studying Math",
                "action": lambda: [s for s in students if s["subject"] == "Math"]
            },
            {
                "id": "R08",
                "keywords": ["science"],
                "description": "Show students studying Science",
                "action": lambda: [s for s in students if s["subject"] == "Science"]
            },
            {
                "id": "R09",
                "keywords": ["english"],
                "description": "Show students studying English",
                "action": lambda: [s for s in students if s["subject"] == "English"]
            },
            {
                "id": "R10",
                "keywords": ["all", "list", "show", "records", "students"],
                "description": "List all student records",
                "action": lambda: students
            },
        ]


#  Knowledge Acquisition 
# Allows adding new rules at runtime

class KnowledgeAcquisition:#You can expand system without changing main code
    def add_rule(self, kb, rule_id, keywords, description, action):
        kb.rules.append({
            "id": rule_id,
            "keywords": keywords,
            "description": description,
            "action": action
        })
#learning capability of expert system

# Inference Engine 
# Matches user query to best rule using keyword scoring

class InferenceEngine:
    def infer(self, kb, user_input):
        # Convert input to lowercase and split into words
        words = user_input.lower().split()

        best_rule        = None
        best_score       = 0
        matched_keywords = []

        # Check each rule and count keyword matches
        for rule in kb.rules:
            score   = 0
            matched = []
            for keyword in rule["keywords"]:
                if keyword.lower() in words:
                    score += 1#If keyword found in input → increase score
                    matched.append(keyword)

            # Keep the rule with the highest score
            if score > best_score:
                best_score       = score
                best_rule        = rule
                matched_keywords = matched

        if best_rule and best_score > 0:
            result = best_rule["action"]()#Runs lambda function → gives filtered students
            return best_rule, result, matched_keywords, best_score

        return None, [], [], 0


# Explanation Module
# Explains why a result was returned

class ExplanationModule:
    def explain(self, rule, matched_keywords, score):
        if rule is None:
            return "No matching rule found. Type 'help' to see valid queries."

        explanation  = f"Rule ID       : {rule['id']}\n"
        explanation += f"Rule          : {rule['description']}\n"
        explanation += f"Matched Words : {', '.join(matched_keywords)}\n"#Converts list → string
        explanation += f"Match Score   : {score} keyword(s) matched"
        return explanation


# Expert System Connects everything
# Main controller connecting all modules
'''KB → rules
IE → decision maker
EM → explanation
KA → adding new rules'''
class StudentExpertSystem:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.ie = InferenceEngine()
        self.em = ExplanationModule()
        self.ka = KnowledgeAcquisition()
    '''Main pipeline:

inference engine finds rule
executes rule
generates explanation'''
    def process(self, user_input):
        rule, result, matched_keywords, score = self.ie.infer(self.kb, user_input)
        explanation = self.em.explain(rule, matched_keywords, score)
        return rule, result, explanation


#  Format Output 
# Formats student records into readable text

def format_result(result):
    if not result:
        return "No records found matching your query.\n"

    lines = [f"Found {len(result)} record(s):\n"]
    lines.append("-" * 48)
    for s in result:
        lines.append(f"  Name       : {s['name']}")
        lines.append(f"  Marks      : {s['marks']}   |   Grade      : {s['grade']}")
        lines.append(f"  Subject    : {s['subject']}   |   Attendance : {s['attendance']}%")
        lines.append("-" * 48)
    return "\n".join(lines)


#  System Instance 
system = StudentExpertSystem()


# GUI Functions 
def send_message(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "You: " + user_input + "\n")#show user message
    entry.delete(0, tk.END)

    # Handle exit command
    if user_input.lower() == "exit":
        chat_box.insert(tk.END, "System: Session ended. Goodbye!\n\n")
        chat_box.config(state=tk.DISABLED)
        return

    # Handle help command
    if user_input.lower() == "help":
        chat_box.insert(tk.END,
            "System: You can type queries like:\n"
            "   - show students with marks above 80\n"
            "   - students with low marks\n"
            "   - show grade A students\n"
            "   - show grade B students\n"
            "   - students with low attendance\n"
            "   - students with high attendance\n"
            "   - show math students\n"
            "   - show science students\n"
            "   - show english students\n"
            "   - list all students\n\n"
        )
        chat_box.config(state=tk.DISABLED)
        chat_box.yview(tk.END)
        return

    # Process query through expert system
    rule, result, explanation = system.process(user_input)

    chat_box.insert(tk.END, "System:\n")

    if rule:
        chat_box.insert(tk.END, format_result(result) + "\n\n")
        chat_box.insert(tk.END, "Explanation:\n" + explanation + "\n\n")
    else:
        chat_box.insert(tk.END, "No matching rule found. Type 'help' to see valid queries.\n\n")

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)


# -------------------- GUI Setup --------------------
root = tk.Tk()#Creates main window
root.title("Student Information Management - Expert System")
root.geometry("580x600")
root.resizable(False, False)

# Title
tk.Label(root, text="Student Information Management", font=("Arial", 14, "bold")).pack(pady=(12, 2))
tk.Label(root, text="AI Expert System", font=("Arial", 10)).pack()
tk.Label(root, text="-" * 70, font=("Arial", 9)).pack(pady=(2, 6))

# Chat box
chat_box = tk.Text(root, font=("Arial", 11), wrap=tk.WORD, bd=1, relief=tk.SUNKEN)#Displays conversation like chatbot
chat_box.pack(padx=12, pady=(0, 6), fill=tk.BOTH, expand=True)

# Welcome message
chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END,
    "Welcome to the Student Information Expert System\n"
    "Ask queries about student records.\n"
    "Type 'help' to see example queries.\n"
    "Type 'exit' to end the session.\n\n"
)
chat_box.config(state=tk.DISABLED)

# Input frame
frame = tk.Frame(root)
frame.pack(padx=12, pady=(0, 10), fill=tk.X)

entry = tk.Entry(frame, font=("Arial", 12))#User types query here
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
entry.bind("<Return>", send_message)
entry.focus()

tk.Button(frame, text="Send", font=("Arial", 11), command=send_message).pack(side=tk.RIGHT)

root.mainloop()
