import typer

from .task import create_task, delete_task, list_tasks, update_task, get_task

app = typer.Typer()
app.command()(create_task)
app.command()(list_tasks)
app.command()(delete_task)
app.command()(update_task)
app.command()(get_task)


if __name__ == "__main__":
    app()