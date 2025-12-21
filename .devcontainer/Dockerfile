FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install essential utilities including coreutils for sleep command
RUN apt-get update && apt-get install -y \
    coreutils \
    curl \
    ca-certificates \
    gnupg \
    procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python 3.13
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.13 \
    python3.13-venv \
    python3.13-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python 3.13 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.13 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/home/vscode/.local/bin:$PATH"

# Install Node.js 22 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update && apt-get install -y gh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create directories for vscode user with proper ownership
RUN mkdir -p /home/vscode/.cache /home/vscode/.claude /home/vscode/.config/github-copilot /home/vscode/.npm-global \
    && chown -R vscode:vscode /home/vscode/.cache /home/vscode/.claude /home/vscode/.config /home/vscode/.npm-global

# Verify installations
RUN python --version && node --version && npm --version && gh --version
