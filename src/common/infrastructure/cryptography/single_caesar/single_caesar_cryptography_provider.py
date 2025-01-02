from src.common.application.cryptography.cryptography_provider import ICryptographyProvider

class SingleCaesarProvider(ICryptographyProvider[str, str]):
  
  def __init__(self):
    pass

  def encrypt(self, plaintext: str) -> str:
    return plaintext[1:] + plaintext[0]
  
  def decrypt(self, ciphertext: str) -> str:
    last_char = len(ciphertext) - 1
    return ciphertext[last_char] + ciphertext[:last_char]
  