from dataclasses import dataclass, field

@dataclass
class LiveData():
    liver_name: str
    live_title: str
    URL: str
    liver_tags: list = field(default_factory=list)

def __init__(self, liver_name = "", live_title = "", URL = "", liver_tags = []):
    self.liver_name = liver_name
    self.live_title = live_title
    self.URL = URL
    self.liver_tags = liver_tags

def mod_liver_name(live_data :LiveData, liver_name: str):
    live_data.liver_name = liver_name

def mod_liver_tags(live_data :LiveData, liver_tags: list):
    live_data.liver_tags.append(liver_tags)