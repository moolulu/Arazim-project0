import socket
import argparse
import sys
from threading import Thread


def receiver(conn):
    from_client = ""
    while True:
        data = conn.recv(4096)
        if not data:
            break
        from_client += data.decode('utf8')
    print(f'Received data: {from_client}')


def run_server(client_ip, client_port):
    """
    Receive data from client at address (ip, port).
    """
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((client_ip, client_port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()

        t = Thread(target=receiver, args=[conn])
        t.start()
        print(f"Message from thread {t.native_id}.")
        #t.run()
        t.join()
        conn.close()

        #receiver(conn)
        #conn.close()


def connections():
    """
    Handle connection requests from clients
    """
    while True:
        args = get_args()
        try:
            """
            t = Thread(target=run_server, args=[args.client_ip, args.client_port])
            t.start()
            t.run()
            print(f"Message from thread {t.native_id}.")
            t.join()
            print("Done.")
            """
            run_server(args.client_ip, args.client_port)
            print("Done.")
        except Exception as error:
            print(f'ERROR: {error}')
            return 1


def get_args():
    parser = argparse.ArgumentParser(description='Receive data from client.')
    parser.add_argument('client_ip', type=str,
                        help='the client\'s ip')
    parser.add_argument('client_port', type=int,
                        help='the client\'s port')
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    connections()


if __name__ == '__main__':
    sys.exit(main())
