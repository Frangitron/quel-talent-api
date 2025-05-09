import os

from fastapi.exceptions import HTTPException

from queltalentapi.foundation.exceptions import NotFoundError


async def handle_exceptions(func, **kwargs):
    """
    Handles exceptions by converting them to HTTPExceptions.
    """
    try:
        return await func(**kwargs)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        if os.environ.get("DEV"):
            raise
        else:
            raise HTTPException(status_code=500)
