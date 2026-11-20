# Lab 5-47: Static Code Analysis – Reflection Answers

## 1. What is static code analysis, and why is it important?

Static code analysis examines source code without running the program. It helps find likely bugs, unsafe coding patterns and style problems early in development. Finding these issues before deployment reduces debugging effort and improves maintainability and security.

## 2. What are the differences between Pylint, Bandit and Flake8?

Pylint focuses on Python code quality, naming, documentation, potential programming mistakes and maintainability. Bandit scans Python source for common security problems, such as disabled TLS verification, weak randomness and unsafe temporary-file handling. Flake8 checks style and formatting rules, including whitespace, line length and unused imports. Their checks overlap only partially, so using all three gives broader coverage.

## 3. What challenges did you face while fixing the issues?

The main challenge was improving security without changing the expected expiry-monitoring behaviour. The RDAP helper needed certificate verification and a timeout, alert IDs needed a secure random source, and report creation needed a safely allocated file. I also had to avoid shared mutable state and make input errors explicit instead of hiding them with a broad exception handler. After each change, the demonstration and tests needed to be rerun.

## 4. How does static code analysis improve software quality?

Static analysis gives developers repeatable feedback about code quality, security and consistency. For a domain and SSL expiry monitor, it can help prevent unsafe network handling and fragile report generation before the system is relied on for operational alerts. It does not replace tests, code review or runtime monitoring, but it complements them.
