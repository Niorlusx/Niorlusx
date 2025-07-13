def log(message):
    print(f"[LOG] {message}")

def load_config(file_path):
    import json
    with open(file_path, 'r') as config_file:
        return json.load(config_file)