"""
Log entry repository module.
"""
from app.db.repositories.mongodb import MongoDBRepository
from app.models.document import LogEntry


class LogEntryRepository(MongoDBRepository[LogEntry]):
    """
    Log entry repository.
    """
    def __init__(self):
        """
        Initialize repository.
        """
        super().__init__(LogEntry, "log_entries")
