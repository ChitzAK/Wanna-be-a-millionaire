from tkinter import *
from tkinter import messagebox
from questions import Question
import pandas as pd
import random
import textwrap
import time
import os

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
PINK = "#e2979c"
RED = "#e7305b"
BLUE = "#7EC8E3"
GREEN = "#18A558"
BLACK = "#010100"
WHITE = "#FFFFFF"
FONT_NAME = "Bradley Hand ITC" # it can be changed to "Courier"
money_dict = {0: "$0", 1: "$100", 2: "$200", 3: "$500", 4: "$1.000", 5: "$5.000", 6: "$10.000", 7: "$50.000",
              8: "$100.000", 9: "$500.000", 10: "$1.000.000"}
columns_values = [50, 50, 400, 400]
rows_value = [400, 340, 340, 400]
MINUTES_TO_ANSWER = 2 * 60
messages = ["You saw all the questions", "You have already clicked this button before",
            "You have already clicked this button before", "The game has finished"]
titles = ["Message:", "You lost!", "Congratulations", "The voting results are: ", "Error: "]
BUTT0N_SIZE = 10
BOLD = "bold"
ITALIC = "italic"
ask_public = "Ask the public"
call_friend = "Call a friend"
half = "50_50"
button_names = {half: "50/50", "Next": "Next Question"}
card_back_file_path = os.getcwd() + "\card_back.png"

# ---------------------------- Variables ------------------------------- #
dict_from_csv = pd.read_csv("Millionaire.csv", engine='python', encoding='cp1252')
all_questions = []
all_buttons = []
percentages = []
number_of_questions = len(dict_from_csv)
user_money_amount = 0
timer = ""
counts = {ask_public: 0, call_friend: 0, half: 0}
keep_going = True
text_label = ""
count_click = 0


# ---------------------------- Functions ------------------------------- #
def get_questions():
    """
    :return: NONE. Creates a new Question object for each item from the dictionary and saves the Question into
    a list called: all_questions
    """
    for _ in range(0, number_of_questions - 1):
        question_text = dict_from_csv.loc[_, "Question text"]
        first_answer = dict_from_csv.loc[_, "First answer"]
        second_answer = dict_from_csv.loc[_, "Second answer"]
        third_answer = dict_from_csv.loc[_, "Third answer"]
        fourth_answer = dict_from_csv.loc[_, "Fourth answer"]
        correct_answer = dict_from_csv.loc[_, "Correct answer"]
        new_question = Question(question_text=question_text, first_answer=first_answer, second_answer=second_answer,
                                third_answer=third_answer, fourth_answer=fourth_answer, correct_answer=correct_answer)
        all_questions.append(new_question)


def pick_question():
    """
    :return: NONE. Picks a random Question from the list of Questions and after that, the Question is deleted
    from the all_questions list. If there are no more Questions to show, the game will stop
    """
    global number_of_questions, keep_going
    if number_of_questions > 0:
        question_number = random.randint(0, number_of_questions - 2)
        selected_question = all_questions.pop(question_number)
        number_of_questions -= 1
        return selected_question
    else:
        messagebox.askokcancel(title=titles[0], message=messages[0])
        keep_going = False


def check_answer(button_press: str, q: Question):
    """
    :param button_press: a string representing the text that is shown in the selected button
    :param q: Question object
    :return: NONE. Check's if the button_press str matches the Question's correct answer.
    If the answer is wrong, the game will stop and it will give a message.
    If the button was already clicked, it will show a message. When the button is clicked, the color will change
    into GREEN.
    """
    global user_money_amount, keep_going, click_count, count_click
    if count_click == 0:
        index = answer_options.index(button_press)
        all_buttons[index].configure(bg=GREEN)
    count_click += 1
    if q.is_correct(button_press) and user_money_amount < 10 and click_count == 0:
        user_money_amount += 1
        click_count += 1
    elif not q.is_correct(button_press):
        keep_going = False
        messagebox.askokcancel(title=titles[1], message=f"The correct answer was: {q.correct_answer}")
        reset_timer()
    elif q.is_correct(button_press) and click_count > 0:
        messagebox.askokcancel(title=titles[0], message=messages[2])
    if user_money_amount == 10:
        messagebox.askokcancel(title=titles[2], message=messages[1])
        keep_going = False


def call_half_half():
    """
    :return: NONE. Call's the half_half function. This function is created, because, the command function
    from each button, doesn't accept any parameters.
    """
    half_half(question)


def half_half(q: Question):
    """
    :param q: Question object
    :return: NONE. Colors the correct answer and one another random answer in BLUE. The remaining 2 answers,
    will be colored in RED. It can be used only one time each game and after calling it, the button is disabled
    """
    if counts[half] == 0:
        options = 0
        try:
            for _ in range(0, 4):
                if not q.is_correct(all_buttons[_].cget('text')) and options < 2:
                    all_buttons[_].config(bg=RED)
                    options += 1
                else:
                    all_buttons[_].config(bg=BLUE)
            counts[half] += 1
        except IndexError:
            messagebox.askokcancel(title=titles[4], message=messages[3])
    button_50_50["state"] = DISABLED


def generate_percentage():
    """
    :return: NONE. Generates 4 random percentages and saves them into a list called: percentages
    """
    num = 100
    first_number = random.randint(1, 70)
    num -= first_number
    percentages.append(first_number)
    second_number = random.randint(1, (num - 10))
    num -= second_number
    percentages.append(second_number)
    third_number = random.randint(1, (num - 10))
    num -= third_number
    percentages.append(third_number)
    fourth_number = 100 - first_number - second_number - third_number
    percentages.append(fourth_number)


