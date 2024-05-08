import traceback

def log_error():
    with open("/var/log/btlog.txt", "a",encoding='utf-8') as file:
        file.write(f"{traceback.format_exc()}\n")
        # traceback.print_exc(file=file)
