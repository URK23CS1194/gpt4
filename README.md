# Personalized Recommendation System

A modular Streamlit application for recommending Coursera courses using a learner profile, dataset matching, optional Ollama personalization, ranking, explanations, feedback refinement, intent detection and saving.

## Dataset
Place `Coursera.csv` inside `dataset/`. The project is configured for the uploaded Coursera dataset. The application reads the course name, university, difficulty, rating, URL, description and skills columns.

## Requirements
- Python 3.10 or newer
- VS Code
- Ollama (optional, for local LLM personalization)

## Setup in Windows PowerShell

```powershell
cd PersonalizedRecommendationSystem
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the application

```powershell
streamlit run main.py
```

The browser will open the application, usually at `http://localhost:8501`.

## Enable Ollama (optional)
1. Install Ollama from https://ollama.com/download
2. In a terminal, run:

```powershell
ollama pull llama3.2
ollama serve
```

3. Keep Ollama running. In the Streamlit sidebar, use model name `llama3.2`.

If Ollama is not running, the application still works using dataset-based matching and scoring. The project uses Ollama/local LLM rather than the paid GPT-4 API.

## Modules
- `input_module.py`: collects the learner profile
- `profile_module.py`: displays the collected profile
- `preference_module.py`: analyzes interests and goals
- `prompt_module.py`: constructs the AI prompt
- `recommendation_module.py`: generates course recommendations
- `ranking_module.py`: ranks recommendations by score
- `explanation_module.py`: creates recommendation explanations
- `feedback_module.py`: refines recommendations using feedback
- `intent_module.py`: detects user intent
- `save_module.py`: saves recommendations to a text file
- `utils.py`: loads and searches the Kaggle dataset
- `main.py`: integrates the modules into the web application

## Screenshots
Save screenshots of the home screen, profile, preference analysis, prompt, recommendations, ranking, explanations, feedback, refined recommendations, intent detection and saved result in the `screenshots/` folder.

## GitHub
Create a new GitHub repository and upload the complete project folder. Do not upload your virtual environment (`venv/`) or private API keys.
