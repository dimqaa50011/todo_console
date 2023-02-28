from datetime import datetime, timedelta
from typing import Optional

from .db_api import TaskCRUD, CreateTaskSchema, UpdateTaskSchrma
from .halpers import get_card, get_all_cards, get_pk, get_search_date

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
            
        msg = get_card(answer)
        return msg
    
    def get_task(self):
        msg = '\n'.join(
            (
                'Введите параметр поиска',
                'one - для поиска конкретной заметки',
                'all - для получения всех заметок',
                'date - для поиска по дате',
                '=> '
            )
        )
        search_parametr = input(msg).strip()
        
        if search_parametr == 'one':
            result = self._fetchone()
            return get_card(result)
        
        elif search_parametr == 'all':
            result = self._fetchall()
            return get_all_cards(result.tasks)
        
        elif search_parametr == 'date':
            result = self._fetch_by_date()
            if isinstance(result, str):
                return result
            return get_all_cards(result.tasks)
        else:
            print('Неизвестный параметр. Попробуйте снова.')
        
    def _fetchall(self):
        with TaskCRUD() as crud:
            tasks = crud.get_all_tasks()
        return tasks

    def _fetchone(self):
        pk = get_pk()
        if pk is None:
            return 'ID должен быть числом'
        with TaskCRUD() as crud:
            task = crud.get_task(pk)
        return task
    
    def _fetch_by_date(self):
        start_date = get_search_date('Введите начальную дату: ')
        end_date = get_search_date(f'Введите кончную дату (оставьте пустым, если нужны заметки только за {start_date.date()}): ')
        if start_date is None:
            return 'Неверный формат даты. Попробуйте снова.'
        
        end_date = start_date + timedelta(days=1) if end_date is None else end_date
        
        with TaskCRUD() as crud:
            result = crud.get_task_by_date(start_date=start_date, end_date=end_date)
        return result

    def remove_task(self) -> str:
        pk = get_pk()
        if pk is None:
            return 'ID должен быть числом'
        
        with TaskCRUD() as crud:
            crud.delete_task(pk)
        return 'Заметка удалена'
    
    def edit_task(self):
        pk = get_pk()
        if pk is None:
            return 'ID должен быть числом'
        with TaskCRUD() as crud:
            task = crud.get_task(pk)
            
            msg = 'Текущее занчение {} (оставьте это поле пустым, если не хотите его менять): '
            new_title = input(msg.format(task.title))
            new_body = input(msg.format(task.body))
            complited = input(msg.format(task.is_complited))
            
            
            crud.update_task(
                pk,
                UpdateTaskSchrma(
                    title=task.title if new_title == '' else new_title,
                    body=task.body if new_body == '' else new_body,
                    is_complited=task.is_complited if complited == '' else not task.is_complited
                )
            )
        return f'Задача №{task.id} обновлена'
            
            