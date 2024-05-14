import random
from concurrent.futures import ThreadPoolExecutor  # needed to run the requests
from uuid import uuid4

import grpc
import grpc._server
from grpc_reflection.v1alpha import \
    reflection  # for clients to query what the server can do

import log
import orders_pb2 as pb
import orders_pb2_grpc as rpc
import validate


def new_order_id() -> None:
    """ Generate a unique new ID. """
    return uuid4().hex


class Orders(rpc.OrdersServicer):
    """ This is the service class.
        The name rpc.OrdersServicer matches the one in the orders_pb2_grpc.py file.
        Here is where we implement the proper methods.
        We need to override the requests.
    """

    def RegisterOrder(self, request, context):
        """ The real implementation of the RegisterOrder method. """

        log.info('request from client:\n%r', request)
        try:
            validate.start_request(request)
        except validate.Error as err:
            log.error('bad request: %s', err)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'{err.field} is {err.reason}')
            raise err

        order_id = new_order_id()

        return pb.StartResponse(order_id=order_id)

    def UpdateOrder(self, request_iterator, context):
        response_list = []
        for request in request_iterator:
            log.info('update:\n%s', request)
            response_list.append(random.choice([True, False]))

        return pb.UpdateResponse(updated=response_list)


def start_server(host, port) -> grpc._server:
    # Create a generic grpc server
    server = grpc.server(ThreadPoolExecutor())

    # Add the service to the server
    rpc.add_OrdersServicer_to_server(Orders(), server)

    # Add reflection to the server
    # names is the description of the generated protocol buffers for the service Orders
    names = (
        pb.DESCRIPTOR.services_by_name['Orders'].full_name,
        reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(names, server)

    # Server configuration and start it
    addr = f'{host}:{port}'
    server.add_insecure_port(addr)
    server.start()
    log.info('server ready on %s', addr)
    return server


if __name__ == '__main__':
    import config  # server config file
    server = start_server(config.host, config.port)
    server.wait_for_termination()
