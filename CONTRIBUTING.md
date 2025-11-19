# Contributing to DevSecOps Pipeline

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features or improvements! Please create an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Possible implementation approaches (if you have ideas)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest src/test_app.py -v
   
   # Run security scans locally
   bandit -r src/
   pip-audit
   ```

4. **Commit your changes**
   ```bash
   git commit -m "feat: add new security feature"
   ```
   
   Use conventional commit messages:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `test:` - Test updates
   - `refactor:` - Code refactoring
   - `ci:` - CI/CD changes

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Fill out the PR template
   - Link any related issues
   - Wait for review

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aryansinghshaktawat/devsecops-pipeline.git
   cd devsecops-pipeline
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install bandit pip-audit cyclonedx-bom
   ```

4. **Run tests**
   ```bash
   pytest src/test_app.py -v --cov=src
   ```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write self-documenting code

## Security Guidelines

- Never commit secrets, API keys, or credentials
- Run security scans before submitting PRs
- Follow secure coding practices
- Report security vulnerabilities privately (see SECURITY.md)

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Include both positive and negative test cases

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update CHANGELOG.md with your changes
- Include code examples where helpful

## Questions?

Feel free to open an issue with the label `question` if you need help or clarification.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
