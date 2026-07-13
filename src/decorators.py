from typing import Callable, Any, Optional

import functools


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
      Декоратор, который  логирует  начало и конец выполнения функции, ее результаты или возникшие ошибки.
     Должен принимать необязательный аргумент 'filename', который определяет,
    куда будут записываться логи (в файл или в консоль)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                return result
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                raise

        return wrapper

    return decorator