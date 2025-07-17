import random
import sqlite3
import re 
import tkinter as tk
from tkinter import PhotoImage

con = sqlite3.connect("capital.db")
cur = con.cursor()

window = tk.Tk()
window.title("GeoQuiz")
window.geometry("650x550")
window.resizable(width=False, height=False)

font_title = ("Consolas", 32, "bold")
font_subtitle = ("Consolas", 18, "bold")
font_question = ("Consolas", 15, "bold")
font_answer = ("Consolas", 15, "underline")
font_text = ("Consolas", 14)

player_name = ""
num_questions = 0
total_points = 0
questions_left = 0
current_result = []
correct_capital = ""
asked_countries = []
selected_continent = ""

img_start = PhotoImage(file="src/btn_start.png")
img_exit = PhotoImage(file="src/btn_exit.png")
img_next = PhotoImage(file="src/btn_next.png")
img_back = PhotoImage(file="src/btn_back.png")
img_restart = PhotoImage(file="src/btn_restart.png")
img_home = PhotoImage(file="src/btn_home.png")

welcome_label = tk.Label(window, text="\nWelcome to\nGeoQuiz!", font=font_title)
welcome_label.pack(pady=60)
start_button = tk.Button(window, image=img_start, command=lambda: show_name_input(), relief=tk.FLAT, bd=0)
start_button.pack(pady=10)

name_panel = tk.Frame(window)
name_label = tk.Label(name_panel, text="\n\nWhat is your name?", font=font_subtitle)
name_entry = tk.Entry(name_panel, font=font_text)
result_label = tk.Label(name_panel, text="", font=font_text)

buttons_name_frame = tk.Frame(name_panel)
next_button = tk.Button(buttons_name_frame, image=img_next, command=lambda: show_continent_selection(), relief=tk.FLAT, bd=0)
next_button.pack()

name_label.pack(pady=10)
name_entry.pack(pady=5)
result_label.pack(pady=3)
buttons_name_frame.pack(pady=(5,0))

continent_label = tk.Label(window, text="Select a continent:", font=font_subtitle)
back_button_continent = tk.Button(window, image=img_back, command=lambda: go_to_name_from_cont(), relief=tk.FLAT, bd=0)
continent_buttons = [
    tk.Button(window, text="Europe",   font=font_answer, command=lambda: select_continent("europe"), relief=tk.FLAT, bd=1),
    tk.Button(window, text="America",  font=font_answer, command=lambda: select_continent("america"), relief=tk.FLAT, bd=0),
    tk.Button(window, text="Asia",     font=font_answer, command=lambda: select_continent("asia"), relief=tk.FLAT, bd=0),
    tk.Button(window, text="Africa",   font=font_answer, command=lambda: select_continent("africa"), relief=tk.FLAT, bd=0),
    tk.Button(window, text="Oceania",  font=font_answer, command=lambda: select_continent("oceania"), relief=tk.FLAT, bd=0),
    tk.Button(window, text="All",      font=font_answer, command=lambda: select_continent("all"), relief=tk.FLAT, bd=0)
]

question_label = tk.Label(window, text="", wraplength=500, font=font_text)
question_label.pack(pady=10)
question_label.pack_forget()

option_buttons = [
    tk.Button(window, text="", font=font_answer, relief=tk.FLAT, bd=0, command=lambda i=i: check_answer(i))
    for i in range(4)
]
for btn in option_buttons:
    btn.pack(pady=5)
    btn.pack_forget()

result_game_label = tk.Label(window, text="", font=font_text)
result_game_label.pack(pady=10)

final_buttons_frame = tk.Frame(window)

restart_button = tk.Button(window, image=img_restart, command=lambda: restart_game(), relief=tk.FLAT, bd=0)
restart_button.pack_forget()

home_button = tk.Button(window, image=img_home, command=lambda: home_game(), relief=tk.FLAT, bd=0)
home_button.pack_forget()

