import os
import re
import json
from .utils import to_persian


def get_all_json_paths(directory):
    """
    Recursively collect full paths of all JSON files in the given directory.

    Args:
        directory (str): Path to the root directory.

    Returns:
        List[str]: List of full paths to .json files.
    """
    json_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_paths.append(os.path.join(root, file))
    return json_paths


def extract_post_index_from_path(filepath):
    """
    Extracts the index `i` from a filename like 'post_i.json'.

    Args:
        filepath (str): Full path to the JSON file.

    Returns:
        int or None: The extracted index, or None if not matched.
    """
    filename = os.path.basename(filepath)
    match = re.match(r"post_(\d+)\.json", filename)
    if match:
        return int(match.group(1))
    return None


def load_post_json(filepath):
    """
    Loads a JSON file, adds 'nameid' field from the filename, and returns the data as a dictionary.

    Args:
        filepath (str): Full path to the JSON file.

    Returns:
        dict: JSON content with an added 'nameid' field.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    nameid = extract_post_index_from_path(filepath)
    data["nameid"] = nameid

    data["title"] = to_persian(data["title"])
    data["color"] = to_persian(data["color"])

    return data


def load_all_posts(directory):
    """
    Loads all JSON post files in a directory, adds 'nameid' to each, and returns them as a list of dictionaries.

    Args:
        directory (str): Path to the root directory containing post_*.json files.

    Returns:
        List[dict]: List of post data dictionaries with 'nameid' included.
    """
    json_paths = get_all_json_paths(directory)
    posts = []

    for path in json_paths:
        post_data = load_post_json(path)
        posts.append(post_data)

    return posts
