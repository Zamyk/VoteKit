import numpy as np
from votekit.pref_profile.approval_profile import ApprovalProfile

def for_all_manipulations(profile: ApprovalProfile, index_of_manipulator: int, function_to_call) -> None:
    """
    Iterates through all possible approval ballots for the manipulator in-place,
    calling function_to_call(profile) on each.
    If function_to_call returns False, the iteration stops early.
    Temporarily unlocks and then restores the writeability flag of the profile's votes array.
    """
    candidates = profile.candidates
    n_cands = len(candidates)
    
    original_vote = profile.votes[index_of_manipulator].copy()
    
    profile.votes.flags.writeable = True
    
    try:
        for mask in range(1 << n_cands):
            new_vote_vec = np.array([(mask >> i) & 1 for i in range(n_cands)], dtype=bool)
            profile.votes[index_of_manipulator] = new_vote_vec
            
            if not function_to_call(profile):
                break
    finally:
        profile.votes[index_of_manipulator] = original_vote
        profile.votes.flags.writeable = False
