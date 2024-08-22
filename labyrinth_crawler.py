import requests
import json
from typing import List
from collections import deque

# Goal
# ----
# You will be entering a maze filled with traps. Your goal is to get out of it!

# API
# ---
# ENDPOINT = "https://polyphonic-here-truly-coastal.trycloudflare.com/"
# The maze will be represented as an API with one GET endpoint.
# To enter the maze, head over to <ENDPOINT>
# To go to a specific step in the maze, GET /<STEP_ID>
# The final step of the maze will be a URL that returns a "CONGRATS" message

# Instructions
# ------------
# Print the STEP_ID of the final step


def get_step(step_id: str) -> List[str]:
    url = 'https://polyphonic-here-truly-coastal.trycloudflare.com/' + step_id

    retry_counter = 0
    limit = 100
    response = None
    while retry_counter < limit:
        response = requests.get(url)
        if response.status_code == 200:
            print(f'{step_id}, {response.elapsed.total_seconds()}')
            break
        retry_counter += 1
    
    step = json.loads(response.text)
    if 'message' in step:
        return [step['message']]
    return step['next_steps']


def crawl() -> str:
    queue = deque([''])
    visited = set()

    while queue:
        step = queue.popleft()
        visited.add(step)
        neighbors = get_step(step)

        if len(neighbors) == 1 and neighbors[0] == 'CONGRATS':
            return step

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
    
    return ''


print(crawl())
