class Annotation:
    start_time: int
    end_time: int
    text: str

    def __init__(self,
                 start_time: int,
                 end_time: int,
                 text: str = None
                 ):
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
