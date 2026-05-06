import tkinter as tk
from tkinter import messagebox#used to show error popups

#  Knowledge Base 
class KnowledgeBase:#This class stores all rules
    def __init__(self):#automatically runs when object is created
        self.rules = [#List of rules
            {
                "keywords": ["attendance", "punctual", "present", "regular", "ontime"],
                "factor": "Attendance & Punctuality",
                "solution": "Employee shows strong attendance habits. Attendance is being counted towards final rating.",
                "type": "positive"
            },
            {
                "keywords": ["target", "goal", "sales", "performance", "achieved", "met"],
                "factor": "Target Achievement",
                "solution": "Employee is meeting assigned targets. Target score is factored into final evaluation.",
                "type": "positive"
            },
            {
                "keywords": ["teamwork", "collaboration", "team", "cooperative", "helpful"],
                "factor": "Teamwork & Collaboration",
                "solution": "Employee demonstrates good team participation. Teamwork skill is noted in evaluation.",
                "type": "positive"
            },
            {
                "keywords": ["communication", "speaking", "presentation", "writing", "report"],
                "factor": "Communication Skills",
                "solution": "Employee shows effective communication. This skill positively impacts overall rating.",
                "type": "positive"
            },
            {
                "keywords": ["leadership", "initiative", "mentor", "guide", "innovate"],
                "factor": "Leadership & Initiative",
                "solution": "Employee demonstrates leadership qualities. This significantly boosts the final rating.",
                "type": "positive"
            },
            {
                "keywords": ["late", "absent", "missing", "leave", "skip"],
                "factor": "Attendance Issue Detected",
                "solution": "Frequent absences or late arrivals detected. This negatively impacts the overall rating.",
                "type": "negative"
            },
            {
                "keywords": ["complaint", "conflict", "rude", "unprofessional", "behavior"],
                "factor": "Behavioral Concern",
                "solution": "Behavioral issues detected. HR review and counseling session is recommended.",
                "type": "negative"
            },
        ]

        # Rating rules: (attendance%, targets%, teamwork_score) -> rating
        '''lambda = short function
 a = attendance
 t = targets
 w = teamwork

If condition true → rating assigned'''
        self.rating_rules = [
            {
                "condition": lambda a, t, w: a >= 90 and t >= 90 and w >= 8,
                "rating": " Outstanding",
                "recommendation": "Promote the employee and give a bonus.",
                "reason": "All three scores are at the highest level — attendance ≥ 90%, targets ≥ 90%, teamwork ≥ 8."
            },
            {
                "condition": lambda a, t, w: a >= 80 and t >= 75 and w >= 6,
                "rating": " Good",
                "recommendation": "Give the employee a salary increment.",
                "reason": "Performance is above average — attendance ≥ 80%, targets ≥ 75%, teamwork ≥ 6."
            },
            {
                "condition": lambda a, t, w: a >= 70 and t >= 60 and w >= 5,
                "rating": " Average",
                "recommendation": "Send the employee for skill development training.",
                "reason": "Scores are moderate — attendance ≥ 70%, targets ≥ 60%, teamwork ≥ 5."
            },
            {
                "condition": lambda a, t, w: True,  # fallback
                "rating": "Poor",
                "recommendation": "Issue a warning letter and schedule a performance review.",
                "reason": "One or more scores fall below the minimum acceptable threshold."
            },
        ]

# Knowledge Acquisition
class KnowledgeAcquisition:
    def add_rule(self, kb, keywords, factor, solution, rule_type="positive"):#Adds rule into knowledge base
        kb.rules.append({"keywords": keywords, "factor": factor, "solution": solution, "type": rule_type})

#  Inference Engine this is the decision-making part
class InferenceEngine:
    def infer(self, kb, user_input):#Takes user input and finds best rule
        best_match = None
        max_score = 0
        words = user_input.lower().split()#Converts input into words

        for rule in kb.rules:#Loop through all rules
            score = sum(1 for word in rule["keywords"] if word in words)#Counts matching keywords
            if score > max_score:
                max_score = score
                best_match = rule

        if best_match and max_score > 0:
            return best_match["factor"], best_match["solution"], max_score, best_match["type"]

        return "General Query", "Please mention specific performance factors like attendance, targets, teamwork, or leadership.", 0, "neutral"

    def evaluate_rating(self, kb, attendance, targets, teamwork):#Checks conditions one by one
        for rule in kb.rating_rules:
            if rule["condition"](attendance, targets, teamwork):#Executes lambda condition
                return rule["rating"], rule["recommendation"], rule["reason"]

