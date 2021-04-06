import sshtunnel
from util import Config
from mysql import connector as db

config = Config()

def query(q):
    """
    config:
    ssh_host = 'target_addr'            ex. 3.33.22.222
    ssh_port = target_port              ex. 22
    ssh_username = 'target_username'    ex. ubuntu
    ssh_pkey='auth_key_path'            ex. /home/user/aws.pem
    remote_host = 'remote_addr'         ex. 127.0.0.1
    remote_port = remote_port           ex. 3306
    db_host = 'db_addr'                 ex. 127.0.0.1
    db_user = 'user'                    ex. root
    db_password = 'password'            ex. 123123
    db_name = 'schema_name'             ex. ssh_db
    """
    with sshtunnel.SSHTunnelForwarder(
        ssh_address_or_host=(config.ssh_host, config.ssh_port),
        ssh_username=config.ssh_username,
        ssh_pkey=config.ssh_pkey,
        remote_bind_address=(config.remote_host, config.remote_port)
    ) as server:
        conn = db.connect(
            host=config.db_host,
            port=server.local_bind_port,
            user=config.db_user,
            passwd=config.db_password,
            db=config.db_name
        )

        cursor = conn.cursor()
        cursor.execute(q)
        result = cursor.fetchall()
        return result

df = query('show tables;')
print(df)
