from tortoise import fields
from tortoise.models import Model


class BotUser(Model):
    id = fields.BigIntField(pk=True, unique=True)  # telegram user id
    username = fields.TextField(null=True)
    full_name = fields.TextField()
    joined_at = fields.DatetimeField(auto_now_add=True)
    left_at = fields.DatetimeField(null=True)

    @property
    def mention(self):
        if self.username:
            return f"@{self.username}"

        return f'<a href="tg://user?id={self.id}">{self.full_name}</a>'

    @property
    def url(self):
        if self.username:
            return f"https://t.me/{self.username}"

        return f"tg://user?id={self.id}"


class BotChat(Model):
    id = fields.BigIntField(pk=True, unique=True)  # telegram chat id signed
    title = fields.TextField()
    username = fields.TextField(null=True)
    type = fields.TextField()


class StateBucket(Model):
    id = fields.IntField(pk=True, unique=True)
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    user_id = fields.BigIntField()
    state = fields.TextField(null=True)
    data = fields.JSONField(default={})


class FormRecord(Model):
    id = fields.IntField(pk=True, unique=True)
    answers = fields.JSONField()
    bot_user: fields.ForeignKeyRelation[BotUser] = fields.ForeignKeyField(
        "models.BotUser", related_name="form_records"
    )
