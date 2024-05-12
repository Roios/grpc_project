#!/bin/bash

output1=$(grpcurl -plaintext localhost:8888 list)
echo "Output of 'grpcurl -plaintext localhost:8888 list' :"
echo "$output1"
echo

output2=$(grpcurl -plaintext localhost:8888 list Orders)
echo "Output of 'grpcurl -plaintext localhost:8888 list Orders' :"
echo "$output2"
echo

output3=$(grpcurl -plaintext -proto orders.proto localhost:8888 describe Orders.RegisterOrder)
echo "Output of 'grpcurl -plaintext -proto orders.proto localhost:8888 describe Orders.RegisterOrder' :"
echo "$output3"
echo

output4=$(grpcurl -plaintext localhost:8888 describe .StartResponse)
echo "Output of 'grpcurl -plaintext localhost:8888 describe .StartResponse' :"
echo "$output4"
echo