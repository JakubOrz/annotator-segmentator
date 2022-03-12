import xml.etree.ElementTree as Et


class TimeOrder:
    times: dict

    def __init__(self, times: dict):
        self.times = times

    def toXML(self) -> Et.Element:
        root: Et.Element = Et.Element('TIME_ORDER')
        for time_stamp, tag_name in self.times.items():
            root.append(Et.Element('TIME_SLOT', attrib={
                'TIME_SLOT_ID': tag_name,
                'TIME_VALUE': str(time_stamp)
            }))
        return root
