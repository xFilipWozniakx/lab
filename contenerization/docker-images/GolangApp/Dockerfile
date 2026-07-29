#Stage 1: builder
FROM golang:1.27rc2-trixie AS builder
ENV CGO_ENABLED=0
RUN apt-get update && apt-get install -y curl ca-certificates 
WORKDIR /go/src
COPY main.go go.mod .
RUN go build -a -installsuffix cgo -o server .

#Stage 2: serve app
FROM golang:tip-alpine3.24
RUN apk --no-cache add curl
COPY --from=builder /go/src/server /go/src
RUN adduser -D -H user && su user
WORKDIR /go/src
CMD ["./server"]
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
	CMD curl -f http://localhost:8080/ || exit 1 
EXPOSE 8080
