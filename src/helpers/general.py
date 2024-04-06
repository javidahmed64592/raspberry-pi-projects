from datetime import datetime


def print_system_msg(msg: str) -> None:
    """
    Print a message to the terminal.

    Parameters:
        msg (str): Message to print
    """
    print(f"[{datetime.now().strftime('%d-%m-%G | %H:%M:%S')}] {msg}")
