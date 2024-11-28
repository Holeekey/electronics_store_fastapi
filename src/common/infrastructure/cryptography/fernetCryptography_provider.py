from common.application.cryptography.cryptography_provider import ICryptographyProvider
from cryptography.fernet import Fernet
from config import FERNET_KEY

def FernetProvider(ICryptographyProvider):
  def __init__(self, key):
    self.provider = Fernet(key)

  def encrypt(self, plaintext: str) -> str:
    return self.provider.encrypt(plaintext)

  def decrypt(self, ciphertext: str) -> str:
    return self.provider.decrypt(ciphertext)
  

def get_fernet_provider() -> FernetProvider:
  fernet = FernetProvider(key= FERNET_KEY)
  return fernet
