# Config Manager

::: contextcraft.utils.config_manager

The config manager module provides configuration management functionality for ContextCraft, handling default settings and user-defined configurations.

## Overview

The config manager is responsible for:

- Loading and managing configuration files
- Providing default configuration values
- Handling configuration validation
- Managing configuration overrides

## Configuration Files

ContextCraft supports configuration through:

- Project-level configuration files
- User-level configuration files
- Environment variable overrides
- Command-line argument overrides

## Default Configuration

The config manager provides sensible defaults for all configuration options, ensuring that ContextCraft works out of the box without requiring extensive configuration.

## Related Modules

- [`bundler`](tools/bundler.md): Uses configuration for bundle settings
- [`git_provider`](tools/git_provider.md): Uses configuration for Git-related settings
