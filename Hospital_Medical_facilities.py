import tkinter as tk

#  Knowledge Base 
class KnowledgeBase:#Stores all medical rules
    def __init__(self):#Constructor initializes rules
        self.rules = [#List of dictionaries
            {
                "keywords": ["fever", "cough", "cold", "chills", "sneezing"],
                "disease": "Common Cold / Flu",
                "solution": "Rest, drink fluids, take paracetamol for fever. Consult a doctor if fever exceeds 103F.",
                "severity": "Low"
            },
            {
                "keywords": ["chest", "pain", "breathless", "pressure", "arm", "sweat"],
                "disease": "Possible Cardiac Issue (Heart Attack Warning)",
                "solution": "EMERGENCY: Call 108 immediately. Chew aspirin if available. Do not drive yourself.",
                "severity": "Critical"
            },
            {
                "keywords": ["headache", "migraine", "nausea", "light", "sensitive"],
                "disease": "Migraine",
                "solution": "Rest in a dark quiet room. Take prescribed migraine medication. Avoid screens.",
                "severity": "Medium"
            },
            {
                "keywords": ["sugar", "thirst", "urination", "fatigue", "blurry", "diabetes"],
                "disease": "Possible Diabetes",
                "solution": "Monitor blood sugar levels. Consult an endocrinologist. Avoid sugary foods.",
                "severity": "Medium"
            },
            {
                "keywords": ["stomach", "vomiting", "diarrhea", "cramps", "loose"],
                "disease": "Gastroenteritis (Food Poisoning / Stomach Infection)",
                "solution": "Drink ORS solution. Avoid solid food temporarily. See a doctor if symptoms persist over 2 days.",
                "severity": "Low"
            },
            {
                "keywords": ["rash", "skin", "itching", "allergy", "hives", "swelling"],
                "disease": "Allergic Reaction / Dermatitis",
                "solution": "Take antihistamine. Avoid the allergen. Consult a dermatologist if rash spreads.",
                "severity": "Medium"
            },
            {
                "keywords": ["joint", "knee", "arthritis", "stiffness", "bone", "swollen"],
                "disease": "Arthritis / Joint Disorder",
                "solution": "Apply ice/heat pack. Take ibuprofen. Consult an orthopedic specialist.",
                "severity": "Medium"
            },
            {
                "keywords": ["unconscious", "faint", "collapse", "seizure", "fit"],
                "disease": "Neurological Emergency",
                "solution": "EMERGENCY: Call 108 immediately. Do not leave the patient alone. Place in recovery position.",
                "severity": "Critical"
            },
            {
                "keywords": ["bleeding", "wound", "cut", "injury", "blood"],
                "disease": "Physical Injury / Trauma",
                "solution": "Apply pressure to stop bleeding. Clean the wound. Visit nearest emergency ward for deep wounds.",
                "severity": "High"
            },
            {
                "keywords": ["depression", "anxiety", "stress", "mental", "sad", "sleep", "insomnia"],
                "disease": "Mental Health Concern",
                "solution": "Speak to a licensed therapist or psychiatrist. Practice mindfulness. Avoid self-medication.",
                "severity": "Medium"
            },
        ]

#Knowledge Acquisition
class KnowledgeAcquisition:
    def add_rule(self, kb, keywords, disease, solution, severity="Medium"):
        kb.rules.append({
            "keywords": keywords,
            "disease": disease,
            "solution": solution,
            "severity": severity
        })

#  Inference Engine 
class InferenceEngine:
    def infer(self, kb, user_input):#Takes user input
        best_match = None
        max_score = 0
        words = user_input.lower().split()
        for rule in kb.rules:
            score = sum(1 for word in rule["keywords"] if word in words)#Counts how many keywords match
            if score > max_score:
                max_score = score
                best_match = rule
        if best_match and max_score > 0:
            return best_match, max_score
        return None, 0

#  Explanation Module 
class ExplanationModule:#Explains decision
    def explain(self, rule, score):
        if rule and score > 0:
            return f"Matched {score} symptom keyword(s) from the knowledge base. Severity: {rule['severity']}"
        return "No matching medical rule found in the knowledge base."

#  Expert System 
class MedicalExpertSystem:#Combines everything
    def __init__(self):
        self.kb = KnowledgeBase()#Initializes all modules
        self.ie = InferenceEngine()
        self.explainer = ExplanationModule()
        self.ka = KnowledgeAcquisition()

    def process(self, user_input):#Main function
        rule, score = self.ie.infer(self.kb, user_input)#Finds best rule
        explanation = self.explainer.explain(rule, score)#Generates explanation
        if rule:
            return rule["disease"], rule["solution"], explanation
        return "Unknown Condition", "Please describe symptoms more clearly or consult a doctor.", explanation

#  Create System Instance 
system = MedicalExpertSystem()

#  GUI Functions 
def send_message(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)

    if user_input.lower() == "exit":
        chat_box.insert(tk.END, "System: Session ended. Stay healthy!\n\n")
        chat_box.config(state=tk.DISABLED)
        return

    if "help" in user_input.lower():
        chat_box.insert(tk.END,
            "System: You can describe symptoms like:\n"
            "  - fever, cough, cold\n"
            "  - chest pain, breathlessness\n"
            "  - headache, migraine\n"
            "  - stomach pain, vomiting\n"
            "  - rash, itching, allergy\n"
            "  - joint pain, stiffness\n"
            "  - bleeding, wound\n"
            "  - anxiety, depression, insomnia\n"
            "  - unconscious, seizure\n\n"
        )
        chat_box.config(state=tk.DISABLED)
        chat_box.yview(tk.END)
        return

    disease, solution, explanation = system.process(user_input.lower())#Calls expert system

    chat_box.insert(tk.END, "\nSystem:\n")
    chat_box.insert(tk.END, "  Possible Condition : " + disease + "\n")
    chat_box.insert(tk.END, "  Recommendation    : " + solution + "\n")
    chat_box.insert(tk.END, "  Reasoning         : " + explanation + "\n")
    chat_box.insert(tk.END, "-" * 55 + "\n\n")

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

# GUI Setup 
root = tk.Tk()
root.title("Medical Help Desk - Expert System")
root.geometry("550x580")
root.resizable(False, False)

# Title
tk.Label(root, text="Medical Help Desk Expert System", font=("Arial", 14, "bold")).pack(pady=(12, 2))
tk.Label(root, text="Describe your symptoms to get a preliminary assessment", font=("Arial", 9)).pack()
tk.Label(root, text="DISCLAIMER: Always consult a qualified medical professional.", font=("Arial", 8), fg="red").pack(pady=(2, 8))

# Chat Box
chat_box = tk.Text(root, font=("Arial", 10), wrap=tk.WORD, bd=1, relief=tk.SUNKEN)#Displays conversation
chat_box.pack(padx=12, pady=(0, 6), fill=tk.BOTH, expand=True)

chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END,
    "Welcome to the Medical Help Desk Expert System\n"
    + "-" * 55 + "\n"
    "Type your symptoms below or type 'help' for options.\n"
    "Type 'exit' to end the session.\n\n"
)
chat_box.config(state=tk.DISABLED)

# Input Frame
frame = tk.Frame(root)
frame.pack(padx=12, pady=(0, 10), fill=tk.X)

entry = tk.Entry(frame, font=("Arial", 11))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
entry.bind("<Return>", send_message)
entry.focus()

tk.Button(frame, text="Send", font=("Arial", 11), command=send_message).pack(side=tk.RIGHT)#Calls function on click


root.mainloop()
