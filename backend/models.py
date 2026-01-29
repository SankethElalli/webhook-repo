def format_push(payload):
    return {
        "type": "PUSH",
        "author": payload["pusher"]["name"],
        "from_branch": None,
        "to_branch": payload["ref"].split("/")[-1],
        "timestamp": payload["head_commit"]["timestamp"]
    }

def format_pull_request(payload):
    return {
        "type": "PULL_REQUEST",
        "author": payload["pull_request"]["user"]["login"],
        "from_branch": payload["pull_request"]["head"]["ref"],
        "to_branch": payload["pull_request"]["base"]["ref"],
        "timestamp": payload["pull_request"]["created_at"]
    }

def format_merge(payload):
    return {
        "type": "MERGE",
        "author": payload["pull_request"]["merged_by"]["login"],
        "from_branch": payload["pull_request"]["head"]["ref"],
        "to_branch": payload["pull_request"]["base"]["ref"],
        "timestamp": payload["pull_request"]["merged_at"]
    }
