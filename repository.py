from sqlalchemy import or_
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from db import Group, Message, GroupMessage, Session

class BaseRepository:
    def get(self, model, id):
        s = Session()
        m = s.query(model).get(id)
        s.close()
        return m

    def getAll(self, model):
        s = Session()
        models = s.query(model).all()
        s.close()
        return models

    def create(self, model):
        session = Session()

        session.add(model)
        session.commit()

        session.close()

    def update(self, model, id, data):
        s = Session()
        instance = s.query(model).get(id)

        for key, value in data.items():
            setattr(instance, key, value)

        s.commit()
        s.close()

    def delete(self, model, id):
        s = Session()

        m = s.query(model).filter(model.id == id).one()
        s.delete(m)

        s.commit()
        s.close()

class MessageRepository(BaseRepository):
    def create(self, link):
        m = Message(link=link)
        super().create(m)

    def update(self, id, link):
        super().update(Message, id, {'link': link})

    def delete(self, id):
        super().delete(Message, id)


class GroupRepository(BaseRepository):
    def create(self, name, telegram_id):
        m = Group(name=name, telegram_id=telegram_id)
        super().create(m)

    def update(self, id, name, telegram_id):
        super().update(Group, id, {'name': name, 'telegram_id': telegram_id})

    def delete(self, id):
        super().delete(Group, id)


class GroupMessageRepository(BaseRepository):
    def create(self, message_id, group_id, time):
        m = GroupMessage(message_id=message_id, group_id=group_id, time=time)
        super().create(m)

    def update(self, id, message_id, group_id, time):
        data = {'message_id': message_id, 'group_id': group_id, 'time': time}
        super().update(GroupMessage, id, data)

    def delete(self, id):
        super().delete(GroupMessage, id)
