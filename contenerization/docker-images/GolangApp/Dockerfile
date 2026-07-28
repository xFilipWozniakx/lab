#Stage 1: builder
FROM golang:1.27rc2-trixie AS builder
ENV CGO_ENABLED=0
RUN apt-get update && apt-get install -y curl ca-certificates 
WORKDIR /go/src
COPY main.go go.mod .
RUN go build -a -installsuffix cgo -o server .



#Stage 2: serve app
FROM golang:tip-alpine3.24
COPY --from=builder /go/src/server /go/src
WORKDIR /go/src
CMD ["./server"]


# Add healthcheck
# Find out about switching root -> user

