import json
import os

# Mapping for sameSite replacements
sameSite_replacements = {
    "strict": "Strict",
    None: "None",
    "lax": "Lax", 
    "no_restriction": "None"
}

def modify_cookie_file():
    try:
        # Use relative path and check file existence
        file_path = "./gmail.cookie.json"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found in current directory")
            
        with open(file_path, 'r') as file:
            cookies_data = json.load(file)

        # Recursive replacement function
        def replace_sameSite(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'sameSite':
                        obj[key] = sameSite_replacements.get(value, value)
                    elif isinstance(value, (dict, list)):
                        replace_sameSite(value)
            elif isinstance(obj, list):
                for item in obj:
                    replace_sameSite(item)

        replace_sameSite(cookies_data)

        # Write back with backup
        backup_path = "gmail.cookie.backup.json"
        os.rename(file_path, backup_path)
        
        with open(file_path, 'w') as file:
            json.dump(cookies_data, file, indent=2, ensure_ascii=False)
            
        print(f"Successfully updated {file_path}")
        print(f"Original file backed up as {backup_path}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Execute the modification
modify_cookie_file()
