"""Importing this package ensures every model is registered against `Base.metadata`.

`Base.metadata.create_all(engine)` only knows about models that have been imported
before it runs.
"""

from app.models.application import Application
from app.models.email import Email
from app.models.status_history import StatusHistory

__all__ = ["Application", "Email", "StatusHistory"]
