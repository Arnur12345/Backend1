import os
import uuid
import shutil
from datetime import datetime
from typing import Dict, Optional, List
from fastapi import UploadFile
import json
import asyncio
from pathlib import Path


class FileManager:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.metadata_file = self.upload_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Загружает метаданные файлов из JSON"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_metadata(self):
        """Сохраняет метаданные файлов в JSON"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2, default=str)
    
    async def save_file(self, file: UploadFile, user_id: int) -> Dict:
        """Сохраняет загруженный файл и возвращает информацию о нем"""
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        safe_filename = f"{file_id}{file_extension}"
        file_path = self.upload_dir / safe_filename
        
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Сохраняем метаданные
        file_info = {
            "file_id": file_id,
            "original_filename": file.filename,
            "saved_filename": safe_filename,
            "file_size": len(content),
            "upload_time": datetime.now().isoformat(),
            "content_type": file.content_type,
            "file_path": str(file_path),
            "user_id": user_id
        }
        
        self.metadata[file_id] = file_info
        self._save_metadata()
        
        return file_info
    
    def get_file_info(self, file_id: str, user_id: int = None) -> Optional[Dict]:
        """Получает информацию о файле по ID"""
        file_info = self.metadata.get(file_id)
        if not file_info:
            return None
        
        # Проверяем права доступа пользователя
        if user_id is not None and file_info.get("user_id") != user_id:
            return None
            
        return file_info
    
    def get_file_content(self, file_id: str, user_id: int = None) -> Optional[str]:
        """Читает содержимое файла"""
        file_info = self.get_file_info(file_id, user_id)
        if not file_info:
            return None
        
        file_path = Path(file_info["file_path"])
        if not file_path.exists():
            return None
        
        try:
            # Пытаемся прочитать как текстовый файл
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Если не получается, пытаемся с другой кодировкой
                with open(file_path, 'r', encoding='cp1251') as f:
                    return f.read()
            except:
                return f"Не удалось прочитать файл {file_info['original_filename']}. Возможно, это бинарный файл."
    
    def list_files(self, user_id: int = None) -> List[Dict]:
        """Возвращает список всех загруженных файлов для пользователя"""
        if user_id is None:
            return list(self.metadata.values())
        
        return [file_info for file_info in self.metadata.values() 
                if file_info.get("user_id") == user_id]
    
    def delete_file(self, file_id: str, user_id: int = None) -> bool:
        """Удаляет файл и его метаданные"""
        file_info = self.get_file_info(file_id, user_id)
        if not file_info:
            return False
        
        # Удаляем физический файл
        file_path = Path(file_info["file_path"])
        if file_path.exists():
            file_path.unlink()
        
        # Удаляем из метаданных
        del self.metadata[file_id]
        self._save_metadata()
        
        return True


# Глобальный экземпляр файл-менеджера
file_manager = FileManager() 