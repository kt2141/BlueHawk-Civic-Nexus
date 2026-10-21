from dataclasses import dataclass
from typing import Dict

EMERGENCY_KEYWORDS = {
    "gun", "weapon", "fight", "attack", "robbery", "theft", "molestation",
    "fire", "explosion", "bomb", "assault", "violence", "panic", "crime"
}

MUNICIPAL_KEYWORDS = {
    "garbage", "waste", "drain", "drainage", "sewage", "streetlight", "pothole",
    "waterlogging", "pollution", "dump", "sanitation", "mosquito", "smoke"
}

NEGATIVE_SENTIMENT_HINTS = {
    "urgent", "immediately", "danger", "unsafe", "severe", "critical", "help"
}


@dataclass
class RoutingDecision:
    category: str
    priority: str
    reason: str



def route_complaint(text: str) -> RoutingDecision:
    clean = " ".join(text.lower().split())
    tokens = set(clean.replace(".", " ").replace(",", " ").split())

    emergency_hits = tokens.intersection(EMERGENCY_KEYWORDS)
    municipal_hits = tokens.intersection(MUNICIPAL_KEYWORDS)
    urgency_hits = tokens.intersection(NEGATIVE_SENTIMENT_HINTS)

    if emergency_hits:
        return RoutingDecision(
            category="Emergency",
            priority="High",
            reason=f"Matched emergency keywords: {', '.join(sorted(emergency_hits))}",
        )

    if municipal_hits:
        priority = "Medium" if urgency_hits else "Normal"
        return RoutingDecision(
            category="Municipal",
            priority=priority,
            reason=f"Matched municipal keywords: {', '.join(sorted(municipal_hits))}",
        )

    return RoutingDecision(
        category="Municipal",
        priority="Normal",
        reason="No emergency keywords detected; defaulting to municipal triage.",
    )


if __name__ == "__main__":
    samples = [
        "There is a fight with weapons near the market, urgent help needed",
        "Overflowing drain and garbage in Ward 12 after rain",
        "Streetlight not working on MG Road",
    ]
    for complaint in samples:
        decision = route_complaint(complaint)
        print({"complaint": complaint, **decision.__dict__})
