import os
import logging

from .db_manager import Database
from ..logger import set_logger

logger = set_logger("setup_database")

def setup_database():
    """Sets up the database by creating necessary tables."""
    
    db = Database()
    queries = db.read_sql('data/schema.sql')
    db.execute_queries(queries)
    logger.info("Database setup completed successfully.")

if __name__ == "__main__":
    setup_database()