exit_button = tk.Button(window, image=img_exit, command=window.quit, relief=tk.FLAT, bd=0)
exit_button.pack(side=tk.BOTTOM, pady=0)

result_questions_label = None
button_frame = None

def show_name_input():
    welcome_label.pack_forget()
    start_button.pack_forget()
    name_panel.pack(pady=10)
    result_label.config(text="", fg="black")
    result_game_label.config(text="")

def go_to_welcome_from_name():
    name_panel.pack_forget()
    result_label.config(text="")
    restart_button.pack_forget()
    home_button.pack_forget()
    result_game_label.config(text="")
    final_buttons_frame.pack_forget()
    welcome_label.pack(pady=60)
    start_button.pack(pady=10)

def show_continent_selection():
    global player_name
    player_name = name_entry.get()
    if not player_name.strip():
        result_label.config(text="Please enter your name.", fg="red")
        return
    if not re.match(r'^[A-Za-z]+$', player_name):
        result_label.config(text="Only letters allowed in name.\nNo spaces or symbols.", fg="red")
        return

    name_panel.pack_forget()
    result_label.config(text="", fg="black")
    continent_label.pack(pady=10)
    for btn in continent_buttons:
        btn.pack(pady=5)
    back_button_continent.pack(pady=(20,0))
    result_game_label.config(text="")
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()

def go_to_name_from_cont():
    continent_label.pack_forget()
    back_button_continent.pack_forget()
    for btn in continent_buttons:
        btn.pack_forget()
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()
    show_name_input()

def select_continent(continent):
    global selected_continent, result_questions_label, button_frame, back_button_questions
    selected_continent = continent
    continent_label.pack_forget()
    back_button_continent.pack_forget()
    for btn in continent_buttons:
        btn.pack_forget()
    questions_label = tk.Label(window, text="\n\nHow many questions do you\nwant to answer this round?", font=font_subtitle)
    questions_label.pack(pady=10)
    questions_entry = tk.Entry(window, font=font_text)
    questions_entry.pack(pady=5)
    result_questions_label = tk.Label(window, text="", font=font_text)
    result_questions_label.pack(pady=3)
    button_frame = tk.Frame(window)
    button_frame.pack(pady=(5,0))
    confirm_button = tk.Button(
        button_frame,
        image=img_next,
        command=lambda: confirm_questions(
            questions_entry, questions_label, confirm_button,
            result_questions_label, back_button_questions, button_frame),
        relief=tk.FLAT, bd=0
    )
    back_button_questions = tk.Button(
        button_frame,
        image=img_back,
        command=lambda: go_to_continent_from_questions(
            questions_label, questions_entry, result_questions_label,
            confirm_button, back_button_questions, button_frame),
        relief=tk.FLAT, bd=0
    )
    back_button_questions.pack(side=tk.LEFT, padx=2)
    confirm_button.pack(side=tk.LEFT, padx=2)
    result_game_label.config(text="")
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()

def go_to_continent_from_questions(
    questions_label, questions_entry, result_questions_label,
    confirm_button, back_button, button_frame
):
    questions_label.pack_forget()
    questions_entry.pack_forget()
    result_questions_label.pack_forget()
    confirm_button.pack_forget()
    back_button.pack_forget()
    button_frame.pack_forget()
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()
    show_continent_selection()

def confirm_questions(questions_entry, questions_label, confirm_button, result_questions_label, back_button_questions, button_frame):
    global num_questions, total_points, questions_left
    try:
        num_questions = int(questions_entry.get())
        if num_questions <= 0:
            raise ValueError
    except ValueError:
        result_questions_label.config(text="Invalid input.\nPlease enter a valid number of questions.", fg="red")
        return
    questions_label.pack_forget()
    questions_entry.pack_forget()
    confirm_button.pack_forget()
    result_questions_label.pack_forget()
    if back_button_questions: back_button_questions.pack_forget()
    if button_frame: button_frame.pack_forget()
    result_game_label.config(
        text="Instructions:\nYou have 4 options for each question, 1 is correct.\nEach correct answer earns 100 points.\nGood luck!", font=font_text, fg="black")
    question_label.pack(pady=20)
    for btn in option_buttons:
        btn.pack(pady=5)
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()
    total_points = 0
    questions_left = num_questions
    get_country()

