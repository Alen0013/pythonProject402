import asyncio


async def send_notification(user: str, delay: int):
    """Асинхронная функция для отправки уведомления с задержкой."""
    print(f"Начинаю отправку уведомления для {user}...")
    await asyncio.sleep(delay)
    print(f"Уведомление для {user} отправлено!")


async def main():
    """Основная функция, запускающая отправку уведомлений."""
    users = [("Alice", 2), ("Bob", 3), ("Charlie", 1), ("Diana", 4)]

    # Создаем задачи для каждого пользователя
    tasks = [asyncio.create_task(send_notification(user, delay))
             for user, delay in users]

    # Ожидаем завершения всех задач
    await asyncio.gather(*tasks)


# Запускаем программу
asyncio.run(main())