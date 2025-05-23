import asyncio


async def send_email(recipient: str, delay: int) -> None:
    """
    Асинхронная функция для имитации отправки письма с задержкой.

    Args:
        recipient: Имя получателя письма.
        delay: Задержка отправки в секундах.
    """
    print(f"Начинаю отправку письма для {recipient}...")
    await asyncio.sleep(delay)  # Имитация задержки отправки
    print(f"Письмо для {recipient} отправлено!")


async def main() -> None:
    """
    Основная асинхронная функция программы.
    Создает задачи для отправки писем всем пользователям и ожидает их завершения.
    """
    # Список пользователей и задержек отправки
    users = [("Alice", 2), ("Bob", 3), ("Charlie", 1), ("Diana", 4)]

    # Создаем список задач для отправки писем
    tasks = []
    for recipient, delay in users:
        # Создаем задачу для каждого пользователя и добавляем в список
        task = asyncio.create_task(send_email(recipient, delay))
        tasks.append(task)

    # Ожидаем завершения всех задач
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Запускаем основную асинхронную функцию
    asyncio.run(main())