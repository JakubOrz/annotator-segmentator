import xml.etree.ElementTree as Et
from .Annotation import Annotation

from typing import List, Union


class Tier:
    annotator: str
    linquistic_type_ref: str
    participant: str
    tier_id: Union[int, str]
    annotations: List['Annotation']

    def __init__(self,
                 annotator: str = "Segmentator2",
                 linquistic_type_ref: str = "default-lt",
                 participant: str = "Speaker",
                 tier_id="Tier0"):
        self.annotator = annotator
        self.linquistic_type_ref = linquistic_type_ref
        self.participant = participant
        self.tier_id = tier_id
        self.annotations = list()

    def add_annotation(self, annotation: Annotation):
        self.annotations.append(annotation)

    def toXML(self, time_orders: dict) -> Et.Element:
        root: Et.Element = Et.Element('TIER',
                                      attrib={'ANNOTATOR': self.annotator,
                                              'LINGUISTIC_TYPE_REF': self.linquistic_type_ref,
                                              'PARTICIPANT': self.participant,
                                              'TIER_ID': self.tier_id
                                              }
                                      )
        for i, a in enumerate(self.annotations):
            value: Et.Element = Et.Element('ANNOTATION_VALUE')
            alignable_annotation: Et.Element = Et.Element('ALIGNABLE_ANNOTATION', attrib={
                'ANNOTATION_ID': f"a_{self.tier_id}_{i}",
                'TIME_SLOT_REF1': time_orders.get(a.start_time),
                'TIME_SLOT_REF2': time_orders.get(a.end_time)
            })
            annotation = Et.Element('ANNOTATION')

            value.text = None
            alignable_annotation.append(value)
            annotation.append(alignable_annotation)

            root.append(annotation)
        return root
