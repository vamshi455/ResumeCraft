"""
Rules Engine - Load and apply matching rules
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class MatchingRulesEngine:
    """Engine for loading and applying matching rules"""

    def __init__(self, rules_path: Optional[Path] = None):
        """
        Initialize the rules engine

        Args:
            rules_path: Path to rules JSON file. If None, uses default location.
        """
        if rules_path is None:
            rules_path = Path(__file__).parent.parent / "config" / "matching_rules.json"

        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from JSON file"""
        try:
            with open(self.rules_path, 'r') as f:
                rules = json.load(f)
                logger.info(f"Loaded matching rules version {rules.get('version', 'unknown')}")
                return rules
        except Exception as e:
            logger.error(f"Failed to load matching rules: {e}")
            # Return default rules
            return self._get_default_rules()

    def _get_default_rules(self) -> Dict[str, Any]:
        """Return default rules if loading fails"""
        return {
            "matching_weights": {
                "skills": {"weight": 0.30},
                "experience": {"weight": 0.25},
                "location": {"weight": 0.20},
                "education": {"weight": 0.10},
                "soft_skills": {"weight": 0.08},
                "culture_fit": {"weight": 0.07}
            }
        }

    def get_matching_weights(self) -> Dict[str, float]:
        """Get current matching weights"""
        weights = {}
        for key, config in self.rules["matching_weights"].items():
            weights[key] = config["weight"]
        return weights

    def get_location_compatibility_score(
        self,
        job_location: str,
        candidate_preference: str,
        willing_to_relocate: bool = False
    ) -> Tuple[int, str]:
        """
        Calculate location compatibility score

        Args:
            job_location: Job location type (Remote/Hybrid/Onsite/Flexible)
            candidate_preference: Candidate's location preference
            willing_to_relocate: Whether candidate is willing to relocate

        Returns:
            Tuple of (score, reasoning)
        """
        # Normalize inputs
        job_location = job_location.strip().title()
        candidate_preference = candidate_preference.strip().title()

        # Find matching rule
        location_rules = self.rules["location_rules"]["compatibility_matrix"]["rules"]

        matching_rule = None
        for rule in location_rules:
            if (rule["job_location"] == job_location and
                rule["candidate_preference"] == candidate_preference):
                matching_rule = rule
                break

        if matching_rule is None:
            logger.warning(f"No matching rule found for {job_location} + {candidate_preference}")
            return 50, "No specific rule found - using default score"

        base_score = matching_rule["score"]
        reasoning = matching_rule["reasoning"]

        # Apply relocation bonus if applicable
        if (willing_to_relocate and
            self.rules["location_rules"]["relocation"]["enabled"] and
            base_score < 70):
            bonus = self.rules["location_rules"]["relocation"]["rules"]["willing_to_relocate"]["score_boost"]
            base_score = min(100, base_score + bonus)
            reasoning += f" (+{bonus} bonus for willingness to relocate)"

        return base_score, reasoning

    def get_experience_score_adjustment(
        self,
        candidate_years: float,
        required_years: float,
        is_senior_role: bool = False
    ) -> Tuple[int, str]:
        """
        Calculate experience score adjustment

        Args:
            candidate_years: Candidate's years of experience
            required_years: Required years for the job
            is_senior_role: Whether this is a senior-level position

        Returns:
            Tuple of (adjustment, reasoning)
        """
        gap = candidate_years - required_years
        exp_rules = self.rules["experience_rules"]

        if gap <= -2:
            # Significantly underqualified
            adjustment = exp_rules["underqualified"]["penalty"]
            reasoning = exp_rules["underqualified"]["reasoning"]
        elif gap == -1:
            # Slightly underqualified
            adjustment = exp_rules["slightly_underqualified"]["penalty"]
            reasoning = exp_rules["slightly_underqualified"]["reasoning"]
        elif gap >= 5:
            # Overqualified
            adjustment = exp_rules["overqualified"]["penalty"]
            reasoning = exp_rules["overqualified"]["reasoning"]
        elif gap >= 2:
            # Exceeds requirement
            adjustment = exp_rules["exceeds_requirement"]["bonus"]
            reasoning = exp_rules["exceeds_requirement"]["reasoning"]
        else:
            # Meets requirement
            adjustment = 0
            reasoning = exp_rules["meets_requirement"]["reasoning"]

        return adjustment, reasoning

    def calculate_weighted_score(self, component_scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall score

        Args:
            component_scores: Dictionary of component scores (0-100 each)
                Keys: skills, experience, location, education, soft_skills, culture_fit

        Returns:
            Weighted overall score (0-100)
        """
        weights = self.get_matching_weights()
        total_score = 0.0

        for component, score in component_scores.items():
            if component in weights:
                weight = weights[component]
                total_score += score * weight
            else:
                logger.warning(f"Unknown component: {component}")

        return round(total_score, 1)

    def get_recommendation(
        self,
        overall_score: float,
        confidence: float = 100.0
    ) -> Dict[str, str]:
        """
        Get hiring recommendation based on score

        Args:
            overall_score: Overall match score (0-100)
            confidence: Confidence in the match (0-100)

        Returns:
            Dictionary with recommendation, level, and action
        """
        thresholds = self.rules["scoring_thresholds"]

        for level, config in thresholds.items():
            if config["min_score"] <= overall_score <= config["max_score"]:
                return {
                    "level": level,
                    "recommendation": config["recommendation"],
                    "action": config["action"],
                    "score_range": f"{config['min_score']}-{config['max_score']}"
                }

        # Default fallback
        return {
            "level": "unknown",
            "recommendation": "REVIEW REQUIRED",
            "action": "Manual review needed",
            "score_range": "N/A"
        }

    def should_auto_reject(
        self,
        location_score: float,
        skills_match: float,
        experience_gap: float,
        willing_to_relocate: bool,
        is_senior_role: bool
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if candidate should be auto-rejected

        Args:
            location_score: Location compatibility score (0-100)
            skills_match: Skills match percentage (0-100)
            experience_gap: Years difference from requirement
            willing_to_relocate: Whether candidate willing to relocate
            is_senior_role: Whether this is a senior position

        Returns:
            Tuple of (should_reject, reason)
        """
        if not self.rules["filters"]["auto_reject_rules"]["enabled"]:
            return False, None

        # Check location incompatibility
        if location_score < 30 and not willing_to_relocate:
            return True, "Location incompatibility with no relocation option"

        # Check insufficient skills
        if skills_match < 40:
            return True, "Insufficient technical skills for role"

        # Check experience gap for senior roles
        if experience_gap < -3 and is_senior_role:
            return True, "Significant experience gap for senior role"

        return False, None

    def get_skills_weight_breakdown(self) -> Dict[str, float]:
        """Get breakdown of required vs preferred skills weights"""
        skills_rules = self.rules["skills_rules"]
        return {
            "required": skills_rules["required_skills"]["weight"],
            "preferred": skills_rules["preferred_skills"]["weight"],
            "minimum_required_match": skills_rules["minimum_required_match"]["threshold"]
        }

    def validate_rules(self) -> Tuple[bool, list]:
        """
        Validate that rules are consistent

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check that weights sum to ~1.0
        weights = self.get_matching_weights()
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            errors.append(f"Weights sum to {total_weight:.2f}, should be 1.0")

        # Check that score thresholds don't overlap
        thresholds = self.rules["scoring_thresholds"]
        ranges = []
        for level, config in thresholds.items():
            ranges.append((config["min_score"], config["max_score"], level))

        ranges.sort()
        for i in range(len(ranges) - 1):
            if ranges[i][1] >= ranges[i+1][0]:
                errors.append(f"Threshold overlap: {ranges[i][2]} and {ranges[i+1][2]}")

        return len(errors) == 0, errors


def get_rules_engine() -> MatchingRulesEngine:
    """Get singleton instance of rules engine"""
    global _rules_engine_instance

    if '_rules_engine_instance' not in globals():
        _rules_engine_instance = MatchingRulesEngine()

    return _rules_engine_instance


# Example usage and testing
if __name__ == "__main__":
    # Test the rules engine
    engine = MatchingRulesEngine()

    print("=== Matching Weights ===")
    weights = engine.get_matching_weights()
    for key, weight in weights.items():
        print(f"{key}: {weight:.1%}")

    print("\n=== Location Compatibility Examples ===")
    scenarios = [
        ("Remote", "Remote", False),
        ("Onsite", "Remote", False),
        ("Onsite", "Remote", True),
        ("Hybrid", "Hybrid", False),
    ]

    for job_loc, cand_pref, willing in scenarios:
        score, reasoning = engine.get_location_compatibility_score(
            job_loc, cand_pref, willing
        )
        print(f"{job_loc} + {cand_pref} (relocate={willing}): {score}/100")
        print(f"  → {reasoning}")

    print("\n=== Experience Score Adjustments ===")
    exp_scenarios = [
        (3, 5, False),  # Underqualified
        (5, 5, False),  # Meets
        (7, 5, False),  # Exceeds
        (10, 5, False),  # Overqualified
    ]

    for cand_years, req_years, is_senior in exp_scenarios:
        adj, reasoning = engine.get_experience_score_adjustment(
            cand_years, req_years, is_senior
        )
        print(f"Candidate: {cand_years}y, Required: {req_years}y → {adj:+d}")
        print(f"  → {reasoning}")

    print("\n=== Weighted Score Calculation ===")
    component_scores = {
        "skills": 85,
        "experience": 90,
        "location": 100,
        "education": 100,
        "soft_skills": 75,
        "culture_fit": 80
    }

    overall = engine.calculate_weighted_score(component_scores)
    print(f"Component scores: {component_scores}")
    print(f"Weighted overall score: {overall}/100")

    recommendation = engine.get_recommendation(overall)
    print(f"Recommendation: {recommendation['recommendation']}")
    print(f"Action: {recommendation['action']}")

    print("\n=== Rules Validation ===")
    is_valid, errors = engine.validate_rules()
    if is_valid:
        print("✅ Rules are valid")
    else:
        print("❌ Rules have errors:")
        for error in errors:
            print(f"  - {error}")
