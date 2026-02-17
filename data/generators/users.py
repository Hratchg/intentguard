import random
import uuid
from datetime import datetime, timedelta

FIRST_NAMES = [
    "Alex", "Jordan", "Sam", "Morgan", "Taylor", "Casey", "Riley", "Quinn",
    "Avery", "Blake", "Cameron", "Dakota", "Emery", "Finley", "Harper", "Jamie",
    "Kai", "Logan", "Marley", "Nico", "Oakley", "Parker", "Reese", "Sage",
    "Tatum", "Val", "Wren", "Zion", "Drew", "Ellis", "Flynn", "Gray",
    "Hayden", "Indigo", "Jules", "Kit", "Lane", "Max", "Noel", "Onyx",
    "Phoenix", "Rain", "Sky", "Toni", "Uma", "Vesper", "Winter", "Xen",
    "Yael", "Zephyr",
]

LAST_NAMES = [
    "Chen", "Patel", "Kim", "Singh", "Nguyen", "Santos", "Rossi", "Muller",
    "Tanaka", "Ali", "Park", "Johansson", "Cohen", "Silva", "Garcia", "Okonkwo",
    "Dubois", "Ivanov", "Yamamoto", "Larsen", "Fernandez", "Bakshi", "Torres",
    "Schmidt", "Nakamura", "Bianchi", "Andersen", "Takahashi", "Chowdhury", "Petrov",
]

SCENARIO_WEIGHTS = {"churn": 0.25, "fraud": 0.15, "normal": 0.35, "confused": 0.25}
ACCOUNT_TYPES = ["free", "pro", "enterprise"]


def generate_users(count: int = 50, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    scenarios = list(SCENARIO_WEIGHTS.keys())
    weights = list(SCENARIO_WEIGHTS.values())
    base_date = datetime(2025, 6, 1)
    users = []

    for i in range(count):
        scenario = rng.choices(scenarios, weights=weights, k=1)[0]
        created = base_date + timedelta(days=rng.randint(0, 180))
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)

        users.append({
            "user_id": str(uuid.UUID(int=rng.getrandbits(128))),
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@example.com",
            "created_at": created.isoformat(),
            "account_type": rng.choice(ACCOUNT_TYPES),
            "scenario_tag": scenario,
        })

    return users
