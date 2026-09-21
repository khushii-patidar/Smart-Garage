import os
import re

def shrink_px(match):
    val = float(match.group(1))
    if val <= 2:
        return f"{int(val)}px"
    new_val = int(val * 0.75)
    return f"{new_val}px"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all numbers followed by px
    new_content = re.sub(r'(\d+(?:\.\d+)?)px', shrink_px, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Shrunk: {filepath}")

def main():
    base_dir = r"c:\Users\Ambika\Downloads\smartgarage-phase1\smartgarage"
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.html') or file.endswith('.css'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
