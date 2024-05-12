#!/bin/bash

echo "Output of 'grpcurl -plaintext localhost:8888 list' :"
output1=$(grpcurl -plaintext localhost:8888 list)
echo "$output1"
echo

echo "Output of 'grpcurl -plaintext localhost:8888 list Orders' :"
output2=$(grpcurl -plaintext localhost:8888 list Orders)
echo "$output2"
echo

echo "Output of 'grpcurl -plaintext -proto orders.proto localhost:8888 describe Orders.RegisterOrder' :"
output3=$(grpcurl -plaintext -proto orders.proto localhost:8888 describe Orders.RegisterOrder)
echo "$output3"
echo

echo "Output of 'grpcurl -plaintext localhost:8888 describe .StartResponse' :"
output4=$(grpcurl -plaintext localhost:8888 describe .StartResponse)
echo "$output4"
echo

echo "Output of 'grpcurl -plaintext -d @ localhost:8888 Orders.RegisterOrder < dummy_request.json' :"
output5=$(grpcurl -plaintext -d @ localhost:8888 Orders.RegisterOrder < dummy_request.json)
echo "$output5"
echo

echo "Output (should fail) of 'grpcurl -plaintext -d @ localhost:8888 Orders.RegisterOrder < dummy_request_2.json' :"
output6=$(grpcurl -plaintext -d @ localhost:8888 Orders.RegisterOrder < dummy_request_2.json)
echo "$output6"
echo