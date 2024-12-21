"""
@author: TKLAB
@title: ComfyUI_Prompt_List_JSON
@description: ComfyUI JSON-based prompt management tool.
"""

from .ComfyUI_Prompt_JSON import ComfyUI_Prompt_JSON

NODE_CLASS_MAPPINGS = {
    "ComfyUI_Prompt_JSON": ComfyUI_Prompt_JSON
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_Prompt_JSON": "Prompt JSON"
}

WEB_DIRECTORY = "./web"

print("\033[1;40;35m ComfyUI_Prompt_List_JSON initialized \033[0;0m")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
