# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within CraxCore Location Tracker, please send an email to the project maintainers. All security vulnerabilities will be promptly addressed.

## API Keys Protection

This project uses API keys to access external services. Please follow these security practices:

1. **Never commit your API keys to public repositories**
2. Always store your API keys in the `.env` file (which is gitignored)
3. Do not share your API keys with others
4. Rotate your API keys periodically
5. Use different API keys for development and production

## Data Security

1. All tracking logs are encrypted by default
2. The application requires password authentication
3. No data is sent to external servers except API requests to OpenCellID

## Environment Security

1. Always use the latest version of dependencies in `requirements.txt`
2. The application is designed to run in a secure Termux environment
3. Root functionality is optional and isolated

## Best Practices for Developers

1. When adding features that require API keys, always read them from the `.env` file
2. Use the built-in encryption utilities for any sensitive data
3. Add new API configuration options to `.env.example` but not with actual values
4. Validate user input to prevent injection attacks
