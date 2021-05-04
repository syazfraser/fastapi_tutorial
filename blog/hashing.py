from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        """
        Hashes the given password and returns it.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)
