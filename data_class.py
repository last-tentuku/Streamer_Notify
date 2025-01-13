from dataclasses import dataclass, field

@dataclass
class LiveData():
    liver_name: str
    live_title: str
    URL: str
    liver_tags: list = field(default_factory=list)

def __init__(self, liver_name, live_title, URL, liver_tags = []):
    self.liver_name = liver_name
    self.live_title = live_title
    self.URL = URL
    self.liver_tags = liver_tags
