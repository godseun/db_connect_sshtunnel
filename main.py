import sshtunnel
from util import Config
from mysql import connector as db

config = Config()

def query(q):
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
