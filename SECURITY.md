# Security Policy

## 🔒 Reporting Security Vulnerabilities

We take the security of ContextCraft seriously. If you believe you have found a security vulnerability, please report it to us responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to [security@contextcraft.dev](mailto:security@contextcraft.dev)
2. **GitHub Security Advisory**: Use GitHub's [private vulnerability reporting](https://github.com/Shorzinator/ContextCraft/security/advisories/new)

### What to Include

When reporting a vulnerability, please include:

- **Description**: A clear description of the vulnerability
- **Impact**: What could an attacker accomplish with this vulnerability
- **Reproduction**: Step-by-step instructions to reproduce the issue
- **Environment**: Version numbers, operating system, Python version
- **Proof of Concept**: Code or commands that demonstrate the vulnerability
- **Suggested Fix**: If you have ideas for how to fix the issue

### Example Report

```
Subject: [SECURITY] Path Traversal Vulnerability in File Processing

Description:
The file processing function in ContextCraft allows path traversal attacks
through maliciously crafted filenames, potentially allowing access to
files outside the intended directory.

Impact:
An attacker could potentially read sensitive files from the system by
crafting filenames with "../" sequences.

Reproduction:
1. Create a file named "../../etc/passwd"
2. Run: contextcraft flatten "../../etc/passwd"
3. Observe that the command processes the file outside the intended directory

Environment:
- ContextCraft version: 0.1.0
- Python version: 3.11.5
- OS: Ubuntu 22.04

Proof of Concept:
[Attach code or detailed steps]

Suggested Fix:
Implement proper path sanitization using os.path.realpath() and validate
that resolved paths are within the intended directory boundaries.
```

## ⏱️ Response Timeline

We will acknowledge receipt of vulnerability reports within **48 hours** and provide regular updates on our progress. We aim to:

- **Initial Response**: Within 48 hours
- **Vulnerability Assessment**: Within 7 days
- **Fix Development**: Timeline depends on complexity
- **Coordinated Disclosure**: 90 days maximum (sooner if possible)

## 🛡️ Supported Versions

We provide security updates for the following versions:

| Version | Security Support |
|---------|:----------------:|
| 0.1.x   | ✅ Active       |
| < 0.1   | ❌ Not supported |

## 🔐 Security Measures

### Development Security

- **Code Review**: All code changes require review
- **Static Analysis**: Automated security scanning with Bandit
- **Dependency Scanning**: Regular dependency vulnerability checks
- **Pre-commit Hooks**: Security checks before code commits

### Runtime Security

- **Input Validation**: All user inputs are validated and sanitized
- **Path Sanitization**: File paths are validated to prevent traversal attacks
- **Permission Checks**: File operations respect system permissions
- **Error Handling**: Sensitive information is not exposed in error messages

### Configuration Security

- **Secure Defaults**: Safe configuration defaults
- **Permission Models**: Principle of least privilege
- **Credential Management**: No hardcoded credentials or secrets

## 🚨 Known Security Considerations

### File System Access

ContextCraft operates on the file system and processes user-specified files and directories. Users should be aware that:

- The tool respects file system permissions
- Symbolic links are handled carefully to prevent traversal attacks
- Large files are processed with memory-conscious streaming
- Binary files are detected and handled appropriately

### Git Operations

When processing Git repositories:

- Only standard Git commands are used
- No external Git hooks or scripts are executed
- Git operations are read-only by default
- Sensitive Git information (like credentials) is not processed

### Third-party Dependencies

We regularly monitor and update dependencies for security vulnerabilities:

- Automated dependency scanning in CI/CD
- Regular updates to address security patches
- Minimal dependency footprint to reduce attack surface

## 🏆 Security Best Practices for Users

### Installation Security

```bash
# Verify package integrity
pip install contextcraft --verify

# Use virtual environments
python -m venv contextcraft-env
source contextcraft-env/bin/activate
pip install contextcraft
```

### Usage Security

```bash
# Review .llmignore files to ensure sensitive files are excluded
cat .llmignore

# Use specific paths instead of wildcards when possible
contextcraft flatten src/specific/module.py

# Be cautious with output file permissions
contextcraft bundle -o output.md
chmod 600 output.md  # Restrict access if needed
```

### Configuration Security

```toml
# In pyproject.toml, be explicit about exclusions
[tool.contextcraft]
global_exclude_patterns = [
    "*.key",
    "*.pem",
    "*.env",
    "secrets/",
    ".ssh/",
    "credentials.*"
]
```

## 📞 Contact Information

- **Security Team**: [security@contextcraft.dev](mailto:security@contextcraft.dev)
- **General Contact**: [contact@contextcraft.dev](mailto:contact@contextcraft.dev)
- **GitHub Security**: [Private vulnerability reporting](https://github.com/Shorzinator/ContextCraft/security/advisories/new)

## 🙏 Acknowledgments

We appreciate security researchers and users who help keep ContextCraft secure. Responsible disclosure helps protect all users.

### Hall of Fame

*No security vulnerabilities have been reported yet. Be the first to help us improve!*

## 📜 Security Policy Updates

This security policy may be updated from time to time. Please check back periodically for the latest information.

**Last Updated**: 13-June-2025

---

**Note**: This security policy is inspired by industry best practices and is continuously improved based on community feedback and evolving security landscapes.
