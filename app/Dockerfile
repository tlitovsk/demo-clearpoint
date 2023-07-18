# Start from the latest golang base image
FROM alpine:3.18.2

# Add Maintainer Info
LABEL maintainer="anatolylit@gmail.com"

# go compat
RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2
RUN apk add gcompat
# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY module ./

# Expose port 8080 to the outside
EXPOSE 8080

# Command to run the executable
CMD ["./module"]