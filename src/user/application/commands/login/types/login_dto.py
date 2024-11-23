class LoginDto:
    def __init__(self, login_credential: str, password: str):
        self.login_credential = login_credential
        self.password = password