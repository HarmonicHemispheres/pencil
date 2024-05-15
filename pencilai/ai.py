from openai import OpenAI
from typing import List
from pencilai.models.file_model import File
from pencilai.models.message_model import Message
import json


class OpenAIModels:
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"


class AIEngine:

    def __init__(self, key: str):
        self.ai = OpenAI(api_key=key)
        self.messages: List[Message] = []


    def get_oa_msgs(self):
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_sys_message(self, files: List[File] = []):
        files_text = ""
        for f in files:
            files_text += f"\n{f.model_dump_json()}"

        msg = f"""
        <purpose>
        you are a helpful coding assistant. you are expert at writing clean, efficient, and well-structured code that integrates seamlessly with the provided context.
        use the users prompt and the files provided in the <files> section to propose updated file content
        </purpose>

        <rules>
        - ALWAYS responsd in json format outlined in the <response> section
        - use the original full file paths when referencing files to update
        - use the similar full file paths when creating new files and add them to the "files_to_create" list
        - use the full file paths when deleting files and add them to the "files_to_delete" list
        - summarize the changes you suggest in the "summary" field of the response
        </rules>

        <files>
        {files_text}
        </files>

        <response>
        {{
            "files_to_update": [
                {{"full_file_path": "<PATH>", "content": "<NEW TEXT CONTENT>"}},
                ...
            ],
            "files_to_create": [
                {{"full_file_path": "<PATH>", "content": "<TEXT CONTENT>"}},
                ...
            ],
            "files_to_delete": [
                {{"full_file_path": "<PATH>"}},
                ...
            ],
            "summary": "<BRIEF DESCRIPTION OF CHANGES>"
        }}
        </response>
        """
        # print(f"⚙️⚙️SYSTEM\n{msg}\n\n")
        return {"role": "system", "content": msg}

    def ask(self, prompt: str, files: List[File] = []) -> str:
        """
        Sends a prompt to the OpenAI API and returns the generated response.
        """
        self.messages.append(
            Message(
                content=prompt, 
                role="user",
                message_format="text"
            ))

        # -- call open ai
        response = self.ai.chat.completions.create(
            messages=[self.get_sys_message(files)] + self.get_oa_msgs(),
            model=OpenAIModels.GPT_4O,
            response_format = { "type": "json_object" },
        )
        resp_text = response.choices[0].message.content
        resp_json = json.loads(resp_text)

        # -- add ai response to active thread 
        self.messages.append(
            Message(
                content=resp_text, 
                role="assistant",
                message_format="json_object"

            ))

        return resp_json
    

    def ask_simple(self, prompt: str):

        # -- call open ai
        response = self.ai.chat.completions.create(
            messages=[
                {"role": "system", "content":"you are a helpful assistant"},
                {"role": "user", "content":prompt}
            ],
            model=OpenAIModels.GPT_3_5_TURBO,
        )
        resp_text = response.choices[0].message.content
        return resp_text