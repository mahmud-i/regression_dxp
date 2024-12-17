import json


def extract_json_object(script_content, key):
    """
    Extracts a JSON object associated with the given key from the script content.

    Args:
        script_content (str): The full text content of the script element.
        key (str): The key whose JSON object needs to be extracted.

    Returns:
        dict or None: The parsed JSON object if found and successfully parsed, else None.
    """
    key_str = f"\\\"{key}\\\":"
    start_index = script_content.find(key_str)
    if start_index == -1:
        print(f'Key "{key}" not found in script content.')
        return None

    # Find the first '{' after the key
    start_brace_index = script_content.find('{', start_index)
    if start_brace_index == -1:
        print(f'Opening brace not found for key "{key}".')
        return None

    brace_count = 0
    end_brace_index = start_brace_index
    for i in range(start_brace_index, len(script_content)):
        if script_content[i] == '{':
            brace_count += 1
        elif script_content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_brace_index = i
                break

    # Extract the JSON string
    json_str = script_content[start_brace_index:end_brace_index + 1]

    # Unescape the JSON string
    try:
        unescaped_json_str = bytes(json_str, "utf-8").decode("unicode_escape")
        # Remove any trailing characters that might not be part of the JSON
        # For example, if the JSON is followed by a comma, it should be removed
        if unescaped_json_str.endswith(','):
            unescaped_json_str = unescaped_json_str[:-1]
        # Parse the JSON
        data = json.loads(unescaped_json_str)
        return data
    except json.JSONDecodeError as e:
        print(f'JSON decoding failed: {e}')
        return None
