# Contributing to Finance Mentor AI

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/finance-mentor-ai.git
   cd finance-mentor-ai
   ```
3. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements_simple.txt
   pip install -r requirements_ml.txt  # optional
   ```

## Code Standards

### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Comment complex logic
- Optimize for performance

### HTML/CSS
- Use semantic HTML
- Follow Bootstrap conventions
- Ensure responsive design
- Maintain accessibility standards

## Testing

Run tests before submitting:
```bash
python test_setup.py
python test_app.py
```

## Submitting Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Commit with clear messages:
   ```bash
   git commit -m "Add: new feature description"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

## Areas for Contribution

### High Priority
- [ ] Enhanced ML models for forecasting
- [ ] Mobile app development
- [ ] Additional banking integrations
- [ ] Advanced security features

### Medium Priority
- [ ] More chart types and visualizations
- [ ] Export functionality improvements
- [ ] Performance optimizations
- [ ] Accessibility improvements

### Low Priority
- [ ] UI/UX enhancements
- [ ] Additional language support
- [ ] Social features
- [ ] Gamification elements

## Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Browser/OS information
- Error messages or screenshots

## Feature Requests

For feature requests, please:
- Check existing issues first
- Describe the use case
- Explain the expected benefit
- Consider implementation complexity

## Questions?

Feel free to open an issue for questions or join our discussions!
