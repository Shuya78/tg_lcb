from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup


class FormState(StatesGroup):
    class Data(TypedDict):
        current_question_index: int
        question_answers: dict[str, str]

    waiting_answer = State()
