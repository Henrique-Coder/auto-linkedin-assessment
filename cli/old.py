from colorama import init as int_colorama, Fore
from pyperclip import copy as pyperclip_copy, paste as pyperclip_paste
from pathlib import Path
from re import sub, search
from os import path
from difflib import get_close_matches
import json


int_colorama(autoreset=True)


class Color:
    WHITE = Fore.WHITE
    RED = Fore.RED
    LWHITE = Fore.LIGHTWHITE_EX
    LRED = Fore.LIGHTRED_EX
    LGREN = Fore.LIGHTGREEN_EX
    LYELLOW = Fore.LIGHTYELLOW_EX


ANSWERS_FOLDER = Path('linkedin_assets')


def sanitize_question_text(question: str) -> str:
    return sub(r'^#+\sQ\d+\.\s', str(), question)


def find_answer(file_data, linkedin_subject_file: str, question: str, copy_to_clipboard: bool = False) -> str:
    question = fr'{question}'
    if not path.exists(Path(ANSWERS_FOLDER, linkedin_subject_file)):
        return f'\n{Color.LRED}File not found: {Color.LYELLOW}{linkedin_subject_file}'

    close_matches = get_close_matches(question, [sanitize_question_text(line.strip()) for line in file_lines], n=3, cutoff=0.3)

    if question in close_matches:
        close_matches = [question]

    if not close_matches:
        return f'\n{Color.LRED}No similar questions found for: {Color.LYELLOW}{question}'

    if len(close_matches) == 1:
        selected_question = close_matches[0]
    else:
        similar_questions = '\n'.join([f'  ├ {Color.WHITE}{idx}: {Color.LYELLOW}{question}{Color.WHITE}' for idx, question in enumerate(close_matches)])
        formatted_output = f'\n  ┌ Similar questions found for queue → {Color.LWHITE}{question}{Color.WHITE}\n  │\n{similar_questions}\n  │\n  └ Enter the number corresponding to the desired question → '

        while True:
            try:
                selected_question_idx = int(input(f'{Color.WHITE}{formatted_output}'))
                allowed_numbers = [str(idx) for idx in range(len(close_matches))]
                if str(selected_question_idx) not in allowed_numbers:
                    print(f'{Color.LRED}\nInvalid option, try again...\n')
                    continue
                selected_question = close_matches[selected_question_idx]
                break
            except ValueError:
                print(f'{Color.LRED}\nInvalid input, please enter a number...\n')
                continue

    for line in file_lines:
        if selected_question in sanitize_question_text(line):
            answer_list = '\n'.join(
                [line.strip() for line in file_lines[file_lines.index(line) + 1:file_lines.index(line) + 6] if line.strip()]).split('\n')
            for answer in answer_list:
                if search(r'\[\w\]', answer):
                    correct_answer = answer[5:].strip()
                    if copy_to_clipboard:
                        pyperclip_copy(correct_answer)

                    print(f'{Color.LGREN}\nAnswer was successfully generated!\n')

                    return f'{Color.WHITE}LinkedIn: {Color.LYELLOW}{linkedin_subject_file[:-8].replace('-', ' ').strip().title()}\n  {Color.WHITE}└ Question: {Color.LYELLOW}{selected_question}\n      {Color.WHITE}└ Answer: {Color.LYELLOW}{correct_answer}'

    return f'\n{Color.LRED}Answer not found for the selected question: {Color.LYELLOW}{selected_question}'


with open(Path(ANSWERS_FOLDER, 'linkedin_data.json'), 'r', encoding='utf-8') as fi:
    file_data = json.load(fi)

while True:
    while True:
        input_question = input(f'\n{Color.WHITE}Enter the question → ').strip()

        if not input_question:
            input_question = pyperclip_paste().strip()
            if not input_question:
                print(f'{Color.LRED}\nNo input found, try again...')
                continue
            break
        break

    question_answer = find_answer(
        file_data=file_data,
        question=input_question,
        copy_to_clipboard=True
    )
    print(question_answer)
