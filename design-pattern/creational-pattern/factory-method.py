from abc import ABC, abstractmethod


class DocumentCreator(ABC):
    @abstractmethod
    def create_document(self):
        """this is the factory method"""
        pass

    def export(self):
        doc = self.create_document()
        return doc