def get_country():
    global current_result, correct_capital, questions_left, asked_countries
    if questions_left == 0:
        finish_game()
        return
    if selected_continent == "all":
        query = ('SELECT country, capital FROM (SELECT country, capital FROM europe '
                 'UNION SELECT country, capital FROM america '
                 'UNION SELECT country, capital FROM asia '
                 'UNION SELECT country, capital FROM africa '
                 'UNION SELECT country, capital FROM oceania)')
    else:
        query = f'SELECT country, capital FROM {selected_continent}'
    while True:
        current_result = cur.execute(query).fetchall()
        random.shuffle(current_result)
        country, correct_capital = current_result[0]
        if country not in asked_countries:
            asked_countries.append(country)
            break
    show_question(country)

def show_question(country):
    global correct_capital
    question_label.config(
        text=f"{questions_left} of {num_questions} questions left.\n\nWhat is the capital of {country}?",
        font=font_question
    )
    options = get_options(correct_capital)
    for i, option in enumerate(options):
        option_buttons[i].config(text=option)

def check_answer(index):
    global total_points, questions_left
    user_answer = option_buttons[index].cget('text')
    if user_answer == correct_capital:
        total_points += 100
        result_game_label.config(text=f"Correct {player_name}!\nYou earned 100 points.\nTotal points: {total_points}", fg="green")
    else:
        result_game_label.config(text=f"Incorrect {player_name}!\nThe correct answer is: {correct_capital}.\nTotal points: {total_points}", fg="red")
    questions_left -= 1
    if questions_left > 0:
        get_country()
    else:
        finish_game()

def get_options(correct_capital):
    options = [correct_capital]
    while len(options) < 4:
        random_capital = cur.execute(
            'SELECT capital FROM (SELECT capital FROM europe UNION '
            'SELECT capital FROM america UNION SELECT capital FROM asia UNION '
            'SELECT capital FROM africa UNION SELECT capital FROM oceania) '
            'ORDER BY RANDOM() LIMIT 1;').fetchone()[0]
        if random_capital not in options:
            options.append(random_capital)
    random.shuffle(options)
    return options

def finish_game():
    result_game_label.config(
        text=(f"\n\nThank you {player_name} for playing GeoQuiz.\n\n"
              f"This round: {num_questions} questions\nYour final score: {total_points} points.\n\n"
              f"Would you like to play again?\n"),
        fg="black")
    question_label.pack_forget()
    for btn in option_buttons:
        btn.pack_forget()
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()
    restart_button.pack(in_=final_buttons_frame, pady=0)
    home_button.pack(in_=final_buttons_frame, pady=0)
    final_buttons_frame.pack(pady=8)

def restart_game():
    global num_questions, total_points, questions_left, asked_countries, selected_continent
    num_questions = 0
    total_points = 0
    questions_left = 0
    asked_countries = []
    selected_continent = ""
    question_label.config(text="")
    for btn in option_buttons:
        btn.pack_forget()
    result_game_label.config(text="")
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()
    show_continent_selection()

def home_game():
    global player_name, num_questions, total_points, questions_left, asked_countries, selected_continent
    name_entry.delete(0, tk.END)
    player_name = ""
    num_questions = 0
    total_points = 0
    questions_left = 0
    asked_countries = []
    selected_continent = ""
    question_label.config(text="")
    for btn in option_buttons:
        btn.pack_forget()
    result_game_label.config(text="")
    final_buttons_frame.pack_forget()
    restart_button.pack_forget()
    home_button.pack_forget()
    welcome_label.pack(pady=60)
    start_button.pack(pady=10)

window.mainloop()
con.close()