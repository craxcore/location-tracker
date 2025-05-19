# Contributing to CraxCore Location Tracker

Thank you for your interest in contributing to the CraxCore Location Tracker project! This document provides guidelines for contributing code and using API keys securely.

## API Keys Security

This project uses API keys for accessing services like OpenCellID. Follow these guidelines to keep API keys secure:

### Never Commit API Keys to Git

1. The project uses a `.env` file for storing API keys locally
2. This file is listed in `.gitignore` and should NEVER be committed to the repository
3. Always use the provided `.env.example` as a template

### Setting Up Your Development Environment

1. Clone the repository
2. Copy `.env.example` to `.env`
3. Add your personal API keys to the `.env` file
4. Run `python init_api_keys.py` to initialize the configuration

### Implementing New Features That Use API Keys

1. Always read API keys from the `.env` file or config
2. Never hardcode API keys in source code
3. Add any new API keys to the `.env.example` file as a template

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure your code follows the project's style guide
5. Make sure all tests pass
6. Submit a pull request

## Code Style Guidelines

-   Follow PEP 8 for Python code
-   Use meaningful variable and function names
-   Add comments for complex logic
-   Write docstrings for all functions and classes

Thank you for helping to improve the CraxCore Location Tracker!
