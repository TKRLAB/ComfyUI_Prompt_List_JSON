# ComfyUI Custom Node: Prompt List JSON

This repository provides a custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that allows managing positive and negative prompts in a structured JSON format. The node supports adding, updating, and logging prompts, ensuring seamless integration into your workflow.

## Features

- 📂 **JSON-based prompt management**: Prompts are stored in a single `list.json` file for easy editing and retrieval.
- 🔄 **Add or update prompts**: Supports both creating new prompts and overwriting existing ones.
- 🖥️ **Console logging**: Optionally logs prompt details for debugging or verification.
- 🛠️ **Automatic file management**: Creates necessary directories and files automatically if they do not exist.

## Installation

1. Clone or download this repository to your ComfyUI custom node directory:
   ```bash
   git clone https://github.com/TKRLAB/ComfyUI_Prompt_List_JSON.git
   ```
2. Restart ComfyUI to load the custom node.
#### Alt method
1. Install from ComfyUI manager

![ComfyUI manager](https://github.com/TKRLAB/ComfyUI_Prompt_List_JSON/blob/master/images/manager.png)

## Usage

![node in menu](https://github.com/TKRLAB/ComfyUI_Prompt_List_JSON/blob/master/images/node_in_menu.png)

### Node Inputs

- **Prompt Name** (required): A unique name for the prompt.
- **Positive Prompt** (required for new prompts): The positive description of the prompt.
- **Negative Prompt** (optional): The negative description of the prompt.
- **Overwrite** (boolean, default `False`): Whether to overwrite an existing prompt with the same name.
- **Console log** (boolean, default `False`): Prints prompt details to the console for debugging.

### Node Outputs

- **Positive Prompt**: The saved or retrieved positive prompt.
- **Negative Prompt**: The saved or retrieved negative prompt.

### Example Workflow

1. Add or update a prompt with the following inputs:
   - **Prompt Name**: `SunsetScene`
   - **Positive Prompt**: `A breathtaking sunset over the mountains`
   - **Negative Prompt**: `Low quality, blurry`
   - **Overwrite**: `True`
   - **Console log**: `True`

![node](https://github.com/TKRLAB/ComfyUI_Prompt_List_JSON/blob/master/images/node.png)

2. The prompt will be saved to the JSON file, and its details will appear in the console if logging is enabled.

### File Structure

Prompts are stored in `list.json` in the following format:
```json
{
    "SunsetScene": {
        "positive": "A breathtaking sunset over the mountains",
        "negative": "Low quality, blurry"
    }
}
```

### Adding Prompts Programmatically

You can also use this node programmatically. Here's an example:
```python
from your_module import ComfyUI_Prompt_JSON

manager = ComfyUI_Prompt_JSON()
positive, negative = manager.process(
    **{
        "Prompt Name": "SunsetScene",
        "Positive Prompt": "A breathtaking sunset over the mountains",
        "Negative Prompt": "Low quality, blurry",
        "Overwrite": True,
        "Console log": True
    }
)
```

### Error Handling

- Raises a `ValueError` if a required field (e.g., `Prompt Name` or `Positive Prompt`) is missing.

![error prompt name](https://github.com/TKRLAB/ComfyUI_Prompt_List_JSON/blob/master/images/node_err1.png)
![error positive prompt](https://github.com/TKRLAB/ComfyUI_Prompt_List_JSON/blob/master/images/node_err2.png)

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

---

Enjoy using the **Prompt List JSON** node with ComfyUI! 🎨
