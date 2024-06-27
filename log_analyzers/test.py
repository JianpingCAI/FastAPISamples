import re

text = """
This is some text.
thread [1] running
<?xml standalone="yes"?>
<a>
Line 1 within tags.
Line 2 within tags.
Line 3 within tags.
</a>
This is some more text.
thread [2] running 
<?xml standalone="yes"?>
<a>
Another set of lines.
Inside the tags again.
</a>
"""

# Pattern to match thread ID, XML declaration, and text between <a> and </a> tags
pattern = r"thread \[(\d+)\] running\s*<\?xml standalone=\"yes\"\?>\s*<a>(.*?)</a>"

matches = re.findall(pattern, text, re.DOTALL)

print("Matches found:")
for match in matches:
    thread_id, content = match
    print(f"Thread ID: {thread_id}")
    # Remove leading/trailing whitespace and print each line within the content
    lines = content.strip().split("\n")
    for line in lines:
        print(line.strip())
    print()  # Print a newline for better readability
