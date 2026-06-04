"""
Meta Ad Copy Scoring Engine
============================
Scores D2C brand ad copies across 6 direct-response marketing dimensions.
Author: MBA Marketing Portfolio Project
"""

import re
import pandas as pd
from ad_copy_data import AD_COPIES


# ─────────────────────────────────────────────
# SCORING DIMENSIONS & LOGIC
# ─────────────────────────────────────────────

def score_hook_strength(copy: str) -> float:
    """
    Hook = first sentence / opening line.
    Scores: question openers, pattern interrupts, bold claims, 'you' usage,
    numbers/stats, provocative statements.
    Max: 20 pts
    """
    score = 0
    first_sentence = copy.split(".")[0].lower()

    if "?" in first_sentence:                          score += 5   # question hook
    if any(w in first_sentence for w in ["you", "your"]):  score += 4   # personalisation
    if re.search(r"\d+", first_sentence):              score += 4   # number/stat
    if any(w in first_sentence for w in [
        "stop", "why", "what if", "still", "never", "wrong",
        "mistake", "truth", "secret", "lied", "don't"
    ]):                                                score += 4   # pattern interrupt
    if len(first_sentence.split()) >= 6:               score += 3   # substantial opener
    return min(score, 20)


def score_problem_agitation(copy: str) -> float:
    """
    PAS (Problem-Agitate-Solve) detection.
    Looks for pain points, frustration language, contrast setups.
    Max: 20 pts
    """
    score = 0
    text = copy.lower()

    pain_words = [
        "still", "struggle", "problem", "breaking out", "wrong", "tired",
        "hate", "frustrated", "can't", "doesn't work", "costing", "battle",
        "excuse", "lied", "without", "despite", "starving", "scarred"
    ]
    agitate_words = [
        "never", "years", "every day", "always", "keeps", "still",
        "even though", "no matter", "keeps failing"
    ]

    pain_count = sum(1 for w in pain_words if w in text)
    agitate_count = sum(1 for w in agitate_words if w in text)

    score += min(pain_count * 4, 12)
    score += min(agitate_count * 4, 8)
    return min(score, 20)


def score_offer_clarity(copy: str) -> float:
    """
    Checks for: price mention, discount/offer, free shipping, returns policy,
    promo code, urgency element.
    Max: 20 pts
    """
    score = 0
    text = copy.lower()

    if re.search(r"₹\s?\d+", copy):                   score += 5   # price anchor
    if re.search(r"\d+%\s*off|use code|promo", text): score += 4   # discount
    if "free shipping" in text or "free delivery" in text: score += 3  # shipping
    if "refund" in text or "return" in text or "money back" in text: score += 3  # risk reversal
    if any(w in text for w in [
        "tonight", "limited", "ends", "only", "sale", "flash", "hours"
    ]):                                                score += 3   # urgency
    if re.search(r"first order|first50|firstbite", text): score += 2  # first-time incentive
    return min(score, 20)


def score_cta_strength(copy: str) -> float:
    """
    Clear, specific CTA vs vague 'click here'.
    Max: 15 pts
    """
    score = 0
    text = copy.lower()

    strong_ctas = [
        "shop now", "buy now", "order now", "try", "start", "get yours",
        "use code", "watch", "swipe", "find yours", "switch to"
    ]
    weak_ctas = ["click", "shop", "check out", "buy", "order"]

    if any(c in text for c in strong_ctas):            score += 10
    elif any(c in text for c in weak_ctas):            score += 5
    if re.search(r"in \d+ (days|minutes|hours)", text): score += 5   # delivery specificity
    return min(score, 15)


def score_social_proof_credibility(copy: str) -> float:
    """
    Any form of proof: numbers sold, certifications, testimonial language,
    dermatologist tested, transformation claims with data.
    Max: 15 pts
    """
    score = 0
    text = copy.lower()

    if re.search(r"\d[\d,]+\s*(units|kits|customers|women|people|sold|reviews)", text):
        score += 6   # volume proof
    if any(w in text for w in [
        "dermatologist", "clinically", "certified", "tested", "doctor"
    ]):                                                score += 5
    if re.search(r"\d+\s*(days|weeks|months)", text):  score += 4   # time-bound claim
    if any(w in text for w in [
        "transformation", "results", "works", "actually", "actually works"
    ]):                                                score += 3
    return min(score, 15)


def score_brand_voice_differentiation(copy: str) -> float:
    """
    Penalises generic language. Rewards: specific POV, tone consistency,
    category disruption language, personality.
    Max: 10 pts
    """
    score = 10   # start full, deduct for generic sins
    text = copy.lower()

    generic_phrases = [
        "best", "great", "good", "quality guaranteed", "available",
        "affordable", "everyone", "all orders", "click the link",
        "limited time offer", "natural ingredients"
    ]
    deductions = sum(1 for p in generic_phrases if p in text)
    score -= min(deductions * 2, 8)

    # Reward personality/POV
    if any(w in text for w in ["damn", "actually", "we're done", "your ex", "biryani", "cardboard"]):
        score += 2

    return max(score, 0)


def score_ad_copy(ad: dict) -> dict:
    """Run all 6 scorers on one ad and return enriched dict."""
    copy = ad["copy"]

    hook          = score_hook_strength(copy)
    problem       = score_problem_agitation(copy)
    offer         = score_offer_clarity(copy)
    cta           = score_cta_strength(copy)
    proof         = score_social_proof_credibility(copy)
    voice         = score_brand_voice_differentiation(copy)
    total         = hook + problem + offer + cta + proof + voice

    # Word count
    word_count = len(copy.split())

    return {
        **ad,
        "Hook Strength"         : hook,
        "Problem Agitation"     : problem,
        "Offer Clarity"         : offer,
        "CTA Strength"          : cta,
        "Social Proof"          : proof,
        "Brand Voice"           : voice,
        "Total Score"           : total,
        "Word Count"            : word_count,
        "Score %"               : round(total / 100 * 100, 1),
    }


def run_engine() -> pd.DataFrame:
    results = [score_ad_copy(ad) for ad in AD_COPIES]
    df = pd.DataFrame(results)
    df = df.sort_values("Total Score", ascending=False).reset_index(drop=True)
    df.index += 1   # rank from 1
    return df


if __name__ == "__main__":
    df = run_engine()
    print("\n📊 TOP 10 AD COPIES\n" + "="*60)
    print(df[["brand","category","format","funnel_stage","Total Score","Score %"]].head(10).to_string())
    print("\n📉 BOTTOM 5 AD COPIES\n" + "="*60)
    print(df[["brand","category","format","funnel_stage","Total Score","Score %"]].tail(5).to_string())
