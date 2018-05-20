from django.db import models


# Create your models here.


class FastaData:
    def __init__(self, value: str):
        self.value = value


class AlignmentNode:
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

    def as_json(self):
        return dict(
            input_label=self.label,
            input_value=self.value)
