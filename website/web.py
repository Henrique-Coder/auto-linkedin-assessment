from streamlit import (
    set_page_config as st_set_page_config, write as st_write, text_area as st_text_area, code as st_code, markdown as st_markdown, error as st_error, success as st_success, warning as st_warning
)
from pathlib import Path
from json import load


with open(Path('website/linkedin_data.json'), 'r', encoding='utf-8') as fi:
    json_data = dict(load(fi))

available_subjects = list(json_data.keys())


def find_answer(json_data: dict, question: str, ):
    for subject in json_data.keys():
        for question_name in json_data[subject].keys():
            if question_name == question:
                return json_data[subject][question_name]['answer']


def main(page_title: str) -> None:
    st_markdown(f"<h1 style='text-align: center;'>{page_title}</h1>", unsafe_allow_html=True)
    input_question = st_text_area('Paste your question here (one per time) ↴', height=180, help='⬐ You can paste one question per time here').strip()
    if input_question:
        st_write('---')
        st_write('The answer below should answer your question ↴')
        answer = find_answer(json_data, input_question)
        if not answer:
            st_error('Sorry, I cannot find the answer for this question. Please try another one.')
        else:
            st_success(answer)
    else:
        st_warning('Please paste your question above to get the answer ⤴')
    st_write('---')
    st_write('All available subjects are listed below ↴')
    st_code(available_subjects, language='python')


if __name__ == '__main__':
    page_title = 'Any LinkedIn Competency Assessments Question → Answer'
    st_set_page_config(page_title, 'favicon.ico', 'wide', 'collapsed')
    main(page_title)
