from typing import Iterable

from aiogram import types
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .phrases import phrases

remove_markup = types.ReplyKeyboardRemove(remove_keyboard=True)


def create_question_answers_markup(answers: Iterable[str]):
    return (
        ReplyKeyboardBuilder()
        .add(*(KeyboardButton(text=a) for a in answers))
        .adjust(2, repeat=True)
        .as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
