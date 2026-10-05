---
title: I Built a Mock Interviewer for [FRIEND'S NAME] That Never Leaves My Laptop
tags: devchallenge, weekendchallenge, hf26challenge
---

[FRIEND'S NAME] has a placement interview coming up, and she told me the part she dreads most isn't the technical round. It's the silence right after "Tell me about yourself."

[REPLACE WITH YOUR TRUE STORY: one or two lines on who your friend is, what she's preparing for, and the moment you realised she needed this. Real detail beats polish here.]

So I built her a practice partner. It's called **Interview Buddy**.

## What it does

You pick the role and round (HR, technical, or mixed). It asks one question at a time, like a real panel would. After every answer you get:

- a score out of 10
- one thing that worked
- one thing to fix
- a stronger version of *your own* answer, not a generic template answer

At the end there's a short report: strengths, what to practise, and what to do this week.

[INSERT: screenshot or short screen recording of one full question and feedback round]

## Why open models were the whole point

Think about what someone says in a mock interview. Their weaknesses. Gaps in their projects. Nervous, half-formed answers they'd never say out loud to a stranger.

I didn't want any of that sitting on a server she doesn't control. Interview Buddy runs **Gemma through Ollama, entirely on a laptop**. No API key, no account, no per-message cost, and it works with the Wi-Fi off. She can fail badly at question one, try again, and nobody sees it.

A closed API would have worked technically. But "your practice answers never leave this machine" is a feature she can actually feel, and it only exists because the model is open and local.

## How it works

It's deliberately small:

- **Flask** serves one page and one endpoint.
- **Ollama** runs Gemma locally.
- The server is **stateless**. The browser sends the conversation history each turn.
- The model is told to answer in a strict format (`SCORE`, `WORKED`, `IMPROVE`, `STRONGER`, `NEXT QUESTION`), and the frontend parses it with a tolerant regex, because small models don't always follow formats perfectly.

Swapping models is one environment variable:

```
OLLAMA_MODEL=gemma3:12b python app.py
```

Small model for a weak laptop, bigger one for better feedback. That flexibility is the other thing a hosted API wouldn't give me.

[INSERT: link to your GitHub repo]

## The part I didn't expect

[FILL IN AFTER YOU TEST IT: what broke? Did the model ever repeat a question, score too kindly, or ramble? What did you change in the prompt? Honest failures make this section the best one in the post.]

## What she said

[FILL IN AFTER YOU HAND IT OVER: her actual words, her first reaction, what she asked you to change. The challenge gives bonus points for this, and it's what readers remember.]

## What's next

- Voice answers, so she can practise out loud
- Questions based on her own resume and projects
- Saving past sessions so she can see her scores improve

*Built for the Hacktoberfest Weekend Challenge: Build for a Friend.*
