from datetime import datetime, timedelta, timezone

def calculate_sm2_review(quality: int, previous_ef: float, repetitions: int, previous_interval: int) -> dict:
    """
    SuperMemo-2 (SM-2) Spaced Repetition Algorithm.
    quality: 0 (complete blackout) to 5 (perfect recall)
    """
    if quality >= 3:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = int(previous_interval * previous_ef)
        repetitions += 1
    else:
        repetitions = 0
        interval = 1

    ef = previous_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(ef, 1.3)
    next_review = datetime.now(timezone.utc) + timedelta(days=interval)

    return {
        "easiness_factor": round(ef, 3),
        "repetitions": repetitions,
        "interval": interval,
        "next_review": next_review.isoformat()
    }