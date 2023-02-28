import re
from typing import List
from datetime import datetime

from .db_api import OutTaskSchema

DATE_FORMAT_PATTERN = re.compile(r'(\d{4}\-\d{2}\-\d{2})')


def get_card(task: OutTaskSchema) -> str:
    if isinstance(task, OutTaskSchema):
        return '\n'.join(
                    (
                        f'ID: {task.id}',
                        f'Зaголовок: {task.title}',
                        'Тело заметки отсутсвует' if task.body is None else f'Зaметка: {task.body}',
                        f'Время создания: {datetime.strftime(task.created_at, "%d %b %Y %H:%M")}',
                        f'Время последнего обновления: {datetime.strftime(task.updated_at, "%d %b %Y %H:%M")}',
                    )
                )


def get_all_cards(data: List[OutTaskSchema]) -> List:
    if isinstance(data, list) and isinstance(data[0], OutTaskSchema):
        cards = []
        for item in data:
            cards.append('#####\n{}\n'.format(get_card(item)))
        return '\n'.join(cards)


def get_pk():
    pk = input('Введите ID задачи: ').strip()
    return int(pk) if pk.isdigit() else None


def _clean_date(date: str) -> str:
    return re.sub(r'[^\-&\d]+', '-', date)


def get_search_date(msg: str):
    search_date = input(msg).strip()
    search_date = _clean_date(search_date)
    print()
    if re.match(DATE_FORMAT_PATTERN, search_date):
        return datetime.strptime(search_date, '%Y-%m-%d')
    return None
