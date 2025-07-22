# Design Document

## Overview

This design outlines the creation of a devcontainer environment that integrates both Gemini CLI and Claude Code tools. The solution will provide a containerized development environment with pre-configured AI assistant access, enabling developers to leverage both Google's Gemini and Anthropic's Claude services seamlessly.

## Architecture

The devcontainer will be built using a multi-stage approach:

1. **Base Image**: Ubuntu-based image with essential development tools
2. **AI Tools Layer**: Installation of Gemini CLI and Claude Code components
3. **Configuration Layer**: Environment setup and VS Code extensions
4. **Runtime Layer**: Final configuration and startup scripts

### Component Structure

```
.devcontainer/
├── devcontainer.json          # VS Code devcontainer configuration
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Optional: for complex setups
└── scripts/
    ├── install-gemini.sh      # Gemini CLI installation script
    ├── install-claude.sh      # Claude Code setup script
    └── setup-env.sh           # Environment configuration
```

## Components and Interfaces

### 1. Devcontainer Configuration (devcontainer.json)

**Purpose**: Defines VS Code devcontainer settings, extensions, and environment variables.

**Key Features**:
- VS Code extensions for AI development
- Port forwarding configuration
- Environment variable definitions
- Post-creation commands

### 2. Container Image (Dockerfile)

**Purpose**: Defines the container image with all necessary tools and dependencies.

**Layers**:
- Base system with Python, Node.js, Git
- Gemini CLI installation
- Claude Code CLI/tools installation
- Development utilities

### 3. Installation Scripts

**Purpose**: Modular scripts for installing and configuring AI tools.

**Scripts**:
- `install-gemini.sh`: Downloads and installs Google AI CLI tools
- `install-claude.sh`: Sets up Claude Code CLI or related tools
- `setup-env.sh`: Configures environment variables and paths

### 4. Environment Configuration

**Purpose**: Manages API keys and service authentication.

**Approach**:
- Environment variables for API keys
- Secure credential management
- Fallback to interactive authentication

## Data Models

### Environment Variables

```bash
# Gemini Configuration
GOOGLE_AI_API_KEY=<api_key>
GOOGLE_AI_PROJECT_ID=<project_id>

# Claude Configuration  
ANTHROPIC_API_KEY=<api_key>
CLAUDE_MODEL=claude-3-sonnet-20240229

# Development Configuration
WORKSPACE_ROOT=/workspace
```

### Configuration Files

```json
// devcontainer.json structure
{
  "name": "Gemini Claude Dev Environment",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-vscode.vscode-typescript-next",
        "claude-ai.claude-dev"
      ]
    }
  },
  "remoteEnv": {
    "GOOGLE_AI_API_KEY": "${localEnv:GOOGLE_AI_API_KEY}",
    "ANTHROPIC_API_KEY": "${localEnv:ANTHROPIC_API_KEY}"
  }
}
```

## Error Handling

### API Key Management

1. **Missing API Keys**: Display clear error messages with setup instructions
2. **Invalid API Keys**: Provide authentication troubleshooting steps
3. **Network Issues**: Include retry mechanisms and offline fallbacks

### Installation Failures

1. **Download Failures**: Implement retry logic with exponential backoff
2. **Permission Issues**: Use appropriate user permissions and sudo where necessary
3. **Dependency Conflicts**: Version pinning and compatibility checks

### Runtime Errors

1. **Service Unavailability**: Graceful degradation when AI services are down
2. **Rate Limiting**: Implement proper error handling for API rate limits
3. **Container Startup**: Health checks and startup validation

## Testing Strategy

### Unit Testing

1. **Installation Scripts**: Test each installation script independently
2. **Configuration Validation**: Verify environment variable handling
3. **Tool Availability**: Check that installed tools are accessible

### Integration Testing

1. **Container Build**: Automated testing of container image creation
2. **Service Integration**: Test API connectivity for both services
3. **VS Code Integration**: Verify extension functionality within devcontainer

### End-to-End Testing

1. **Complete Workflow**: Test full development workflow with both AI assistants
2. **Cross-Platform**: Validate on different host operating systems
3. **Performance**: Measure container startup time and resource usage

### Testing Tools

- **Docker**: Container testing and validation
- **Bash Testing**: Script validation using bats or similar
- **VS Code Testing**: Extension and devcontainer functionality testing

## Implementation Considerations

### Security

- API keys stored as environment variables, not in container image
- Secure credential passing from host to container
- Regular security updates for base image and dependencies

### Performance

- Multi-stage Docker builds to minimize image size
- Caching strategies for faster rebuilds
- Lazy loading of AI tools when possible

### Maintainability

- Modular script structure for easy updates
- Version pinning for reproducible builds
- Clear documentation and examples

### Compatibility

- Support for multiple VS Code versions
- Cross-platform compatibility (Windows, macOS, Linux)
- Flexible base image options