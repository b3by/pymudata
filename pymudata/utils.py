from .activity import Activity


def from_file(file_path, **kwargs):
    return Activity(file_path, **kwargs)
