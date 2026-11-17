from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Data structures

@dataclass
class Step:
    """One row of the trace = what happened for ONE page reference."""
    step: int                 
    page: str                 
    frames: List[str]        
    status: str               
    replaced: Optional[str]   

@dataclass
class Result:
    algorithm: str
    frames_count: int
    total_refs: int
    hits: int
    faults: int
    hit_ratio: float          
    fault_ratio: float        
    final_frames: List[str]
    trace: List[Step] = field(default_factory=list)

    @property
    def hit_percent(self) -> float:
        return self.hit_ratio * 100

    @property
    def fault_percent(self) -> float:
        return self.fault_ratio * 100

#input validation

def parse_reference_string(text: str) -> List[str]:
    
    pages = text.replace(",", " ").split()
    if not pages:
        raise ValueError("Reference string cannot be empty.")
    return pages


def validate_inputs(pages: List[str], frames_count) -> int:
    
    if not pages:
        raise ValueError("Reference string cannot be empty.")
    try:
        frames_count = int(frames_count)
    except (TypeError, ValueError):
        raise ValueError("Number of frames must be a whole number.")
    if frames_count < 1:
        raise ValueError("Number of frames must be at least 1.")
    return frames_count