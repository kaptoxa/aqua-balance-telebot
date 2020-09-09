""" We create one bot for one user to work with his tasks """
import datetime
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions


class Mark(NamedTuple):
    """Tuple structure respondes a record in DB"""
    id: Optional[int]
    date: str
    drink: str  # what a drink?
    volume: int  # in ml


class AquaBalanceBot():

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def new_user(self, name):
        cursor = db.get_cursor()
        cursor.execute(f"select * from users where id={self.chat_id}")
        row = cursor.fetchone()
        if row:
            return False

        inserted_row_id = db.insert("users", {
            "id": self.chat_id,
            "name": name,
            "norm": 3
        })
        return inserted_row_id

    def add(self, raw_message: str) -> Mark:
        """ new mark """
        volume, text = _parse_message(raw_message)
        if not volume:
            return

        f_now = _get_now_formatted()
        inserted_row_id = db.insert("drunk", {
            "mdate": f_now,
            "volume": volume,
            "drink": text,
            "user_id": self.chat_id
        })
        return Mark(id=None, drink=text, volume=volume, date=f_now)

    def update_norm(self, value: int) -> bool:
        db.update("users", {"norm": value},
                  {"id": ("=", self.chat_id)})
        return True

    def drunklist(self) -> List[Mark]:
        """ return all marks """
        rows = db.fetchall(
            "drunk", ["*"],
            {"user_id": ("=", self.chat_id)})
        return [Mark(*row[:-1]) for row in rows]
        # clip this field because this is chat id

    def today(self) -> List[Mark]:
        """ return marks for today """
        def is_today(mark):
            then = datetime.datetime.strptime(mark.date, "%Y-%m-%d %H:%M:%S")
            then = then.replace(
                tzinfo=pytz.timezone("Europe/Moscow"))

            now = _get_now_datetime()
            delta = then - now
            return delta.days < 2 and _get_now_datetime().day == then.day

        return filter(is_today, self.drunklist())

    def total(self) -> int:
        norm = db.fetchone(
            "users", ["norm"],
            {"id": ("=", self.chat_id)})

        E = sum(mark.volume for mark in self.today())
        return int(E / norm * 100)

    def check(self) -> bool:
        return self.total() >= 100


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _parse_message(msg):
    """ text is what type of drink, number is a volume """
    text = []
    volume = 0
    for word in msg.split():
        try:
            volume += int(word)
        except ValueError:
            text += [word]

    if not text:
        text = ['water']
    return volume, ' '.join(text)
