import json
import os
import folder_paths
from collections import OrderedDict
import random

# Define a default boolean parameter for input
BOOLEAN = ("BOOLEAN", {"default": False})

class ComfyUI_Prompt_JSON:
    def __init__(self):
        # Define the folder for storing prompts
        self.prompt_list_folder = os.path.join(folder_paths.base_path, "Prompt")
        # Ensure the folder exists
        if not os.path.exists(self.prompt_list_folder):
            os.makedirs(self.prompt_list_folder, exist_ok=True)

    def load_json(self, file_path):
        """Load data from the specified JSON file into an OrderedDict."""
        if not os.path.exists(file_path):
            return OrderedDict()
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file, object_pairs_hook=OrderedDict) or OrderedDict()

    def save_json(self, file_path, data):
        """Save data to the specified JSON file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define the input types for the node interface.
        - 'Prompt List': A dropdown to select existing prompts or create a new one.
        - 'New List Name': A string input for creating a new list (used when creating a new list).
        - 'Random': A boolean to enable/disable random prompt selection.
        - 'Overwrite': A boolean to allow overwriting an existing prompt.
        - 'Console Log': A boolean to enable logging to the console.
        - 'Prompt Name': A string for naming the current prompt.
        - 'Positive Prompt': Multiline text for the positive part of the prompt.
        - 'Negative Prompt': Multiline text for the negative part of the prompt.
        """
        instance = cls()
        # Include existing JSON files along with the option to create a "New List"
        prompt_files = ["New List"] + [f for f in os.listdir(instance.prompt_list_folder) if f.endswith('.json')]
        return {
            "required": {
                "Prompt List": (prompt_files, ),
                "New List Name": ("STRING", {"multiline": False}),
                "Random": BOOLEAN,
                "Overwrite": BOOLEAN,
                "Console Log": BOOLEAN,
                "Prompt Name": ("STRING", {"multiline": False}),
                "Positive Prompt": ("STRING", {"multiline": True}),
                "Negative Prompt": ("STRING", {"multiline": True}),
            }
        }

    # Define return types for the process function
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "full list")
    FUNCTION = "process"
    CATEGORY = "prompt"

    def process(self, **kwargs):
        """
        Process prompts:
        - Load the selected prompt list.
        - Optionally select a random prompt from the list.
        - Return the positive and negative prompts, as well as the full list.
        """
        prompt_list_name = kwargs.get("Prompt List", "").strip()
        new_list_name = kwargs.get("New List Name", "").strip()
        random_selection = kwargs.get("Random", False)
        overwrite = kwargs.get("Overwrite", False)
        console_log = kwargs.get("Console Log", False)
        prompt_name = kwargs.get("Prompt Name", "").strip()
        positive_prompt = kwargs.get("Positive Prompt", "").strip()
        negative_prompt = kwargs.get("Negative Prompt", "").strip()

        # Handle "New List" option: Create a new list if selected
        if prompt_list_name == "New List":
            if not new_list_name:
                raise ValueError("'New List Name' is required when creating a new list.")
            prompt_list_name = new_list_name + ".json"

        # Construct the file path for the selected or new prompt list
        prompt_list_path = os.path.join(self.prompt_list_folder, prompt_list_name)
        data = self.load_json(prompt_list_path)

        # Handle random selection of a prompt from the list
        if random_selection:
            if not data:
                raise ValueError("The selected prompt list is empty or invalid.")
            # Choose a random prompt name and fetch its details
            prompt_name = random.choice(list(data.keys()))
            positive_prompt = data[prompt_name]["positive"]
            negative_prompt = data[prompt_name]["negative"]
        else:
            # Validate required fields for manual input
            if not prompt_name:
                raise ValueError("'Prompt Name' is required when Random is not enabled.")
            if prompt_name in data:
                if overwrite:
                    # Overwrite existing positive/negative prompts if allowed
                    if positive_prompt:
                        data[prompt_name]["positive"] = positive_prompt
                    if negative_prompt or not data[prompt_name]["negative"]:
                        data[prompt_name]["negative"] = negative_prompt
                else:
                    # Load existing prompt details
                    positive_prompt = data[prompt_name]["positive"]
                    negative_prompt = data[prompt_name]["negative"]
            else:
                # Add a new prompt to the list
                if not positive_prompt:
                    raise ValueError("'Positive Prompt' is required when adding a new prompt.")
                data[prompt_name] = OrderedDict([
                    ("positive", positive_prompt),
                    ("negative", negative_prompt),
                ])

        # Optionally log the prompt details to the console
        if console_log:
            import shutil
            terminal_width = shutil.get_terminal_size((80, 20)).columns

            # Function to format multiline text with a background color
            def format_with_bg_multiline(text, color_code):
                lines = [text[i:i + terminal_width] for i in range(0, len(text), terminal_width)]
                return "\n".join(f"\033[1;{color_code}m{line.ljust(terminal_width)}\033[0;0m" for line in lines)

            # Log formatted details
            print(format_with_bg_multiline(f"{prompt_name} from {prompt_list_name}", "40;37"))
            print(format_with_bg_multiline(f"POSITIVE: {positive_prompt}", "40;32"))
            print(format_with_bg_multiline(f"NEGATIVE: {negative_prompt}", "40;31"))

        # Save the updated list back to the file
        self.save_json(prompt_list_path, data)

        # Return the processed positive prompt, negative prompt, and full list as JSON
        full_list = json.dumps(data, ensure_ascii=False, indent=4)
        return positive_prompt, negative_prompt, full_list

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
