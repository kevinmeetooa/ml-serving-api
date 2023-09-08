# Makefile for our Flask application
# Targets
.PHONY: build run test

build:
	docker build -t serving-api .

run:
	docker run -p 5000:5000 serving-api

test:
	pytest src