# Explanation Module
class ExplanationModule:#Explains WHY decision was made
    def explain(self, score, rule_type):
        if score > 0:#If keywords matched
            impact = "positively" if rule_type == "positive" else "negatively"
            return f"Matched {score} keyword(s) from knowledge base. This factor impacts rating {impact}."
        return "No relevant performance rule matched."

# Expert System 
class PerformanceExpertSystem:#Combines all modules
    def __init__(self):
        self.kb = KnowledgeBase()
        self.ie = InferenceEngine()
        self.explainer = ExplanationModule()
        self.ka = KnowledgeAcquisition()

    def process(self, user_input):#Calls inference engine
        factor, solution, score, rule_type = self.ie.infer(self.kb, user_input)
        explanation = self.explainer.explain(score, rule_type)
        return factor, solution, explanation

    def get_final_rating(self, attendance, targets, teamwork):#Calls rating logic
        return self.ie.evaluate_rating(self.kb, attendance, targets, teamwork)

#  System Instance
system = PerformanceExpertSystem()

#  GUI Functions
def send_message(event=None):#Triggered when user clicks send
    user_input = entry.get().strip()#Gets input
    if not user_input:
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, " You: " + user_input + "\n")
    entry.delete(0, tk.END)

    if user_input.lower() == "exit":
        chat_box.insert(tk.END, "System: Session ended. Thank you!\n\n")
        chat_box.config(state=tk.DISABLED)
        return

    if "help" in user_input.lower():
        chat_box.insert(tk.END,
            "You can describe the employee using these keywords:\n"
            "   Positive  : attendance / punctual / target / achieved / teamwork /\n"
            "                  collaboration / communication / leadership / initiative\n"
            "    Negative  : late / absent / skip / complaint / conflict / rude\n"
            "   For Final Rating: click the 'Get Final Rating' button below.\n\n"
        )
        chat_box.config(state=tk.DISABLED)
        chat_box.yview(tk.END)
        return

    factor, solution, explanation = system.process(user_input)#Calls expert system

    chat_box.insert(tk.END, "System:\n")#Displays output
    chat_box.insert(tk.END, "    Factor     : " + factor + "\n")
    chat_box.insert(tk.END, "    Evaluation : " + solution + "\n")
    chat_box.insert(tk.END, "    Reason     : " + explanation + "\n\n")

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)


def open_rating_window():#Opens new window
    win = tk.Toplevel(root)#Creates a new child window
    win.title("Final Performance Rating")
    win.geometry("420x370")
    win.resizable(False, False)#“This ensures fixed window size.
    win.grab_set()#“It forces user to interact with this window first.
#HEADING LABELS
    tk.Label(win, text="Final Performance Rating", font=("Arial", 13, "bold")).pack(pady=(14, 2))
    tk.Label(win, text="Enter employee scores to get final verdict", font=("Arial", 9)).pack()
    tk.Label(win, text="─" * 52, font=("Arial", 9)).pack(pady=(4, 10))#Creates a separator line
    '''.pack() → places widget
 pady → vertical spacing'''
    fields_frame = tk.Frame(win)#Creates container
    fields_frame.pack(padx=20)#Adds padding horizontally
#Label for attendance, grid() → table layout , sticky="w" → left align
    tk.Label(fields_frame, text="Attendance (0–100 %)  :", font=("Arial", 11), anchor="w").grid(row=0, column=0, pady=6, sticky="w")
    att_entry = tk.Entry(fields_frame, font=("Arial", 11), width=8)#Input box for attendance
    att_entry.grid(row=0, column=1, padx=10)
