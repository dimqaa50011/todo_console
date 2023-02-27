from datetime import datetime

from .db_api import TaskCRUD, CreateTaskSchema

class AppCommands:
    
    def add_task(self):
        with TaskCRUD() as crud:
            answer = crud.create_task(
                CreateTaskSchema(
                    title=input('Введите заголовок заметки: '),
                    body=input('Введите тело заметки: ')
                )
            )
        
        if answer is None:
            msg = 'Не удалось добавить заметку. Попробуйте снова.'
            
        msg = '\n'.join(
            (
                f'ID: {answer.id}',
                f'ЗАголовок: {answer.title}',
                'Тело заметки отсутсвует' if answer.body is None else f'Зaметка: {answer.body}',
                f'Время создания: {datetime.strftime(answer.created_at, "%w %b %Y %H:%M")}',
                f'Время последнего обновления: {datetime.strftime(answer.updated_at, "%w %b %Y %H:%M")}',
            )
        )
        
        return msg