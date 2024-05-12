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
- the order is registered
- the supermarket says if the order is ready

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
<summary>Side note</summary>

The implemented server has reflection. That allows the clients to query the server about what it can do and what it needs (methods and types).
In our case is running in the localhost:888. From the command line you query the server.

Lets query the services available (we know that we only have `Orders`):

`grpcurl -plaintext localhost:8888 list`

Lets query the methods for the service `Orders` available:

`grpcurl -plaintext localhost:8888 list Orders`

And as expected we only have 1 method `Orders.RegisterOrder`. We can ask more information about it:

`grpcurl -plaintext localhost:8888 describe Orders.RegisterOrder`

and

`grpcurl -plaintext localhost:8888 describe .StartRequest`

</details>

### gRPC Client

The main goal of the client is to send requests to the server and receive answers.

# References

<https://grpc.io/>
