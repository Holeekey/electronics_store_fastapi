from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

TEnc = TypeVar("TEnc")
TDec = TypeVar("TDev")

class ICryptographyProvider(Generic[TEnc, TDec], metaclass=ABCMeta):
  @abstractmethod
  def encrypt(self, plaintext: TDec) -> TEnc:
    pass

  @abstractmethod
  def decrypt(self, ciphertext: TEnc) -> TDec:
    pass