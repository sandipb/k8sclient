.PHONY: build py

build:
	go mod tidy
	go build ./

py:
	mypy python/
	black python/