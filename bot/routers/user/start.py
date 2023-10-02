from aiogram import F, types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from ... import markups
from ...core import bot
from ...database.models import BotUser, FormRecord
from ...phrases import phrases
from ...state import FormState
from . import router


async def send_next_question(
    bot_user: BotUser, state: FSMContext, state_data: FormState.Data
):
    try:
        question, answers = phrases.questions[state_data["current_question_index"]]
    except IndexError:
        await state.clear()
        await FormRecord.create(
            bot_user=bot_user, answers=state_data["question_answers"]
        )

        return await bot.send_message(bot_user.id, phrases.form_end_message_text)

    await bot.send_message(
        bot_user.id,
        question,
        reply_markup=markups.create_question_answers_markup(answers),
    )


@router.message(CommandStart())
async def start_command_handler(_: types.Message, state: FSMContext, bot_user: BotUser):
    await state.set_state(FormState.waiting_answer)

    state_data: FormState.Data = {
        "current_question_index": 0,
        "question_answers": {},
    }

    await state.set_data(state_data)  # type: ignore
    await send_next_question(bot_user, state, state_data)


@router.message(FormState.waiting_answer, F.text)
async def answer_handler(
    message: types.Message,
    state: FSMContext,
    state_data: FormState.Data,
    bot_user: BotUser,
):
    current_question, _ = phrases.questions[state_data["current_question_index"]]
    state_data["question_answers"][current_question] = message.text  # type: ignore
    state_data["current_question_index"] += 1
    await state.set_data(state_data)  # type: ignore
    await send_next_question(bot_user, state, state_data)
