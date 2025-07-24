# AI Agent Boilerplate

This project is a simple AI agent powered by Groq cloud (via LangChain), delivered through a Flask backend. All logic will be cleanly separated into modular files for easy maintenance and extension.

## Tech Stack

- [Flask](https://flask.palletsprojects.com/en/stable/) – For backend
- [Langchain](https://python.langchain.com/docs/introduction/) – Framework to build Chatbot

## Features

- Fast, production-ready backend (Flask)
- Modular integration with Groq's LLM via LangChain
- Runs on Windows, Linux, and macOS


## Prerequisites

### Install Python and create virtual environment

   - [Windows](https://github.com/Madhyamakist/workspace-setup-windows) 
   - [macOS](https://github.com/Madhyamakist/workspace-setup-mac/blob/dev/python_installation.md)
   <!-- - [Linux](https://github.com/Madhyamakist/workspace-setup-windows/blob/dev/python_installation.md)   -->


### Get a valid Groq API


- Go to [Groq](https://console.groq.com/keys) and create API Key
---



The Python version needs to be the same as mentioned in the `.tool-versions` file.

Install the Python version if not installed:
```
asdf install python X.Y.Z
```


Make sure the correct Python version has been set before you work on this project.
```
python3 --version
```

Before getting started, ensure `asdf` and Python is installed and working.This project uses [asdf](https://asdf-vm.com/) to manage language versions. 

## Getting Started

### Clone the repository:

```bash
git clone https://github.com/Madhyamakist/ai-agent-boilerplate.git myproject
```

---

### Set up virtual environment
#### Windows
<details>
- To create a virtual environment called "venv", run

```bash
python -m venv test
```
-  To activate the environment
```bash
test\Scripts\activate
```
</details>

#### macOS
<details>
- Navigate to your project directory
```bash
cd path/to/your/project
```
- Create a virtual environment named "test", 

```bash
python3 -m venv .test
```
-  To activate the environment
```bash
source .venv/bin/activate
```
</details>

---
