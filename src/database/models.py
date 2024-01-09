from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.IntField(pk=True)


class CreatedAtMixin:
    created_at = fields.DatetimeField(auto_now_add=True)


class User(BaseModel, CreatedAtMixin):
    first_name = fields.TextField(null=True, max_length=15)
    last_name = fields.TextField(null=True, max_length=20)
    username = fields.TextField(null=True, max_length=30, index=True, unique=True)
    email = fields.TextField(max_length=256, index=True, unique=True)
    language = fields.CharField(default='ru', max_length=4)

    chats: fields.ManyToManyRelation['Chat']


class ChatSettings(BaseModel):
    chat = fields.OneToOneField('models.Chat', related_name='settings')
    admins: fields.ManyToManyRelation['User']


class Chat(BaseModel, CreatedAtMixin):
    title = fields.TextField(max_length=64)
    members: fields.ManyToManyRelation['User']
    settings: fields.OneToOneRelation['ChatSettings']

    link = fields.TextField(min_length=3, max_length=6, regex=r'^[a-zA-Z]+$', index=True, unique=True)
