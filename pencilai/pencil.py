from pencilai.ai import AIEngine
from pencilai.models.file_model import File
from pathlib import Path
from typing import List
from rich.console import Console
import json

ignore = [
    ".png",
    ".pyc",
]
ignore_paths = [
    ".git"
]


class PencilAI:

    def __init__(self, openai_api_key: str = None, base_dir: str = None):
        self.base_dir = Path(base_dir)
        self.ai = AIEngine(openai_api_key)
        self.console = Console()


    def read_entire_project(self) -> List[File]:
        """
        Reads the contents of all files in the project directory and its subdirectories.
        Returns a list of all file contents.
        """
        file_contents = []
        for path in self.base_dir.rglob("*"):
            if any([True if ip in str(path.absolute()) else False for ip in ignore_paths]):
                continue
            if path.is_file() and path.suffix not in ignore:
                with open(path, "r", encoding="utf-8") as file:
                    f = File(
                        name=path.name,
                        full_path=path.absolute().as_posix(),
                        content=file.read()
                    )
                    file_contents.append(f)
        return file_contents
    
    def update_project(self, updates: dict):
        for file in updates.get("files_to_update", []):
            f = Path(file.get("full_file_path")).absolute()
            f.write_text(file.get("content"), encoding="utf-8")
            self.console.print(f"🤖:  Updated file: '{f}'")
        
        for file in updates.get("files_to_create", []):
            f = Path(file.get("full_file_path")).absolute()
            if not f.exists():
                f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(file.get("content"), encoding="utf-8")
            self.console.print(f"🤖:  Created file: '{f}'")
        
        for file in updates.get("files_to_delete", []):
            f = Path(file.get("full_file_path")).absolute()
            f.unlink()
            self.console.print(f"🤖:  Deleted file: '{f}'")

    def chat(self):
        

        while True:
            # get user prompt
            prompt = input("\n😎:  ")
            if prompt.lower() in ["exit", "quit"]:
                self.console.print("Exiting chat...")
                break

            # get ai response
            # -- UTIL STEPS
            clever_work_notice = self.ai.ask_simple(
                prompt=f"generate a 3-6 word clever notice for the user indicating you are thinking about their request. Use the <user-prompt> below to help tailor your response. For example: 'Thinking cap on!', 'Cogwheels turning...' etc... <user-prompt>{prompt}</user-prompt>"
            )
            print("\n")

            # -- DECIDE JOB
            with self.console.status(f"🤖:[green4] {clever_work_notice} [/green4]", spinner="dots") as status:
                response = self.ai.ask(prompt, files=self.read_entire_project())
            self.console.print(f"\n🤖:  {response.get("summary")}")

            # update files
            self.update_project(response)
            self.console.print(f"\n🤖:  Project Updated!")