#TARGET INPUT
    tk.Label(fields_frame, text="Targets Met (0–100 %) :", font=("Arial", 11), anchor="w").grid(row=1, column=0, pady=6, sticky="w")
    tgt_entry = tk.Entry(fields_frame, font=("Arial", 11), width=8)
    tgt_entry.grid(row=1, column=1, padx=10)
#TEAMWORK INPUT
    tk.Label(fields_frame, text="Teamwork Score (0–10):", font=("Arial", 11), anchor="w").grid(row=2, column=0, pady=6, sticky="w")
    team_entry = tk.Entry(fields_frame, font=("Arial", 11), width=8)
    team_entry.grid(row=2, column=1, padx=10)
#RESULT BOX
    result_box = tk.Text(win, font=("Arial", 11), height=6, wrap=tk.WORD, bd=1, relief=tk.SUNKEN, state=tk.DISABLED)
    result_box.pack(padx=16, pady=(14, 6), fill=tk.X)

    def calculate():#Converts input to numbers
        try:
            att = float(att_entry.get())#Takes attendance
            tgt = float(tgt_entry.get())#gets target percentage
            team = float(team_entry.get())#Gets teamwork score

            if not (0 <= att <= 100 and 0 <= tgt <= 100 and 0 <= team <= 10):#Validates input
                messagebox.showerror("Invalid Input", "Attendance & Targets: 0–100\nTeamwork: 0–10", parent=win)
                return

            rating, recommendation, reason = system.get_final_rating(att, tgt, team)#Gets result

            result_box.config(state=tk.NORMAL)#We enable the text box so that we can update its content
            result_box.delete("1.0", tk.END)#This clears previous results before displaying new output.
            result_box.insert(tk.END, f"  Performance Rating  : {rating}\n")
            result_box.insert(tk.END, f"  Recommendation      : {recommendation}\n")
            result_box.insert(tk.END, f"  Reasoning           : {reason}\n")
            result_box.config(state=tk.DISABLED)#Makes text box read-only again

            # Also log to main chat
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "Final Rating Result:\n")
            chat_box.insert(tk.END, f"    Performance Rating  : {rating}\n")
            chat_box.insert(tk.END, f"    Recommendation      : {recommendation}\n")
            chat_box.insert(tk.END, f"    Reasoning           : {reason}\n\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.", parent=win)

    tk.Button(win, text="  Evaluate  ", font=("Arial", 11, "bold"), command=calculate).pack(pady=4)


#  GUI Setup 
root = tk.Tk()#Main window
root.title("Employee Performance Evaluation - Expert System")
root.geometry("520x600")
root.resizable(False, False)

tk.Label(root, text="Employee Performance Evaluation", font=("Arial", 14, "bold")).pack(pady=(12, 2))
tk.Label(root, text="AI Expert System", font=("Arial", 10)).pack()
tk.Label(root, text="─" * 60, font=("Arial", 9)).pack(pady=(2, 6))

chat_box = tk.Text(root, font=("Arial", 11), wrap=tk.WORD, bd=1, relief=tk.SUNKEN)#Displays conversation
chat_box.pack(padx=12, pady=(0, 6), fill=tk.BOTH, expand=True)

chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END,
    "Welcome to the Employee Performance Expert System\n"
    "Describe an employee's performance in the input box below.\n"
    "Type 'help' to see all supported keywords.\n"
    "Click 'Get Final Rating' to enter scores and get a verdict.\n"
    "Type 'exit' to quit.\n\n"
)
chat_box.config(state=tk.DISABLED)

frame = tk.Frame(root)#Creates a container inside main window
frame.pack(padx=12, pady=(0, 6), fill=tk.X)#“Frame is used to organize input field and button in one row.

entry = tk.Entry(frame, font=("Arial", 12))#Creates text input box
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
entry.bind("<Return>", send_message)#Binds Enter key to function
entry.focus()#Cursor automatically placed in input box

tk.Button(frame, text="Send", font=("Arial", 11), command=send_message).pack(side=tk.RIGHT)#Calls function

tk.Button(root, text=" Get Final Rating", font=("Arial", 11, "bold"),
          bg="#2e7d32", fg="white", padx=10, pady=4,
          command=open_rating_window).pack(pady=(0, 10))

root.mainloop()#Mainloop keeps the application active and listens for user events.
