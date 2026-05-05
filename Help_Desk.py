import tkinter as tk#Python library used to create graphical user interfaces
#create windows, buttons, text boxes
# -------------------- Knowledge Base (expert knowledge)--------------------
class KnowledgeBase:#Stores rules:
    def __init__(self):
        self.rules = [
            {"keywords": ["password", "login"], "solution": "Reset your password using 'Forgot Password'."},
            {"keywords": ["internet", "network"], "solution": "Restart your router or modem."},
            {"keywords": ["slow", "performance"], "solution": "Close background apps or restart your system."},
            {"keywords": ["software", "install"], "solution": "Reinstall or update the software."},
            {"keywords": ["virus", "malware"], "solution": "Run a full antivirus scan."},
            {"keywords": ["printer"], "solution": "Check printer connection and reinstall drivers."},
        ]

# -------------------- Knowledge Acquisition (adding new knowledge)--------------------
class KnowledgeAcquisition:#Used to add new rules
    def add_rule(self, kb, keywords, solution):#Makes system extendable
        #means the system can be easily improved by adding new rules without modifying the main program.
        kb.rules.append({"keywords": keywords, "solution": solution})

# -------------------- Inference Engine --------------------
class InferenceEngine:#brain Main logic/decision-making class
    def infer(self, kb, user_input):#Function to process user input
        best_match = None#Stores best rule found
        max_score = 0#Stores highest match score

        words = user_input.split()#Breaks input into words

        for rule in kb.rules:#Loop through each rule
            score = sum(1 for word in rule["keywords"] if word in words)#Counts matching keywords
            if score > max_score:#Checks if current rule is better
                max_score = score
                best_match = rule

        if best_match and max_score > 0:#If any match found
            return best_match["solution"], max_score#Return solution + score
        
        return "Issue unclear. Please contact human support.", 0

# -------------------- Explanation Module(Explains reasoning) --------------------
class ExplanationModule:
    def explain(self, score):#Takes score
        if score > 0:
            return f"Matched {score} keyword(s) from knowledge base."
        return "No relevant rule matched."#Explains how many keywords matched uperwala

# -------------------- Expert System --------------------
class ExpertSystem:#Main system class
    def __init__(self):#Constructor
        self.kb = KnowledgeBase()#Creates knowledge base
        self.ie = InferenceEngine()#Creates inference engine
        self.explainer = ExplanationModule()#Creates explanation module
        self.ka = KnowledgeAcquisition()#Creates knowledge acquisition module

    def process(self, user_input):#Main function to process input
        solution, score = self.ie.infer(self.kb, user_input)#Finds solution
        explanation = self.explainer.explain(score)#Gets explanation
        return solution, explanation

# Create system instance
system = ExpertSystem()

# -------------------- GUI Functions --------------------
def send_message(event=None):#Runs when user sends message
    user_input = entry.get().lower().strip()
    '''Gets input
 Converts to lowercase
 Removes spaces'''
    if not user_input:#If empty, do nothing
        return

    chat_box.config(state=tk.NORMAL)#Enable writing in chat box
    chat_box.insert(tk.END, "👤 You: " + user_input + "\n")#Show user message
    entry.delete(0, tk.END)

    if user_input == "exit":#Exit condition
        chat_box.insert(tk.END, "🤖 System: Session ended. Thank you!\n")
        chat_box.config(state=tk.DISABLED)
        return

    if "help" in user_input:#Show help menu
        chat_box.insert(tk.END,
            "🤖 You can ask about:\n"
            "- login/password issues\n"
            "- network/internet problems\n"
            "- system performance\n"
            "- software installation\n"
            "- printer issues\n\n")
        chat_box.config(state=tk.DISABLED)
        return

    solution, explanation = system.process(user_input)

    chat_box.insert(tk.END, "🤖 System:\n")
    chat_box.insert(tk.END, "✔️ Solution: " + solution + "\n")
    chat_box.insert(tk.END, "🧠 Reason: " + explanation + "\n\n")

    chat_box.config(state=tk.DISABLED)#Disable editing
    chat_box.yview(tk.END)#Auto-scroll to bottom

# -------------------- GUI Setup --------------------
root = tk.Tk()#Create main window
root.title("AI Help Desk Expert System")
root.geometry("450x550")#Set window size

chat_box = tk.Text(root, font=("Arial", 11), wrap=tk.WORD)#Create chat area
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_box.config(state=tk.DISABLED)#read only

chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END,
    "🤖 Welcome to the Help Desk Expert System\n"
    
    "Type your issue below 👇 or 'help' for options.\n"
    "Type 'exit' to quit.\n\n")
chat_box.config(state=tk.DISABLED)

frame = tk.Frame(root)#Create container for input
frame.pack(padx=10, pady=5, fill=tk.X)#Place frame

entry = tk.Entry(frame, font=("Arial", 12))#Input box
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))#Position input box
entry.bind("<Return>", send_message)

send_btn = tk.Button(frame, text="Send", command=send_message)#Create send button
send_btn.pack(side=tk.RIGHT)#Position button

# Run GUI
root.mainloop()
