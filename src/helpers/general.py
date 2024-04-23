from datetime import datetime


def system_msg(msg: str) -> None:
    """
    Print a message to the terminal.

    Parameters:
        msg (str): Message to print
    """
    return f"\r[{datetime.now().strftime('%d-%m-%G | %H:%M:%S')}] {msg}"
