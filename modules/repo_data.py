
default_conf = "repo.cnf"
default_tags = "clones.lis"

def load_conf(path=default_conf):
    conf = list()
    with open(path, mode='r') as f:
        conf = [i.strip() for i in f.readlines()]
    return conf

def get_version(path=default_conf):
    conf = load_conf(path)
    return str(conf[1])

def get_url(path=default_conf):
    conf = load_conf(path)
    return conf[3]

def get_branch(path=default_conf):
    conf = load_conf(path)
    return conf[5]

def get_path(path=default_conf):
    conf = load_conf(path)
    return conf[7]

def get_ignore_past(path=default_conf):
    conf = load_conf(path)
    return False if conf[9] == "GetAll" else True

def get_cloned(path=default_tags):
    conf = list()
    with open(path, mode='r') as f:
        conf = [i.strip() for i in f.readlines()]
    return conf

def save_cloned(list, path=default_tags):
    with open(path, mode='a') as f:
        f.write('\n'.join([""] + tags))