# simple_plantuml_agent.py
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.file import FileTools


import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


env_vars_to_clear = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_API_BASE']
for var in env_vars_to_clear:
    if os.getenv(var):
        print(f"⚠️  Removing conflicting {var}")
        del os.environ[var]


# os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_ROUTER_KEY")
# os.environ['OPENAI_API_BASE'] = 'https://openrouter.ai/api/v1'
# os.environ['OPENAI_BASE_URL'] = 'https://openrouter.ai/api/v1'



env_vars_to_clear = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_API_BASE']
for var in env_vars_to_clear:
    if os.getenv(var):
        print(f"⚠️  Removing conflicting {var}")
        del os.environ[var]
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI_KEY")




def read_and_analyze_code(file_path: str) -> str:
    """Read a code file and return its content for analysis."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return f"File content of {file_path}:\n{content}"
    except Exception as e:
        return f"Error reading file: {e}"

def save_plantuml(content: str, filename: str) -> str:
    """Save PlantUML content to a file."""
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return f"PlantUML saved to {filename}"
    except Exception as e:
        return f"Error saving file: {e}"

# Create the agent
plantuml_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[FileTools(), read_and_analyze_code, save_plantuml],
    instructions=[
        "You are a PlantUML expert.",
        "When given a code file, analyze it and create a PlantUML class diagram.",
        "Always start PlantUML with @startuml and end with @enduml.",
        "Show classes, methods, and relationships.",
        "Save the result to a .puml file."
    ],
    show_tool_calls=True,
    markdown=True
)

# Batch processing
python_files = list(Path(".").rglob("*.py"))
print(f"Found {len(python_files)} Python files")

for py_file in python_files:
    print(f"Processing: {py_file}")
    file_stem = py_file.stem
    puml_filename = f"{file_stem}.puml"

    original_cwd = os.getcwd()
    os.chdir(py_file.parent)

    try:
        plantuml_agent.print_response(
            f"Read the file '{py_file.name}' and create a PlantUML activity diagram. Save it as {file_stem}_activity.puml",
            stream=True
        )
        plantuml_agent.print_response(
            f"Read the file '{py_file.name}' and create a PlantUML class diagram. Save it as {file_stem}_class.puml",
            stream=True
        )
        print(f"✅ Completed: {py_file.name}")
    except Exception as e:
        print(f"❌ Error with {py_file.name}: {e}")
    finally:
        os.chdir(original_cwd)

print("Batch processing complete!")