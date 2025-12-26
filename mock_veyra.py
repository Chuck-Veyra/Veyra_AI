import random
from datetime import datetime, timedelta
import json

# --- SAFETY / CONFIG ---
SAFETY_RULES = {
    'max_daily_interventions': 3,
    'min_hours_between_subreddit': 6,
    'blacklisted_subreddits': ['politics', 'conspiracy'],
    'temperature_check': True
}

last_interventions = {}

# --- MOCK THREAD CLASS ---
class MockThread:
    def __init__(self, thread_id, title, selftext, subreddit, comments=0):
        self.id = thread_id
        self.title = title
        self.selftext = selftext
        self.subreddit = subreddit
        self.comments = comments
    def has_summon(self):
        text = (self.title + " " + self.selftext).lower()
        return "u/veyra" in text

# --- SIGNAL SCORING ---
def score_thread(thread):
    score = 0
    breakdown = {"explicit_summon":0, "density_penalty":0}

    if thread.has_summon():
        score += 50
        breakdown["explicit_summon"] = 50

    if thread.comments > 50:
        score -= 10
        breakdown["density_penalty"] = -10

    score = max(0, min(100, score))
    return score, breakdown

# --- ELIGIBILITY ---
def in_cooldown(subreddit):
    last_time = last_interventions.get(subreddit)
    if last_time:
        return datetime.now() - last_time < timedelta(hours=SAFETY_RULES['min_hours_between_subreddit'])
    return False

def should_intervene(thread):
    # Safety / blacklist / cooldown
    if thread.subreddit in SAFETY_RULES['blacklisted_subreddits']:
        return False, "Subreddit blacklisted"
    if in_cooldown(thread.subreddit):
        return False, "Cooldown active"

    score, breakdown = score_thread(thread)
    threshold = 50  # For summon-only
    probability = 1.0  # Always respond if summoned

    if breakdown["explicit_summon"] == 0:
        return False, "Not summoned"

    if score < threshold:
        return False, f"Score below threshold {score}"

    if random.random() > probability:
        return False, "Failed probability gate"

    return True, breakdown

# --- MOCK POST / LOG ---
def post_comment(thread, text):
    # Simulate posting
    print(f"Mock post to thread {thread.id} ({thread.subreddit}): {text}")
    return text

def log_intervention(thread, score, expression):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "thread_id": thread.id,
        "score": score,
        "intervention_type": "summon_response",
        "outcome": None,
        "lesson": "Mock run test"
    }
    print("Logging:", log_data)
    # Could append to JSON file here

# --- MOCK RUN ---
mock_threads = [
    MockThread("t1", "Need help with Python u/veyra", "How do I use classes?", "learnpython", 5),
    MockThread("t2", "Random thread", "No summon here", "learnpython", 10),
    MockThread("t3", "u/veyra check this out", "Testing summon", "test", 2),
]

for thread in mock_threads:
    intervene, reason = should_intervene(thread)
    if intervene:
        comment_text = "Hello! I am Veyra, here to clarify or teach. 😊"
        post_comment(thread, comment_text)
        last_interventions[thread.subreddit] = datetime.now()
        log_intervention(thread, 100, comment_text)
    else:
        print(f"Skipped thread {thread.id}: {reason}")
