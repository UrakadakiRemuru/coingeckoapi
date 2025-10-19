import asyncio
import functools


def retry(attempts: int = 5, attempt_time: int = 5, exceptions: tuple[Exception, ...] = (Exception,)):
    '''
    Осуществляет повтор заданное число раз, через заданный интервал времени в случае возникновения исключений. Если все попытки исчерпаны
    поднимает случившееся исключение.
    Args:
        attempts (int): Количество повторений.
        attempt_time (int): Время, через которое произойдет следующая попытка.
        exceptions (tuple[Exception, ...]): Кортеж исключений, после которых необходим повтор.
    '''

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    print(f'Столкнулись с проблемой {str(e)}. Попробуем снова через {attempt_time} секунд.')
                    if attempt == attempts:
                        print(f'Попытки не увенчались успехом. Столкнулись со следующей ошибкой {str(e)}.')
                        raise e
                    await asyncio.sleep(attempt_time)

        return wrapper

    return decorator
