import os
import time
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def cleanup_old_files(folder: str, max_age_hours: int = 24):
    """Remove files older than max_age_hours."""
    try:
        cutoff = time.time() - (max_age_hours * 3600)
        folder_path = Path(folder)
        
        for file_path in folder_path.rglob('*'):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff:
                file_path.unlink()
                logger.debug(f"Cleaned up: {file_path}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")