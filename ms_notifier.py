import os

import paramiko
from plyer import notification


def read_ms_disk_size():
    host = os.environ.get("MS_HOST_IP")
    user = os.environ.get("MS_USER")
    secret = os.environ.get("MS_USER_PASSWORD")
    port = os.environ.get("MS_HOST_PORT")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=int(port))
    stdin, stdout, stderr = client.exec_command("""df -hT /var | grep G | awk '{print $1,":\\n",$3,"-",$4,"-",$5}'""")
    data = stdout.read() + stderr.read()
    client.close()
    return data


def notify_ms_disk_space():
    msg = read_ms_disk_size().decode('utf-8')
    notification.notify(
        title='Сводка по MS',
        message=msg,
        timeout=60,     # Время показа (сек),
    )
