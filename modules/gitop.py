import subprocess

def fetch_tags():
    subprocess.run(['git', 'pull', '--tags']) #fetch remote tags

def get_remote_tags():
    fetch_tags()
    tags = list()
    tags = subprocess.run(['git', 'tag'], capture_output=True, text=True).stdout #get stdout as string
    tags = tags.split()
    return tags

def get_latest_hash():
    tags = list()
    tags = subprocess.run(['git', 'ls-remote', '--heads', url], capture_output=True, text=True).stdout #get stdout as string
    tags = tags.split('\t')
    tags = tags[:1]
    return tags