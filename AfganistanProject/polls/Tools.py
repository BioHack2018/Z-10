from polls.models import AlignmentNode
import json
from django.core import serializers


class MyTools:

    @staticmethod
    def parse_alignment(filename):
        arrayResult = []
        with open(filename) as f:
            next(f)
            for i, line in enumerate(f):
                if line != "\n":
                    if not line.strip()[0] == "*":
                        arrayResult.append(line.strip())

        for i, v in enumerate(arrayResult):
            if i != 0 and i % 6 == 0:
                arrayResult.insert(i - 1, " ")

        finalResult = []

        for i, v in enumerate(arrayResult):
            vp = v.split(" ")
            if len(vp)>2:
                finalResult.append(AlignmentNode(vp[0], vp[len(vp)-1]))
            else:
                finalResult.append(AlignmentNode('', ''))

        for v in finalResult:
            print(v.label)

        return finalResult
