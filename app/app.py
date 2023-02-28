from typing import Callable, Optional
import sys


def execute_command(func):
    def wrapper(*args, **kwargs):
        print('-' * 50)
        result = func(*args, **kwargs)
        print('-' * 50)
        return result
    return wrapper


class ConsoleApplication:
    def __init__(self) -> None:
        self._commands = {}
    
    def init_command(self, command: str, callback: Callable, description: Optional[str] = None):
        self._commands[command] = {
            'func': callback,
            'description': 'Описание отсутсвует' if description is None else description,
            'func': callback
        }
    
    def run(self):
        self._set_default_commands()
        msg = self._get_commands()
        print(msg)
        while True:
            cmd = input('Введите команду: ')
            self._handler(cmd)
            
    @execute_command
    def _handler(self, cmd: str) -> None:
        result = self._run_command(cmd)
        print(result)
    
    def _set_default_commands(self):
        self.init_command(
            command='exit',
            description='Завешение программы',
            callback=sys.exit
        )
        self.init_command(
            command='help',
            description='Получение справки о командах',
            callback=self._get_commands
        )
    
    def _run_command(self, command: str):
        command_obj = self._commands.get(command)
        func = self._run_bad_command if command_obj is None else command_obj['func']
        return func()
    
    def _get_commands(self):
        available_commands = '\n'.join([f'команда {cmd} - {self._commands[cmd]["description"]}' for cmd in self._commands])
        return f'Доступные команды:\n{available_commands}'
    
    def _run_bad_command(self):
        print('-----Неизвестная команда-----')
        return self._run_command('help')
    