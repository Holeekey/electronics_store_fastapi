from src.common.application.cryptography.cryptography_provider import ICryptographyProvider
from cryptography.fernet import Fernet
from src.config import FERNET_KEY, ENCODING

class FernetProvider(ICryptographyProvider[str, str]):
  def __init__(self):
    self.provider = Fernet(FERNET_KEY)

  def encrypt(self, plaintext: str) -> str:
    return self.provider.encrypt(bytes(plaintext, ENCODING)).decode()

  def decrypt(self, ciphertext: str) -> str:
    return self.provider.decrypt(bytes(ciphertext, ENCODING)).decode()
  

def get_fernet_provider() -> FernetProvider:
  fernet = FernetProvider()
  return fernet
