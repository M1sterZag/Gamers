import click
from loguru import logger

from app.auth.utils import get_password_hash
from app.dao.dependencies import get_session_with_commit
from app.auth.dao import UsersDAO


@click.command()
@click.option("--username", prompt="Username", required=True)
@click.option("--email", prompt="Email", required=True)
@click.option("--password", prompt="Password", hide_input=True, confirmation_prompt=True, required=True)
def create_admin(username, email, password):
    """
    Создает нового пользователя с ролью ADMIN.
    """

    async def main():
        logger.info(f"Пытаюсь создать админа: {username}")
        hashed_password = get_password_hash(password)

        async for session in get_session_with_commit():
            try:
                # Проверяем, существует ли уже пользователь с таким email или username
                existing_user = await UsersDAO.find_one_or_none(session=session, email=email, username=username)
                if existing_user:
                    click.echo("Пользователь с таким email или username уже существует.")
                    return

                # Создаем нового администратора
                await UsersDAO.add(
                    session=session,
                    username=username,
                    email=email,
                    password=hashed_password,
                    is_admin=True
                )
                click.echo("Администратор успешно создан!")
            except Exception as e:
                click.echo(f"Ошибка при создании администратора: {e}")
                raise

    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    create_admin()
