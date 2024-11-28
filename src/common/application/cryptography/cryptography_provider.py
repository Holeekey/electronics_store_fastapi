from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

class ICryptographyProvider(ABCMeta):
  @abstractmethod
  def encrypt(self, plaintext: str) -> str:
    pass

  @abstractmethod
  def decrypt(self, ciphertext: str) -> str:
    pass