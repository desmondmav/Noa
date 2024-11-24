import os
import shutil
import logging
from typing import List, Dict, Any
from pathlib import Path

class FileHandler:
    """
    Comprehensive file handling utility class
    """
    def __init__(self, base_dir: str = 'study_resources'):
        """
        Initialize file handler with base directory
        
        :param base_dir: Base directory for file operations
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save_file(self, file_path: str, destination_folder: str = 'documents') -> Dict[str, Any]:
        """
        Save a file to a specific directory
        
        :param file_path: Path of the file to save
        :param destination_folder: Subdirectory to save the file
        :return: File metadata
        """
        try:
            # Create destination directory
            dest_dir = self.base_dir / destination_folder
            dest_dir.mkdir(parents=True, exist_ok=True)

            # Generate unique filename
            file_name = Path(file_path).name
            unique_name = self._generate_unique_filename(dest_dir, file_name)
            
            # Copy file
            full_dest_path = dest_dir / unique_name
            shutil.copy2(file_path, full_dest_path)

            # Return file metadata
            return {
                'original_name': file_name,
                'saved_name': unique_name,
                'path': str(full_dest_path),
                'size': os.path.getsize(full_dest_path)
            }
        except Exception as e:
            self.logger.error(f"File saving error: {e}")
            raise

    def _generate_unique_filename(self, directory: Path, filename: str) -> str:
        """
        Generate a unique filename to prevent overwriting
        
        :param directory: Target directory
        :param filename: Original filename
        :return: Unique filename
        """
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while (directory / new_filename).exists():
            new_filename = f"{base}_{counter}{ext}"
            counter += 1

        return new_filename

    def list_files(self, folder: str = 'documents') -> List[Dict[str, Any]]:
        """
        List files in a specific folder
        
        :param folder: Folder to list files from
        :return: List of file metadata
        """
        try:
            folder_path = self.base_dir / folder
            if not folder_path.exists():
                return []

            return [
                {
                    'name': file.name,
                    'path': str(file),
                    'size': file.stat().st_size,
                    'modified': file.stat().st_mtime
                }
                for file in folder_path.iterdir() if file.is_file()
            ]
        except Exception as e:
            self.logger.error(f"File listing error: {e}")
            return []

    def delete_file(self, filename: str, folder: str = 'documents') -> bool:
        """
        Delete a specific file
        
        :param filename: Name of the file to delete
        :param folder: Folder containing the file
        :return: Deletion status
        """
        try:
            file_path = self.base_dir / folder / filename
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            self.logger.error(f"File deletion error: {e}")
            return False