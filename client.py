from collections import namedtuple
from datetime import datetime, timedelta

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
        log.info('order started:\n%s', request)

        # Call the method with a timeout
        try:
            response = self.stub.RegisterOrder(request, timeout=timeout)
        except grpc.RpcError as err:
            log.error('start: %s (%s)', err, err.__class__.__mro__)
            raise ClientError(f'{err.code()}: {err.details()}') from err
        return response.order_id

    def update_order(self, events):

        # The request to the server needs to be iterable
        def generate_events():
            for event in events:
                request = pb.UpdateRequest(
                    client_id=event.client_id,
                    address=pb.Address(street=event.street,
                                       number=event.number,
                                       city=event.city,
                                       postal_code=event.postal_code),
                )
                request.time.FromDatetime(event.time)
                log.info('order updated:\n%s', request)
                yield request

        response = self.stub.UpdateOrder(generate_events())
        # The response is not an iterable object (the streaming was from the client to the server and not the other way)
        log.info('Received update response:\n%s', response.updated)


def start_client(host, port):
    addr = f'{host}:{port}'
    # initialize a client
    client = Client(addr)
    return client


def send_request(client):
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


def random_event_generator(count: int = 5) -> list:

    AddressEvent = namedtuple('AddressEvent',
                              'client_id street number city postal_code time')
    time = datetime(2024, 5, 13, 18, 56)
    new_events = []
    for idx in range(count):
        a_event = AddressEvent(client_id="123abc",
                               street="Av. Liberdade",
                               number=25 + idx,
                               city="Lisboa",
                               postal_code=1600,
                               time=time)
        new_events.append(a_event)
        log.info('update %d:\n %s', idx, a_event)
        time += timedelta(seconds=15)
    return new_events


def send_stream_request(client):
    # try a set of random request
    try:
        new_events = random_event_generator()
        client.update_order(new_events)
    except ClientError as err:
        raise SystemExit(f'error: {err}')


if __name__ == '__main__':
    import config
    client = start_client(config.host, config.port)
    # sending one single request
    send_request(client)
    # sending a stream of requests
    send_stream_request(client)
