import functools


def retry_if_false(retries=3, except_text="Error: Function failed no details provided"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                result = func(*args, **kwargs)
                if result:
                    return result 
            raise Exception(except_text)
        return wrapper
    return decorator