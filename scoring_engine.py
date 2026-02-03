from constants import ROLE_WEIGHTS

def compute_score(section_scores, role):
    w = ROLE_WEIGHTS[role]
    return round(
        section_scores["skills_score"] * w["skills"] +
        section_scores["experience_score"] * w["experience"] +
        section_scores["projects_score"] * w["projects"] +
        section_scores["clarity_score"] * w["clarity"],
        2
    )
