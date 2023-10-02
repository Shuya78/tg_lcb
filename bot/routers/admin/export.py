from io import BytesIO

from aiogram import types
from aiogram.filters.command import Command
from openpyxl import Workbook

from ...database.models import FormRecord
from ...phrases import phrases
from . import router


@router.message(Command("export"))
async def export_command_handler(message: types.Message):
    wb = Workbook()
    ws = wb.active

    form_records = await FormRecord.filter().prefetch_related("bot_user")
    ws.append(("ID", "Username", "Имя", *(q[0] for q in phrases.questions)))  # type: ignore

    for record in form_records:
        ws.append(  # type: ignore
            (
                str(record.bot_user.id),
                str(record.bot_user.username),
                record.bot_user.full_name,
                *record.answers.values(),  # type: ignore
            )
        )

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    input_file = types.BufferedInputFile(buffer.read(), filename="answers.xlsx")

    await message.answer_document(input_file)