def call_ask_the_public():
    """
    :return: NONE. Call's the ask_the_public function. This function is created, because, the command function
    from each button, doesn't accept any parameters.
    """
    ask_the_public(question)


def ask_the_public(q: Question):
    """
    :param q: Question object
    :return: NONE. Shows a messagesbox with a percentage for each answer option. It can be used only
    one time each game and after calling it, the button is disabled
    """
    if counts[ask_public] == 0:
        generate_percentage()
        answers = f"{q.first_answer}: {percentages[0]}% \n"
        answers += f"{q.second_answer}: {percentages[1]}% \n"
        answers += f"{q.third_answer}: {percentages[2]}% \n"
        answers += f"{q.fourth_answer}: {percentages[3]}% \n"
        messagebox.askokcancel(title=titles[3], message=answers)
        counts[ask_public] += 1
        ask_public_button["state"] = DISABLED


def call_a_friend():
    """
    :return: NONE. Generates a random answer from all the possible answers from a list. After that, the button
    gets disabled. It can be called only one time each game
    """
    if counts[call_friend] == 0:
        try:
            answer = random.choice(all_buttons)
            answer.config(bg=PINK)
            counts[call_friend] += 1
        except IndexError:
            messagebox.askokcancel(title=titles[4], message=messages[3])
        call_friend_button["state"] = DISABLED



def create_buttons(ans_opt: list, ques: Question):
    """
    :param ans_opt: a list, representing all the answer options from a Question object
    :param ques: Question object
    :return: NONE. Used for creating new buttons for each answer options. Each button has a
    function that will check if the answer is correct when the button is clicked
    """
    for idx, answer in enumerate(ans_opt):
        each_button = Button(window, text=ans_opt[int(idx)], anchor=W,
                             command=lambda m=ans_opt[int(idx)], q=ques: check_answer(m, q))
        each_button.configure(width=37, height=2, font=(FONT_NAME, BUTT0N_SIZE, BOLD))
        canvas.create_window(columns_values[int(idx)], rows_value[int(idx)], anchor=NW, window=each_button)
        all_buttons.append(each_button)


def count_down(count: int):
    """
    :param count: an integer, representing the number of minutes, ex: 2*60
    :return: NONE. This function will count down from the number of minutes, until it reaches 00:00
    """
    time_format = time.strftime("%M:%S", time.gmtime(count))
    canvas.itemconfig(timer_text, text=time_format)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)


def wrap_text(q: Question):
    """
    :param q: takes a Question as an input
    :return: the Question text, separated by a new line after each 45 characters
    """
    return "\n".join(textwrap.wrap(q.question_text, 45))


def reset_timer():
    """
    :return: NONE. Reset's the timer text to '00:00' and it cancel's the previous timer function
    """
    global timer, timer_text
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text='00:00')


def reset():
    """
    :return: NONE. Reset's the: all_buttons list, count_click into their initial values
    """
    global all_buttons, count_click
    reset_timer()
    all_buttons = []
    count_click = 0


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Want to be a millionaire?")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_back_img = PhotoImage(file=card_back_file_path)
canvas_image = canvas.create_image(400, 263, image=card_back_img)
title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, ITALIC))
word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, BOLD))
timer_text = canvas.create_text(100, 130, text=f"{MINUTES_TO_ANSWER}:00", fill=WHITE, font=(FONT_NAME, 35, BOLD))
canvas.grid(column=0, row=0)

title_label = Label(text=money_dict[user_money_amount], font=(FONT_NAME, 40, BOLD), fg=BLACK, bg=WHITE)
title_window = canvas.create_window(300, 50, anchor=NW, window=title_label)

question_label = Label(text=text_label, font=(FONT_NAME, 15, BOLD), fg=BLACK)
question_window = canvas.create_window(150, 180, anchor=NW, window=question_label)

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

button_50_50 = Button(window, text=button_names[half], font=(FONT_NAME, BUTT0N_SIZE, BOLD), command=call_half_half)
button_50_50.grid(column=0, row=1)
button_50_50.config(pady=20, padx=20)
ask_public_button = Button(text=ask_public, font=(FONT_NAME, BUTT0N_SIZE, BOLD), command=call_ask_the_public)
ask_public_button.grid(column=1, row=1)
ask_public_button.config(pady=20, padx=20)
call_friend_button = Button(text=call_friend, font=(FONT_NAME, BUTT0N_SIZE, BOLD), command=call_a_friend)
call_friend_button.grid(column=2, row=1)
call_friend_button.config(pady=20, padx=20)

get_questions()

while keep_going:
    click_count = 0
    count_down(MINUTES_TO_ANSWER)
    question = pick_question()
    answer_options = [question.first_answer, question.second_answer, question.third_answer, question.fourth_answer]
    text_label = wrap_text(question)
    question_label.configure(text=text_label)
    create_buttons(answer_options, question)
    var = IntVar()
    button = Button(window, text=button_names["Next"], command=lambda: var.set(1),
                    font=(FONT_NAME, BUTT0N_SIZE, BOLD))
    button.grid(column=2, row=2, columnspan=2)
    button.config(pady=20, padx=20)
    button.wait_variable(var)
    title_label.config(text=money_dict[user_money_amount])
    reset()

window.mainloop()
