from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Step:
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

def _padded(frames: List[str], frames_count: int) -> List[str]:
    return list(frames) + ["-"] * (frames_count - len(frames))


def fifo(pages, frames_count):
    frames, trace = [], []
    faults, hits = 0, 0
    for page in pages:
        if page in frames:
            hits += 1
            status = "H"
        else:
            faults += 1
            status = "F"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
        current = _padded(frames, frames_count)
        trace.append((page, current, status))
    return faults, hits, trace

def lru(pages, frames_count):
    frames, recent, trace = [], [], []
    faults, hits = 0, 0
    for page in pages:
        if page in frames:
            hits += 1
            status = "H"
            recent.remove(page)
        else:
            faults += 1
            status = "F"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                oldest = recent.pop(0)
                frames[frames.index(oldest)] = page
        recent.append(page)
        current = _padded(frames, frames_count)
        trace.append((page, current, status))
    return faults, hits, trace

def optimal(pages, frames_count):
    frames, trace = [], []
    faults, hits = 0, 0
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "H"
        else:
            faults += 1
            status = "F"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                farthest = -1
                replace_page = None
                for f in frames:
                    try:
                        next_use = pages[i + 1 :].index(f)
                    except ValueError:
                        next_use = float("inf")
                    if next_use > farthest:
                        farthest = next_use
                        replace_page = f
                frames[frames.index(replace_page)] = page
        current = _padded(frames, frames_count)
        trace.append((page, current, status))
    return faults, hits, trace