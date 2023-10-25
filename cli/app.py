from colorama import init as int_colorama, Fore
from pyperclip import copy as pyperclip_copy, paste as pyperclip_paste
from pathlib import Path
from json import load
from difflib import get_close_matches


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


def find_exact(json_data: dict, question: str) -> str | None:
    for subject in json_data.keys():
        for question_name in json_data[subject].keys():
            if question_name == question:
                answer = json_data[subject][question_name]['answer']

                return f'\n{Color.LGREN}Answer was successfully generated!\n\n{Color.WHITE}LinkedIn: {Color.LYELLOW}{subject}\n  {Color.WHITE}└ Question: {Color.LYELLOW}{question_name}\n      {Color.WHITE}└ Answer: {Color.LYELLOW}{answer}'


def find_similars(json_data: dict, question: str) -> list | None:
    answer_match_list = list()

    for subject in json_data.keys():
        for question_name in json_data[subject].keys():
            if question in question_name:
                answer_match_list.append(question_name)

    return answer_match_list


with open(Path(ANSWERS_FILE_PATH), 'r', encoding='utf-8') as fi:
    json_data = dict(load(fi))

print(f'{Color.LWHITE}\nSubjects available: {Color.LMAGENTA}{list(json_data.keys())}')


def main(copy_answer_to_clipboard: bool = False) -> None:
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

        answer = find_exact(json_data, input_question)

        if not answer:
            answer_match_list = find_similars(json_data, input_question)

            if not answer_match_list:
                print(f'{Color.LRED}\nNo answer found for: {Color.LYELLOW}{input_question}')
                continue

            if len(answer_match_list) == 1:
                selected_question = answer_match_list[0]
                print(find_exact(json_data, selected_question))
                continue

            print()

            selected_question = None
            close_matches = get_close_matches(input_question, answer_match_list, n=9, cutoff=0.1)
            similar_questions = '\n'.join([f'├ {Color.WHITE}{idx+1}: {Color.LYELLOW}{question}{Color.WHITE}' for idx, question in enumerate(close_matches)])
            formatted_output = f'┌ Similar questions found for queue → {Color.LWHITE}{input_question}{Color.WHITE}\n│\n{similar_questions}\n│\n└ Enter the number corresponding to the desired question → '

            while True:
                try:
                    selected_question_idx = int(input(f'{Color.WHITE}{formatted_output}')) - 1
                    allowed_numbers = [str(idx) for idx in range(len(close_matches))]
                    if str(selected_question_idx) not in allowed_numbers:
                        print(f'{Color.LRED}\nInvalid option, try again...\n')
                        continue
                    selected_question = close_matches[selected_question_idx]
                    break
                except ValueError:
                    print(f'{Color.LRED}\nInvalid input, please enter a number...\n')
                    continue

            answer = find_exact(json_data, selected_question)

        if copy_answer_to_clipboard:
            pyperclip_copy(answer)

        print(answer)


if '__main__' == __name__:
    main(copy_answer_to_clipboard=False)  # SAMPLE: Which statement is not an advantage of robotic process automation (RPA)?
