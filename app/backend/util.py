import urllib.parse


def encode_password(password: str) -> str:
    # URL encode the password and double quote it
    return urllib.parse.quote_plus(password)


def escape_password(encoded_password: str) -> str:
    # Escape % to %%
    return encoded_password.replace("%", "%%")
