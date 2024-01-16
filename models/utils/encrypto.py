import secrets


class Encrypto:
    """ Generate random 32-bit integer value """
    def __init__(self):
        self._max_int = 2**32 - 1

    @property
    def get_id(self) -> int:
        """
        :return: int value
        """
        token = secrets.token_hex(4)  # 4 bytes = 32 bits
        encrypted_value = int(token, 16)  # convert hex string to integer
        return encrypted_value % self._max_int  # ensure value is within 32-bit integer range

