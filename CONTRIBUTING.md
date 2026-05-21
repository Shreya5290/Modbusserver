# Contributing

Thank you for contributing to this Modbus Server UI project.

## Getting Started

1. Fork the repository and clone your fork.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app locally:

```bash
python app.py
```

5. Open http://localhost:5000.

## Branch Naming

Use a descriptive branch name:

- `feature/<short-description>`
- `fix/<short-description>`
- `docs/<short-description>`

Examples:

- `feature/add-register-export`
- `fix/coil-write-validation`

## Commit Guidelines

Write short, clear commit messages in the imperative form.

- Good: `Add coil input validation`
- Good: `Fix register range check`
- Avoid: `changes` or `update file`

## Pull Request Checklist

Before opening a pull request, verify:

- The app starts with `python app.py`
- Core read/write flows still work
- No unrelated files were changed
- README/Docs are updated when behavior changes

## Coding Guidelines

- Keep changes focused and minimal.
- Match existing code style.
- Add comments only where logic is not obvious.
- Return user-friendly API errors for invalid inputs.

## Reporting Issues

Use the issue templates and include:

- What you expected to happen
- What actually happened
- Steps to reproduce
- Environment details (OS, Python version)
