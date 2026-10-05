# Interview Buddy

A mock interview partner for campus placements. It asks one question at a time, scores each answer out of 10, shows what worked, what to fix and a stronger version, then gives a final report. It runs fully on your laptop using Gemma through Ollama. No API keys, no internet needed after setup, and nothing you say leaves the machine.

## Run it

1. Install [Ollama](https://ollama.com) and pull a Gemma model:
   ```
   ollama pull gemma3:4b
   ```
2. Install and start the app:
   ```
   pip install -r requirements.txt
   python app.py
   ```
3. Open http://127.0.0.1:5000

## Use a different model

```
OLLAMA_MODEL=gemma3:12b python app.py
```

Any model Ollama can serve works. Smaller models are faster on weak laptops, bigger ones give better feedback.

## How it works

- `app.py`: tiny Flask server. Builds the interviewer prompt and calls Ollama's chat API.
- `static/index.html`: the whole UI. Keeps the conversation in the browser and parses the model's structured reply (score, feedback, next question).
- The server is stateless. The browser sends the history on every turn.
