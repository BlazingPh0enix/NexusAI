# NexusAI: AI-Powered Strategic Proposal Generator

Welcome to **NexusAI**, an innovative AI-driven platform built with [CrewAI](https://crewai.com) that leverages multi-agent collaboration to generate comprehensive strategic proposals for companies. This project empowers users to analyze market trends, identify AI use cases, collect resources, assess feasibility, and produce detailed proposals—all through an intuitive web interface powered by Streamlit.

## Features

- **Multi-Agent AI System**: Utilizes specialized AI agents for research, use case generation, resource collection, feasibility analysis, and proposal writing.
- **Web-Based Interface**: Easy-to-use Streamlit app for inputting company details and viewing generated reports.
- **Comprehensive Output**: Generates detailed Markdown reports and downloadable DOCX files.
- **Customizable Agents and Tasks**: Easily modify agent roles, goals, and task configurations via YAML files.
- **Seamless Integration**: Supports various search tools and integrates with external APIs for enhanced data gathering.

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- **Python**: Version 3.10 to 3.13 .
- **UV**: A fast Python package installer and resolver. Install it via:
  ```bash
  pip install uv
  ```
- **Pandoc**: Required for generating DOCX files from Markdown. Download from [pandoc.org](https://pandoc.org/installing.html).
- **API Keys**: Obtain an OpenAI API key for the AI agents to function properly.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BlazingPh0enix/NexusAI.git
   cd nexus_ai
   ```

2. **Install Dependencies**:
   Use UV to install the project dependencies:
   ```bash
   uv sync
   ```
   Alternatively, you can use the CrewAI CLI for installation:
   ```bash
   crewai install
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Configuration

Customize the AI agents and tasks to suit your needs:

- **Agents Configuration**: Edit `src/nexus_ai/config/agents.yaml` to define agent roles, goals, and backstories.
- **Tasks Configuration**: Modify `src/nexus_ai/config/tasks.yaml` to specify task descriptions and expected outputs.
- **Core Logic**: Update `src/nexus_ai/crew.py` to add custom logic, tools, or arguments.
- **Inputs**: Adjust `src/nexus_ai/main.py` for custom inputs to agents and tasks.

For advanced users, you can integrate additional search tools like Tavily or SerperDev by uncommenting and configuring them in `crew.py`.

## Running the Project

### Option 1: Web Interface (Recommended)

Launch the Streamlit web app for an interactive experience:

```bash
streamlit run app.py
```

- Open your browser and navigate to the provided URL (usually `http://localhost:8501`).
- Enter a company name and industry, then click "Generate Proposal" to create a strategic report.

### Option 2: Command Line Interface

Run the CrewAI crew directly from the terminal:

```bash
crewai run
```

This will execute the agents and generate a `final_proposal.md` file in the `output` folder with research on Nissan (default example). For custom inputs, modify `main.py` accordingly.

## Usage

1. **Input Details**: Provide the company name and industry in the web app.
2. **Generate Report**: Click the "Generate Proposal" button. A spinner will indicate progress.
3. **View Results**: The report will be displayed in a formatted view with tabs for "Final Report" and "Raw Markdown".
4. **Download**: Use the download button to save the report as a DOCX file.
5. **Customization**: Tailor the agents and tasks for specific use cases by editing the configuration files.

## Project Structure

```
nexus_ai/
├── app.py                          # Streamlit web application
├── pyproject.toml                  # Project dependencies and configuration
├── .env                             # Environment variables (not included in repo)
├── uv.lock                         # UV lockfile for dependencies
├── README.md                       # This file
├── output/
│   └── final_proposal.md           # Generated proposal output
├── src/
│   └── nexus_ai/
│       ├── __init__.py
│       ├── main.py                 # Entry point for CLI execution
│       ├── crew.py                 # CrewAI crew definition
│       ├── config/
│       │   ├── agents.yaml         # Agent configurations
│       │   └── tasks.yaml          # Task configurations
│       └── tools/
│           ├── __init__.py
│           └── search_tool.py      # Custom search tools
└── tests/                          # Unit tests
```


## For more information

- 📚 [CrewAI Documentation](https://docs.crewai.com)
- 🐙 [GitHub Repository](https://github.com/crewAIInc/crewAI)
