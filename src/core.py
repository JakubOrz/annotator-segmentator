import xml.etree.ElementTree as Et
import os
import math
from datetime import datetime
from config import Config
from models import Annotation, Tier, Informations
from scipy.io import wavfile

TEMPLATE_FILE = "data/eaf_templates/eaf_template_2.eaf"


class EafFile:
    def __init__(self, wav_file: str, output_file: str):
        self.tree: Et.ElementTree = Et.parse(TEMPLATE_FILE)
        root: Et.Element = self.tree.getroot()
        root.attrib['AUTHOR'] = 'Jakub_O_segmentation_generator'
        root.attrib['DATE'] = datetime.now().isoformat()
        self.tiers = 1

        self.wav_file = self.hook_wav_file(wav_file)
        self.output_file = output_file

    def hook_wav_file(self, fileName: str) -> str:

        if not os.path.isfile(fileName):
            raise FileNotFoundError("Nie ma takiego pliku")
        if not fileName.lower().endswith('.wav'):
            raise FileNotFoundError("Podany plik nie jest typu wav")

        media_descriptor: Et.Element = self.tree.getroot().find('HEADER').find('MEDIA_DESCRIPTOR')
        media_descriptor.attrib['MEDIA_URL'] = f"file://{os.path.abspath(fileName)}"
        media_descriptor.attrib['RELATIVE_MEDIA_URL'] = fileName
        return fileName

    def add_time_order(self, time_order: dict):
        time_orders: Et.Element = self.tree.getroot().find('TIME_ORDER')
        for time_stamp, tag_name in time_order.items():
            time_orders.append(Et.Element('TIME_SLOT', attrib={
                'TIME_SLOT_ID': tag_name,
                'TIME_VALUE': str(time_stamp)
            }))

    def add_tier(self, tier: Et.Element):
        self.tree.getroot().insert(2 + self.tiers, tier)
        self.tiers += 1

    def add_informations(self, informations: Informations):
        time_orders = informations.pepare_time_order()
        self.add_time_order(time_orders)
        for tier in informations.tiers:
            self.add_tier(tier.toXML(time_orders))

    def save_file(self, fileName: str):
        if fileName.endswith(".eaf"):
            self.tree.write(fileName)
        else:
            self.tree.write(f"{fileName}.eaf")

    def collect_data_3(self) -> Informations:
        samplerate, data = wavfile.read(self.wav_file)

        milisecond_rate = samplerate // 1000
        issilent: bool = True

        config: Config = Config()

        MAX_SILENT_PATIENCE = config.get_colelctor_option('max_silent_patience') * milisecond_rate
        MAX_LOUD_PATIENCE = config.get_colelctor_option('max_loud_patience') * milisecond_rate
        LOUND_POINT = config.get_colelctor_option('loud_point')
        LEFT_CORRECTION = config.get_colelctor_option('left_correction') * milisecond_rate
        RIGHT_CORRECTION = config.get_colelctor_option('right_correction') * milisecond_rate

        tier_names: list = config.get_annotator_option('tiers_names')
        annotator = config.get_annotator_option('annotator_name')
        start = 0
        end = 0

        informations: Informations = Informations()
        for channel in range(0, 2):
            tier: Tier = Tier(tier_id=tier_names[channel],
                              participant=tier_names[channel],
                              annotator=annotator)

            # Przechodzenie po kanale
            patience = 30
            for i, sample in enumerate(data):
                if issilent:
                    if math.fabs(sample[channel]) > LOUND_POINT:
                        if patience <= 0:
                            start = (i // milisecond_rate) - LEFT_CORRECTION
                            issilent = False
                            patience = MAX_SILENT_PATIENCE

                        else:
                            patience -= 1
                    else:
                        patience = MAX_LOUD_PATIENCE
                else:
                    if math.fabs(sample[channel]) < LOUND_POINT:
                        if patience <= 0:
                            end = (i // milisecond_rate) - RIGHT_CORRECTION
                            tier.add_annotation(Annotation(
                                start_time=start,
                                end_time=end)
                            )
                            issilent = True
                            patience = MAX_LOUD_PATIENCE
                        else:
                            patience -= 1
                    else:
                        patience = MAX_SILENT_PATIENCE
            informations.addTier(tier)
        return informations

    def start_processing(self) -> dict:
        self.add_informations(self.collect_data_3())
        self.save_file(self.output_file)
        return {'success': True}

