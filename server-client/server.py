import argparse
import sys
from threading import Thread
import Listener
import Connection


def receiver(conn: Connection):
    """
    Receive data from client at address (ip, port).
    """
    with conn:
        from_client = ""
        while True:
            data = conn.receive_message()
            if not data:
                break
            from_client += data
        print(f'Received data: {from_client}')


def run_server(server_ip: str, server_port: int):
    """
    Listens to client address and creates a threads to receive messages.
    """
    with Listener.Listener(server_ip, server_port) as listener:
        while True:
            conn = listener.accept()
            t = Thread(target=receiver, args=[conn])
            t.start()
            print(f"Message from thread {t.native_id}.")


def connections():
    """
    Handle connection requests from clients
    """
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print("Done.")
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


def get_args():
    parser = argparse.ArgumentParser(description='Receive data from client.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    connections()


if __name__ == '__main__':
    sys.exit(main())
