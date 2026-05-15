import paramiko
from plyer import notification
import os


def read_maxbot_working():
    host = os.getenv("MAXBOT_HOST_IP")
    user = os.getenv("MAXBOT_USER")
    secret = os.getenv("MAXBOT_USER_PASSWORD")
    port = os.getenv("MAXBOT_HOST_PORT")
    private_key_file = os.getenv("MAXBOT_PK_FILE")
    pk_passphrase = os.getenv("MAXBOT_PK_PASSPHRASE")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=host,
        username=user,
        password=secret,
        port=int(port),
        pkey=paramiko.Ed25519Key.from_private_key_file(private_key_file, pk_passphrase),
        passphrase=pk_passphrase
    )
    stdin, stdout, stderr = client.exec_command("""ps aux | grep 'node bot.js'""")# | awk '{print $1,":\\n",$3,"-",$4,"-",$5}'
    data = stdout.read() + stderr.read()
    client.close()
    return data


def notify_maxbot_is_working():
    msg = read_maxbot_working().decode('utf-8')
    line = next(iter(
        i
        for i in msg.split('\n')
        if (i.rfind("node bot.js") == len(i) - len("node bot.js") and i.find("grep") == -1)
    ), None)
    notification.notify(
        title='Бот цифровой заведующий',
        message="Бот работает, всё хорошо" if line is not None else "Иди восстанавливать! Срочно!",
        timeout=60,  # Время показа (сек),
    )
