# Start from the latest golang base image
FROM alpine:3.18.2

# Add Maintainer Info
LABEL maintainer="anatolylit@gmail.com"

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY module ./

# Expose port 8080 to the outside
EXPOSE 8080

# Command to run the executable
CMD ["./module"]