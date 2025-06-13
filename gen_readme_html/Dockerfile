# Use official pandoc/minimal image
FROM pandoc/minimal:latest

# Install necessary tools
RUN apk add --no-cache bash

# Copy the conversion script
COPY readme2html.sh /usr/local/bin/readme2html

# Make script executable
RUN chmod +x /usr/local/bin/readme2html

# Set working directory
WORKDIR /data

# Set entrypoint
ENTRYPOINT ["readme2html"]

# Default command (shows help if no args provided)
CMD ["--help"]
