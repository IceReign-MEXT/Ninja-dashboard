import os

# Folder to inspect
project_folder = '.'

def inspect_file(file_path):
    """Basic inspection: type, size, first few lines."""
    info = {}
    info['type'] = 'directory' if os.path.isdir(file_path) else 'file'
    info['size_bytes'] = os.path.getsize(file_path)
    info['first_lines'] = []
    if info['type'] == 'file' and file_path.endswith(('.py', '.sh', '.txt', '.md')):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i in range(5):
                    line = f.readline()
                    if not line:
                        break
                    info['first_lines'].append(line.strip())
        except Exception as e:
            info['first_lines'].append(f'Error reading file: {e}')
    return info

def inspect_folder(folder):
    result = {}
    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        result[item] = inspect_file(full_path)
    return result

if __name__ == "__main__":
    structure = inspect_folder(project_folder)
    for file_name, info in structure.items():
        print(f"File/Dir: {file_name}")
        print(f"  Type: {info['type']}")
        print(f"  Size: {info['size_bytes']} bytes")
        if info['first_lines']:
            print(f"  First lines:")
            for line in info['first_lines']:
                print(f"    {line}")
        print('-' * 40)
