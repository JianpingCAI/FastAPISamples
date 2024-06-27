import re

text = """
This is some text.
thread [thread1] running
<?xml standalone="yes"?>
<a>
    <line> Line 1 within tags.</line>
</a>
This is some more text.
thread [thread2] running 
<?xml standalone="yes"?>
<a>
    <line> Another set of lines.</line>
</a>
"""

# Compile the pattern to match thread ID, XML declaration, and text between <a> and </a> tags
pattern = re.compile(r'thread \[(.*?)\] running\s*<\?xml standalone="yes"\?>\s*<a>(.*?)</a>', re.DOTALL)

# Find all matches using the compiled pattern
matches = pattern.findall(text)

print("Matches found:")
for match in matches:
    thread_id, content = match
    print(f"Thread ID: {thread_id}")
    # Remove leading/trailing whitespace and print each line within the content
    lines = content.strip().split('\n')
    for line in lines:
        print(line.strip())
    print()  # Print a newline for better readability
