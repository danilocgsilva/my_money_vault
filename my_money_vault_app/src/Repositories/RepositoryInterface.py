from abc import ABC, abstractmethod
from typing import List, Optional

class RepositoryInterface(ABC):
    """Abstract base class for Institution repository"""
    
    @abstractmethod
    def create(self, model):
        pass
    
    @abstractmethod
    def find_by_id(self, model_id: int):
        pass
    
    @abstractmethod
    def find_all(self) -> List:
        pass
    
    @abstractmethod
    def update(self, model):
        pass
    
    @abstractmethod
    def delete(self, model_id: int) -> bool:
        pass
