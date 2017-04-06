all:
	python -m grpc_tools.protoc -I./protos/ --python_out=./lback_grpc --grpc_python_out=./lback_grpc ./protos/server.proto
	python -m grpc_tools.protoc -I./protos/ --python_out=./lback_grpc --grpc_python_out=./lback_grpc ./protos/agent.proto
