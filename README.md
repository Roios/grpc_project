# gRPC project in Python

This is a repository with a mini project for me to explore how gRPC works.

## What is gRPC

RPC means Remote Procedure Call. **gRPC** is a RPC framework created by Google.

The main basic idea behind a RPC is: the client sends a request to the server and the servers sends a response back.

Quoting the website:

> In gRPC, a client application can directly call a method on a server application on a different machine as if it were a local object, making it easier for you to create distributed applications and services.

Two key characteristics of gRPC are:

- HTTP Protocol -> HTTP 2
- Messaging Format -> Protobuf (Protocol Buffers)

## Mini project idea

We are going to implement a simple supermarket order app.
The idea is:

- the client makes an order
- the order is sent the server
- the client gets the order id

## Components

### gRPC Server

The main goal of the server is to receive requests and answer to them.

The server requires fixed data structure for the requests and the proper methods to know what to do.

**gRPC** uses Protocol Buffers for serializing structured data.

The first step is to define the structure for the data you want to serialize in a proto file (orders.proto). Protocol buffer data is structured as:

- messages: each message is a small logical record of information containing a series of name-value pairs called fields.
- services: each service encapsulates a functionality that can be invoked remotely. A service has methods.

For example:

This is how one can define the structure of an address:

```
message Address {
  string street = 1;
  int64 number = 2;
  string city = 3;
  int64 postal_code = 4;
}
```

And this is a service Orders. The service has a method (GetClosest) that receives and returns an Address.
We can have multiple methods per service.

```
service Orders {
  rpc GetClosest(StartRequest) returns (StartResponse) {}
}
```

Once we have the protocol written, we need to generate the Python code for that.
Assuming that we are in the directory where the proto file is:

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. orders.proto
```

- `-I.` -> look for protocol definition in the current directory
- `--python_out=.` -> where the generated serialization/deserialization code should go
- `--grpc_python_out=.` -> where Python server code should be placed
- `orders.proto` -> the protocol to use

Check `gen_grpc_code.sh`.

Once we run it, we will get 2 new files:

- `orders_pb2_grpc.py` -> the gRPC defintion
- `orders_pb2.py` -> protocol buffer definition

Now we have all the **gRPC** code needed for the server. The server code can be found in `server.py`.

In the `order.proto` we say that the method `RegisterOrder` exists but we didn't write it. In `orders_pb2_grpc.py`, the method `RegisterOrder` exists but it just says unimplemented. The real implementation is in `server.py`. So the first step is to override the methods of the service (check class `Orders`). Finally we can start the server (check `start_server`).

<details>
<summary>Side note about grpcurl</summary>

The implemented server has reflection. That allows the clients to query the server about what it can do and what it needs (methods and types).
In our case is running in the localhost:888. From the command line you query the server. For that we need `grpcurl`. To install it run:

`curl -sSL "https://github.com/fullstorydev/grpcurl/releases/download/v1.9.1/grpcurl_1.9.1_linux_x86_64.tar.gz" | sudo tar -xz -C /usr/local/bin`

Lets query the services available (we know that we only have `Orders`):

`grpcurl -plaintext localhost:8888 list`

Lets query the methods for the service `Orders` available:

`grpcurl -plaintext localhost:8888 list Orders`

And as expected we only have 1 method `Orders.RegisterOrder`. We can ask more information about it:

`grpcurl -plaintext localhost:8888 describe Orders.RegisterOrder`

and

`grpcurl -plaintext localhost:8888 describe .StartRequest`

We can also test the server! Lets use 2 dummy request files, one good and another bad to raise an error.

`grpcurl -plaintext -d @ localhost:8888 Orders.RegisterOrder < dummy_request.json`

and

`grpcurl -plaintext -d @ localhost:8888 Orders.RegisterOrder < dummy_request_2.json`

</details>

### gRPC Client

The main goal of the client is to send requests to the server and receive answers.

We need to create a class `Client` (check `client.py`). That class needs a channel and a stub. A channel provides a connection to a gRPC server on a specified host and port. A stub is a client-side proxy for the remote service.

Once we have the basic client, we need to implement the client's code. It consists in preparing a request in the proper format to the server and receive the response. To do it properly, one must implement the "send request" with a timeout. That means that if the server takes too long to answer, we get an error.

To run it, you must start initiate the `server.py`, otherwise you get the timeout error. Once the server is up and running, you can run `client.py`.

### gRPC streaming

Streaming allows us to send more than 1 message at the time. In other words, to send a continuous stream of messages from client/server to server/client. Stream can be in one way (unilateral) or both ways (bilateral).

#### Unilateral

Lets consider that the client can move so we want to update the address. The same way we created the `StartRequest` in the `orders.proto` file, we create the `UpdatedRequest`. We also have a new method called `UpdateOrder`. We generate the code as before:

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. orders.proto
```

On the server side, we need to implement the `UpdateOrder` method.

On the client side, we need to implement a method on the `Client` class that send multiple message, `update_order`.

To run it, you must start initiate the `server.py`, otherwise you get the timeout error. Once the server is up and running, you can run `client.py`. It will first send one single request and after it will send a stream of requests.

# References

<https://grpc.io/>


## Closure

The goal of this repo was achieved (basic hands-on with gRPC). This repo is closed.
