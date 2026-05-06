
#   AIRLINE & CARGO SCHEDULING EXPERT SYSTEM
#   AI Practical | Python + Tkinter


import tkinter as tk#used to create GUI (window, buttons, text box).


# KNOWLEDGE BASE


knowledge_base = [#list of dictionaries storing rules.

    {
        "keywords": ["flight delayed", "departure delayed", "late flight"],
        "solution": "Flight delay detected. Rescheduling and passenger notification are recommended."
    },

    {
        "keywords": ["bad weather", "storm", "fog", "heavy rain"],
        "solution": "Weather disruption detected. Flight operations may require delay or rerouting."
    },

    {
        "keywords": ["cargo overload", "excess luggage", "overweight cargo"],
        "solution": "Cargo weight limit exceeded. Recalculate load distribution before departure."
    },

    {
        "keywords": ["crew unavailable", "pilot unavailable", "staff shortage"],
        "solution": "Crew scheduling issue detected. Assign backup crew members if available."
    },

    {
        "keywords": ["runway busy", "airport congestion", "air traffic"],
        "solution": "Airport congestion detected. Adjust landing or departure schedules."
    },

    {
        "keywords": ["fuel shortage", "low fuel", "refuelling issue"],
        "solution": "Fuel management issue detected. Verify fuel availability before scheduling."
    },

    {
        "keywords": ["maintenance required", "technical issue", "aircraft problem"],
        "solution": "Aircraft maintenance issue detected. Technical inspection is required before operation."
    },

    {
        "keywords": ["cargo missing", "lost shipment", "delivery issue"],
        "solution": "Cargo tracking issue detected. Verify shipment records and tracking information."
    },

    {
        "keywords": ["international flight", "customs issue", "documentation problem"],
        "solution": "Customs or documentation issue detected. Verify international travel documents."
    },

    {
        "keywords": ["passenger overflow", "overbooking", "full flight"],
        "solution": "Overbooking detected. Passenger reallocation or compensation may be necessary."
    },

    {
        "keywords": ["connecting flight", "missed connection", "transit delay"],
        "solution": "Transit scheduling issue detected. Rebook passengers to the next available flight."
    },

    {
        "keywords": ["cargo priority", "urgent shipment", "medical cargo"],
        "solution": "High-priority cargo detected. Schedule immediate loading and faster transportation."
    }

]

# INFERENCE ENGINE

def analyze_issue(user_input):#Function to process user input and find solution.

    user_input = user_input.lower()#Makes matching case-insensitive

    matched_solutions = []#Store matched results

    for rule in knowledge_base:#Loop through rules

        for word in rule["keywords"]:#Check each keyword

            if word in user_input:

                matched_solutions.append(rule["solution"])#Add solution and stop checking more keywords for that rule

                break

    if matched_solutions:

        return "\n\n".join(matched_solutions)#If multiple matches → show all solutions

    return "Scheduling issue could not be identified clearly. Please provide more details."

# SEND MESSAGE FUNCTION


def send_message(event=None):#Called when user clicks button or presses Enter

    user_input = entry.get().strip()

    if not user_input:
        return

    chat_box.config(state=tk.NORMAL)#Enable chat box

    chat_box.insert(#Display user message
        tk.END,
        "Operator: " + user_input + "\n\n"
    )

    result = analyze_issue(user_input)#Process input

    chat_box.insert(#Display system response
        tk.END,
        "Expert System:\n" + result + "\n\n"
    )

    entry.delete(0, tk.END)

    chat_box.config(state=tk.DISABLED)#Disable chat box (read-only)

    chat_box.yview(tk.END)#Auto-scroll

# GUI WINDOW


root = tk.Tk()#Creates main window

root.title("Airline & Cargo Scheduling Expert System")

root.geometry("700x600")

root.configure(bg="white")

# TITLE

title = tk.Label(
    root,
    text="Airline & Cargo Scheduling Expert System",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="black",
    pady=10
)

title.pack()#Displays heading of application

# CHAT BOX
# ------------------------------------------------

chat_box = tk.Text(#Where conversation appears
    root,
    font=("Arial", 11),
    wrap=tk.WORD,
    bg="#f5f5f5",
    fg="black",
    padx=10,
    pady=10
)

chat_box.pack(
    padx=10,
    pady=5,
    fill=tk.BOTH,
    expand=True
)

chat_box.insert(
    tk.END,
    "Expert System: Describe airline or cargo scheduling issues.\n"
    "Example: 'Flight delayed due to bad weather'\n\n"
)

chat_box.config(state=tk.DISABLED)#Prevents typing inside it

# INPUT FRAME

frame = tk.Frame(root, bg="white")#Holds input box + button

frame.pack(
    padx=10,
    pady=10,
    fill=tk.X
)

# ENTRY BOX

entry = tk.Entry(#User types query here
    frame,
    font=("Arial", 12),
    bg="white",
    fg="black",
    insertbackground="black"
)

entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    padx=(0, 10)
)

entry.bind("<Return>", send_message)#Press Enter → send message

entry.focus()

# SEND BUTTON

send_button = tk.Button(#Clicking button triggers analysis
    frame,
    text="Analyze",
    font=("Arial", 11),
    command=send_message
)

send_button.pack(side=tk.RIGHT)

# MAIN LOOP

root.mainloop()
