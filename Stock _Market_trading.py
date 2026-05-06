
#   STOCK MARKET TRADING EXPERT SYSTEM
#   AI Practical | Python + Tkinter

import tkinter as tk#Imports Tkinter module for creating GUI.window, buttons, text box).

# KNOWLEDGE BASE

knowledge_base = [#This is a list of rules

    {
        "keywords": ["bullish", "market rising", "uptrend", "price increasing"],
        "solution": "Bullish market trend detected. Buying opportunities may exist."
    },

    {
        "keywords": ["bearish", "market falling", "downtrend", "price dropping"],
        "solution": "Bearish market conditions detected. Trade carefully and avoid risky investments."
    },

    {
        "keywords": ["high volume", "heavy trading", "strong buying"],
        "solution": "High trading volume detected. Market momentum appears strong."
    },

    {
        "keywords": ["low volume", "weak trading"],
        "solution": "Low trading activity detected. Market signals may be unreliable."
    },

    {
        "keywords": ["strong earnings", "profit growth", "good results"],
        "solution": "Positive company performance detected. Investor confidence may increase."
    },

    {
        "keywords": ["loss", "poor earnings", "bad results"],
        "solution": "Weak financial performance detected. Investors should be cautious."
    },

    {
        "keywords": ["overvalued", "expensive stock", "overbought"],
        "solution": "Stock appears overvalued. Risk of price correction exists."
    },

    {
        "keywords": ["undervalued", "cheap stock", "oversold"],
        "solution": "Stock may be undervalued and could present investment opportunities."
    },

    {
        "keywords": ["positive news", "government support", "new contract"],
        "solution": "Positive market news detected. Market sentiment may improve."
    },

    {
        "keywords": ["negative news", "lawsuit", "scandal"],
        "solution": "Negative market sentiment detected. Investors should monitor risks carefully."
    },

    {
        "keywords": ["volatile", "market unstable", "price fluctuations"],
        "solution": "High market volatility detected. Short-term trading risk is high."
    },

    {
        "keywords": ["recession", "economic slowdown", "inflation"],
        "solution": "Economic uncertainty detected. Defensive investment strategies are recommended."
    }

]

# INFERENCE ENGINE

def analyze_market(user_input):#Function to analyze user input

    user_input = user_input.lower()#Converts input to lowercase

    matched_solutions = []#Empty list to store results

    for rule in knowledge_base:#Loop through each rule

        for word in rule["keywords"]:#Loop through keywords in that rule
            '''If match found:

Add solution to list
break avoids duplicate matches'''
            if word in user_input:

                matched_solutions.append(rule["solution"])

                break

    if matched_solutions:

        return "\n\n".join(matched_solutions)

    return "Market condition could not be analyzed clearly. Please provide more details."

# SEND MESSAGE FUNCTION

def send_message(event=None):#Handles user input and output

    user_input = entry.get().strip()#Gets text from input box

    if not user_input:#Prevents empty input
        return

    chat_box.config(state=tk.NORMAL)#Enables chat box for writing

    chat_box.insert(
        tk.END,
        "Trader: " + user_input + "\n\n"
    )#Displays user input

    result = analyze_market(user_input)#Calls inference engine

    chat_box.insert(
        tk.END,
        "Expert System:\n" + result + "\n\n"
    )#Displays system response

    entry.delete(0, tk.END)

    chat_box.config(state=tk.DISABLED)#Makes chat box read-only

    chat_box.yview(tk.END)#Auto scroll to latest message


# GUI WINDOW

root = tk.Tk()#Creates main window

root.title("Stock Market Trading Expert System")

root.geometry("700x600")

root.configure(bg="white")

# TITLE

title = tk.Label(#Displays heading text
    root,
    text="Stock Market Trading Expert System",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="black",
    pady=10
)

title.pack()#Places it on screen


# CHAT BOX

chat_box = tk.Text(#Multi-line text area for conversation
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

chat_box.insert(#Default instruction message
    tk.END,
    "Expert System: Describe current stock market conditions.\n"
    "Example: 'Market is bullish with strong earnings and high volume'\n\n"
)

chat_box.config(state=tk.DISABLED)#Makes it read-only

# INPUT FRAME
#Container for input + button
frame = tk.Frame(root, bg="white")

frame.pack(
    padx=10,
    pady=10,
    fill=tk.X
)

# ENTRY BOX

entry = tk.Entry(#Text input field
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
entry.bind("<Return>", send_message)#Press Enter to send message

entry.focus()
'''automatically places the cursor (typing pointer) inside the input box (entry) when the program starts.'''

# SEND BUTTON

send_button = tk.Button(#Button to analyze input
    frame,
    text="Analyze",
    font=("Arial", 11),
    command=send_message
)

send_button.pack(side=tk.RIGHT)

# MAIN LOOP

root.mainloop()#Runs the GUI continuously
