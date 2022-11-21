from passlib.hash import pbkdf2_sha256


class PasswordManager():
    def hash(self, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def compare(self, password: str, hash:str) -> bool:
        return pbkdf2_sha256.verify(password, hash)