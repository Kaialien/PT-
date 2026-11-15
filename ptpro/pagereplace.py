def fifo(pages, frames_count):
  frames = []
  trace = []
  faults = 0
  hits = 0

  for page in pages:
    if page in frames:
      hits += 1
      status = "HIT"
    else:
      faults += 1
      status = "FAULT"
      if len(frames) < frames_count:
        frames.append(page)
      else:
        frames.pop(0)
        frames.append(page)

    current = list(frames)
    while len(current) < frames_count:
      current.append("-")
    trace.append((page, current, status))

  return faults, hits, trace


def lru(pages, frames_count):
  frames = []
  recent = []
  trace = []
  faults = 0
  hits = 0

  for page in pages:
    if page in frames:
      hits += 1
      status = "HIT"
      recent.remove(page)
    else:
      faults += 1
      status = "FAULT"
      if len(frames) < frames_count:
        frames.append(page)
      else:
        oldest = recent.pop(0)
        idx = frames.index(oldest)
        frames[idx] = page

    recent.append(page)
    current = list(frames)
    while len(current) < frames_count:
      current.append("-")
    trace.append((page, current, status))

  return faults, hits, trace


def optimal(pages, frames_count):
  frames = []
  trace = []
  faults = 0
  hits = 0

  for i, page in enumerate(pages):
    if page in frames:
      hits += 1
      status = "HIT"
    else:
      faults += 1
      status = "FAULT"
      if len(frames) < frames_count:
        frames.append(page)
      else:
        farthest = -1
        replace_page = None
        for f in frames:
          try:
            next_use = pages[i + 1 :].index(f)
          except ValueError:
            next_use = float("inf")  # Never used again

          if next_use > farthest:
            farthest = next_use
            replace_page = f

        idx = frames.index(replace_page)
        frames[idx] = page

    current = list(frames)
    while len(current) < frames_count:
      current.append("-")
    trace.append((page, current, status))

  return faults, hits, trace

