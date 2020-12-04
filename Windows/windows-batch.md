# Batch File Tips

## Redirect Operators
[Microsoft Docs | Command redirection operators](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-xp/bb490982(v=technet.10)) (_[Wayback](https://web.archive.org/web/20201127015722/https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-xp/bb490982(v=technet.10))_)

Operator | Description
--- | ---
`>` | Writes the command output to a file or a device, such as a printer, instead of the Command Prompt window.
`<` | Reads the command input from a file, instead of reading input from the keyboard.
`>>` | Appends the command output to the end of a file without deleting the information that is already in the file.
`>&` | Writes the output from one handle to the input of another handle.
`<&` | Reads the input from one handle and writes it to the output of another handle.
`|` | Reads the output from one command and writes it to the input of another command. Also known as a pipe.

## Redirect Handles
Handle | Numeric | Description
---|---|---
STDIN | 0 | Keyboard input
STDOUT | 1 | Output to the Command Prompt window
STDERR | 2 | Error output to the Command Prompt window
UNDEFINED | 3-9 | These handles are defined individually by the application and are specific to each tool.


## Examples

Redirect `Your DOS command 2> nul`
