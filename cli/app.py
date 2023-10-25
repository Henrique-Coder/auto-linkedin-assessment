from colorama import init as int_colorama, Fore
from pyperclip import copy as pyperclip_copy, paste as pyperclip_paste
from pathlib import Path
from json import load


int_colorama(autoreset=True)


class Color:
    WHITE = Fore.WHITE
    RED = Fore.RED
    LWHITE = Fore.LIGHTWHITE_EX
    LRED = Fore.LIGHTRED_EX
    LGREN = Fore.LIGHTGREEN_EX
    LYELLOW = Fore.LIGHTYELLOW_EX
    LMAGENTA = Fore.LIGHTMAGENTA_EX


ANSWERS_FILE_PATH = Path('linkedin_data.json')


def find_answer(json_data: dict, question: str, copy_to_clipboard: bool = False):
    for subject in json_data.keys():
        for question_name in json_data[subject].keys():
            if question_name == question:
                answer = json_data[subject][question_name]['answer']
                if copy_to_clipboard:
                    pyperclip_copy(answer)

                return f'\n{Color.LGREN}Answer was successfully generated!\n\n{Color.WHITE}LinkedIn: {Color.LYELLOW}{subject}\n  {Color.WHITE}└ Question: {Color.LYELLOW}{question_name}\n      {Color.WHITE}└ Answer: {Color.LYELLOW}{answer}'


with open(Path(ANSWERS_FILE_PATH), 'r', encoding='utf-8') as fi:
    json_data = dict(load(fi))

print(f'{Color.LWHITE}\nSubjects available: {Color.LMAGENTA}{list(json_data.keys())}')


while True:
    while True:
        input_question = input(f'{Color.WHITE}\nEnter the question → ').strip()

        if not input_question:
            input_question = pyperclip_paste().strip()
            if not input_question:
                print(f'{Color.LRED}\nNo input found, try again...')
                continue
            break
        break

    answer = find_answer(json_data, input_question, False)
    if not answer:
        print(f'{Color.LRED}\nNo answer found for: {Color.LYELLOW}{input_question}')
        continue
    print(answer)

# Example question: Which statement is not an advantage of robotic process automation (RPA)?
