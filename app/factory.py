from app import ConsoleApplication, AppCommands


def setup_commands(app: ConsoleApplication) -> None:
    cmd = AppCommands()
    
    app.init_command(
        command='add',
        description='Добавить заметку',
        callback=cmd.add_task
    )
    
    app.init_command(
        command='get',
        description='Получение заметок. Варианты: получить все заметки, заметки по дате, одну заметку',
        callback=cmd.get_task
    )
    
    app.init_command(
        command='remove',
        description='Удаление заметки по ID',
        callback=cmd.remove_task
    )
    
    app.init_command(
        command='update',
        description='Обновление заметки',
        callback=cmd.edit_task
    )

def create_app() -> ConsoleApplication:
    app = ConsoleApplication()
    setup_commands(app)
    
    return app
