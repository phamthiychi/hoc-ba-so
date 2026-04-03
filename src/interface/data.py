from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")

class Repository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, create_info: dict) -> Optional[T]:
        """Thêm thông tin của một đối tượng cụ thể"""
        raise NotImplementedError

    @abstractmethod
    async def get(self, code: str) -> Optional[T]:
        """Lấy thông tin của một đối tượng cụ thể"""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Optional[list[T]]:
        """Lấy thông tin của tất cả đối tượng"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, code: str) -> bool:
        """Xóa thông tin của một đối tượng cụ thể"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, update_info: dict) -> Optional[T]:
        """Cập nhật thông tin của một đối tượng cụ thể"""
        raise NotImplementedError