import grpc

import log
import orders_pb2 as pb
import orders_pb2_grpc as rpc


class ClientError(Exception):
    pass


class Client:

    def __init__(self, addr):
        # channel provides a connection to a gRPC server on a specified host and port
        self.channel = grpc.insecure_channel(addr)
        # stub is a client-side proxy for the remote service
        self.stub = rpc.OrdersStub(self.channel)
        log.info('Client connected to %s', addr)

    def close(self):
        self.channel.close()

    def order_start(self,
                    client_id: str,
                    street: str,
                    number: int,
                    city: str,
                    postal_code: int,
                    type: str,
                    time,
                    timeout: int = 6) -> str:
        # Create the request in the proper format
        request = pb.StartRequest(
            client_id=client_id,
            type=pb.APP if type == 'APP' else pb.ONLINE,
            address=pb.Address(street=street,
                               number=number,
                               city=city,
                               postal_code=postal_code),
        )
        request.time.FromDatetime(time)
        log.info('order started: %s', request)

        # Call the method with a timeout
        try:
            response = self.stub.RegisterOrder(request, timeout=timeout)
        except grpc.RpcError as err:
            log.error('start: %s (%s)', err, err.__class__.__mro__)
            raise ClientError(f'{err.code()}: {err.details()}') from err
        return response.order_id


def start_client(host, port):
    addr = f'{host}:{port}'
    # initialize a client
    client = Client(addr)

    # try a random request
    try:
        order_id = client.order_start(
            client_id="123abc",
            street="Av. Liberdade",
            number=25,
            city="Lisboa",
            postal_code=1600,
            type="APP",
            time=datetime(2024, 5, 13, 18, 56),
        )
        log.info('order ID: %s', order_id)
    except ClientError as err:
        raise SystemExit(f'error: {err}')

    return client


if __name__ == '__main__':
    from datetime import datetime

    import config
    client = start_client(config.host, config.port)
