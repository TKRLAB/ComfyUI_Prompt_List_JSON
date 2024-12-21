import json
import os
import folder_paths
from collections import OrderedDict

# Define a default boolean parameter for input
BOOLEAN = ("BOOLEAN", {"default": False})

class ComfyUI_Prompt_JSON:
    def __init__(self):
        # Define the folder and file paths for storing prompts
        self.prompt_list_folder = os.path.join(folder_paths.base_path, "Prompt")
        self.json_path = os.path.join(self.prompt_list_folder, "list.json")
        # Ensure the necessary files and directories exist
        self.ensure_json_file_exists()
        # Load the existing data from the JSON file
        self.data = self.load_json()

    def ensure_json_file_exists(self):
        """Ensure the prompt directory and JSON file exist. If not, create them."""
        if not os.path.exists(self.prompt_list_folder):
            os.makedirs(self.prompt_list_folder, exist_ok=True)
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w', encoding='utf-8') as file:
                json.dump({}, file, ensure_ascii=False, indent=4)

    def load_json(self):
        """Load data from the JSON file into an OrderedDict."""
        with open(self.json_path, 'r', encoding='utf-8') as file:
            return json.load(file, object_pairs_hook=OrderedDict) or OrderedDict()

    def save_json(self):
        """Save the current data to the JSON file."""
        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    @classmethod
    def INPUT_TYPES(cls):
        """Define the input types for the node interface."""
        instance = cls()
        items = list(instance.data.keys())
        return {
            "required": {
                "Prompt Name": ("STRING", {"multiline": False}),
                "Overwrite": BOOLEAN,
                "Console log": BOOLEAN,
                "Positive Prompt": ("STRING", {"multiline": True}),
                "Negative Prompt": ("STRING", {"multiline": True}),
            }
        }

    # Define return types for the process function
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "process"
    CATEGORY = "prompt"

    @classmethod
    def get_prompt_list(cls):
        """Retrieve a list of all prompt names in the data."""
        instance = cls()
        return list(instance.data.keys())

    def process(self, **kwargs):
        """
        Process and update prompts.
        - Adds or updates a prompt based on the provided input.
        - Prints prompt information if 'Console log' is enabled.
        """
        prompt_name = kwargs.get("Prompt Name", "").strip()
        positive_prompt = kwargs.get("Positive Prompt", "").strip()
        negative_prompt = kwargs.get("Negative Prompt", None)
        overwrite = kwargs.get("Overwrite", True)
        console_log = kwargs.get("Console log", True)

        # Ensure the prompt name is not empty
        if not prompt_name:
            raise ValueError("'Prompt Name' is required and cannot be empty.")

        # Check if the prompt already exists
        if prompt_name in self.data:
            # If overwrite is enabled, update the existing prompt
            if overwrite:
                if positive_prompt:
                    self.data[prompt_name]["positive"] = positive_prompt
                if negative_prompt is not None:
                    self.data[prompt_name]["negative"] = negative_prompt
        else:
            # For new prompts, 'Positive Prompt' is required
            if not positive_prompt:
                raise ValueError("'Positive Prompt' is required when adding a new prompt.")

            # Create a new prompt entry
            self.data[prompt_name] = OrderedDict([
                ("positive", positive_prompt),
                ("negative", negative_prompt if negative_prompt is not None else "")
            ])

        # Optionally log the prompt details to the console
        if console_log:
            print(f'POSITIVE: {self.data[prompt_name]["positive"]}\n')
            print(f'NEGATIVE: {self.data[prompt_name]["negative"]}')

        # Save changes to the JSON file
        self.save_json()
        return (self.data[prompt_name]["positive"], self.data[prompt_name]["negative"])

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        """Check for changes in the node (stub implementation)."""
        return float("NaN")

# Node mappings for the interface
NODE_CLASS_MAPPINGS = {
    "ComfyUI_Prompt_JSON": ComfyUI_Prompt_JSON
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_Prompt_JSON": "Prompt JSON"
}
