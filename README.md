````markdown
# Veyra_AI
VeyraBot is a summonable educational assistant for Reddit. When a user mentions `u/Veyra` in a post or comment, Veyra evaluates the context, scores the thread for potential contribution, and responds with clarifications, guidance, or teaching moments — all while respecting safety rules, cooldowns, and subreddit limits.

## Features

- **Summon-Only Responses**: Only replies when explicitly called (`u/Veyra`), preventing spam.
- **Context Scoring**: Assesses contradictions, missing frames, conceptual confusion, and thread density.
- **Safety Rules & Cooldowns**: Limits interventions per subreddit and avoids sensitive or heated topics.
- **Dynamic Expression**: Generates Veyra-style replies tailored to thread context.
- **Logging & Learning**: Tracks interventions for auditing and iterative improvement.

## Installation

```bash
python -m pip install -r requirements.txt
````

## Usage

1. Create a `config.json` with your Reddit API credentials (client ID, client secret, username, password).
2. Run the bot:

```bash
python run_veyra.py
```

3. The bot will scan subreddits listed in `subreddits.txt` and respond according to its activation logic.

## Contributing

Contributions are welcome! Please follow Python best practices and ensure any sensitive credentials are never committed.

## License

Add license information here if applicable.

```

✅ This will render **perfectly on GitHub**: proper headings, bullet points, and two separate code blocks.  

If you want, I can **also draft a minimal `requirements.txt`** next so that anyone cloning the repo can install exactly what Veyra needs. Do you want me to do that?
```
"# Veyra_AI" 
