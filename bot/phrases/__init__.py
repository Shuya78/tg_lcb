from dataclasses import dataclass, field

from .admin_phrases import AdminPhrases


@dataclass(frozen=True)
class BotPhrases:
    admin = AdminPhrases()
    bot_started = "Бот {me.username} успешно запущен"
    questions: tuple[tuple[str, list[str]], ...] = field(
        default_factory=lambda: (
            ("Вопрос 1", ["Один", "Два", "Три"]),
            ("Вопрос 2", []),
            ("Вопрос 3", []),
        )
    )
    form_end_message_text = "Ваши ответы отправлены"


phrases = BotPhrases()
