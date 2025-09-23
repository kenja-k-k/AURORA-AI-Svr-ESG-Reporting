# syntax=docker/dockerfile:1

ARG SNETD_VERSION=snetd-linux-amd64-v6.1.0

# ----------------------------
# Stage 1: Download snetd binary
# ----------------------------
FROM debian:bookworm-slim AS snet-daemon

# Install minimal tools to download snetd
RUN apt-get update && \
    apt-get install -y wget curl ca-certificates bash && \
    rm -rf /var/lib/apt/lists/*

# Download official snetd binary
RUN wget -O /usr/local/bin/snetd https://github.com/singnet/snet-daemon/releases/download/v6.1.0/snetd-linux-amd64-v6.1.0 \
  && chmod +x /usr/local/bin/snetd

# ----------------------------
# Stage 2: Runtime container
# ----------------------------
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates tzdata bash curl && \
    rm -rf /var/lib/apt/lists/*

# Set SSL cert path for Go TLS verification
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Create non-root snet user
RUN adduser --disabled-password --gecos "" --uid 10001 snet

# Working directory for logs
RUN mkdir -p /var/log/snet-daemon && chown -R snet:snet /var/log/snet-daemon

# Mountable config directory
RUN mkdir -p /etc/singnet && chown -R snet:snet /etc/singnet
VOLUME ["/etc/singnet"]

# Mountable custom certs directory
VOLUME ["/usr/local/share/ca-certificates"]

# Copy snetd binary from builder stage
COPY --from=snet-daemon /usr/local/bin/snetd /usr/local/bin/snetd

# Use log directory as working directory
WORKDIR /var/log/snet-daemon

# Run as non-root user
#USER snet

# Entrypoint: update CA certs at startup, then run snetd
ENTRYPOINT ["sh", "-c", "\
if [ -d /usr/local/share/ca-certificates ] && [ \"$(ls -A /usr/local/share/ca-certificates)\" ]; then \
    cp /usr/local/share/ca-certificates/* /usr/local/share/ca-certificates/; \
fi && update-ca-certificates && exec snetd serve -c /etc/singnet/snetd.config.json"]

