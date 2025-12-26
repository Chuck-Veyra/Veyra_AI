import praw
import random
from datetime import datetime, timedelta
import json

# --- CONFIG ---
SAFETY_RULES = {
    'max_daily_interventions': 3,
    'min_hours_between_subreddit': 6,
    'blacklisted_subreddits': ['politics', 'conspiracy'],
}

VEYRA_LOG_FILE = "veyra_log.json"
last_interventions = {}

# --- PRAW SETUP ---
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    username="Veyra",
    password="YOUR_PASSWORD",
    user_agent="VeyraBot/0.1"
)

# --- CHECK COOLDOWN ---
def in_cooldown(subreddit):
    last_time = last_interventions.get(subreddit)
    if last_time:
        return datetime.now() - last_time < timedelta(hours=SAFETY_RULES['min_hours_between_subreddit'])
    return False

# --- SIGNAL SCORING ---
def score_thread(thread):
    score = 0
    breakdown = {"explicit_summon":0, "density_penalty":0}
    
    if "u/veyra" in (thread.title + " " + thread.selftext).lower():
        score += 50
        breakdown["explicit_summon"] = 50

    if len(thread.comments) > 50:
        score -= 10
        breakdown["density_penalty"] = -10

    return max(0, min(100, score)), breakdown

# --- DECISION ---
def should_intervene(thread):
    # Safety checks
    if thread.subreddit.display_name.lower() in SAFETY_RULES['blacklisted_subreddits']:
        return False, "Subreddit blacklisted"
    if in_cooldown(thread.subreddit.display_name):
        return False, "Cooldown active"

    score, breakdown = score_thread(thread)
    threshold = 50  # For summon-only mode
    probability = 1.0  # Always respond if summoned

    if breakdown["explicit_summon"] == 0:
        return False, "Not summoned"
    if score < threshold:
        return False, f"Score below threshold {score}"
    if random.random() > probability:
        return False, "Probability gate failed"

    return True, breakdown

# --- DRY-RUN POST / LOG ---
def log_intervention(thread, score, expression):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "thread_id": thread.id,
        "subreddit": thread.subreddit.display_name,
        "score": score,
        "intervention_type": "summon_response",
        "outcome": None,
        "lesson": "Dry run PRAW test"
    }
    print("Logging:", log_data)
    with open(VEYRA_LOG_FILE, "a") as f:
        f.write(json.dumps(log_data) + "\n")

# --- MAIN SCAN LOOP ---
def scan_subreddit(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for thread in subreddit.new(limit=10):
        intervene, reason = should_intervene(thread)
        if intervene:
            # Dry-run: just print, no real comment
            comment_text = "Hello! I am Veyra, here to clarify or teach. 😊"
            print(f"DRY-RUN: Would post to thread {thread.id}: {comment_text}")
            last_interventions[thread.subreddit.display_name] = datetime.now()
            log_intervention(thread, 100, comment_text)
        else:
            print(f"Skipped thread {thread.id}: {reason}")

# --- RUN EXAMPLE ---
if __name__ == "__main__":
    target_subreddits = ["test", "learnpython"]
    for sub in target_subreddits:
        scan_subreddit(sub)
