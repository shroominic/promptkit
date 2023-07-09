from promptkit.config import settings


def from_template(name: str, **kwargs) -> str:
    """
    Return a template string with the given name, using the given kwargs
    """
    with open(f"{settings.TEMPLATE_PATH}/{name}{settings.TEMPLATE_EXT}") as f:
        return f.read().format(**kwargs)

