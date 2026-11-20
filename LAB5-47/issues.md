# Lab 5-47: Static Analysis Findings

The line references below refer to domain_ssl_monitor_before.py, the intentionally flawed baseline. Locations are approximate and can shift if the file is edited.

| Issue | Type / Severity | Location (baseline) | Description | Fix Approach |
|---|---|---:|---|---|
| TLS certificate verification disabled | Security – High | fetchRdapRecord | The RDAP request disables certificate verification, allowing an attacker to impersonate the endpoint or intercept registration data. | Use HTTPS with certificate verification enabled (the Requests default); do not pass verify=False. |
| Weak random number generator for alert IDs | Security – Low | evaluateDomain | The standard random module is not intended for security-sensitive identifiers. | Use secrets.token_hex() to generate an unpredictable alert identifier. |
| Insecure temporary-file creation | Security – Medium | createReport | tempfile.mktemp() chooses a name without securely creating the file, creating a race condition. | Use NamedTemporaryFile(delete=False) and write through the securely opened handle. |
| Mutable default argument | Code quality | evaluateDomain | The default alertHistory=[] list is shared between calls, so one invocation can leak alerts into another. | Use None or create a new list inside the function. |
| Broad exception handler | Code quality | evaluateDomain | except Exception hides unrelated programming and data errors. | Validate the date format and catch only the specific expected exception, such as ValueError. |
| Non-snake-case identifiers | Code quality | Multiple functions | Names such as evaluateDomain and alertHistory violate the standard Python naming convention. | Rename functions and variables using snake_case. |
| Missing module/function documentation | Code quality | Multiple functions | The baseline does not explain the purpose and contracts of its public functions. | Add concise module and function docstrings. |
| Inconsistent whitespace and long lines | Style | Multiple lines | Long statements and inconsistent spacing reduce readability and trigger style checks. | Use consistent formatting, split long expressions and run Flake8 after changes. |

## Fix summary

The corrected domain_ssl_monitor.py uses verified HTTPS and a timeout for RDAP requests, cryptographically secure alert identifiers, securely created temporary report files, fresh per-call alert lists, narrow input validation, snake_case names and docstrings. It preserves the intended monitoring behaviour and is covered by tests/test_domain_ssl_monitor.py.
