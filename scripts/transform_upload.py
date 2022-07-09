from tempfile import SpooledTemporaryFile

import librosa
import noisereduce as nr
from pyspark.shell import spark
from threading import Thread
import pandas as pd
import boto3
from logger import get_logger

_logger = get_logger("TransformUpload")
_logger.debug("Loaded successfully!")


class TransformUpload:
    def __init__(self, audio_text_pair):
        try:
            self.s3_client = boto3.client('s3')
            self.s3_resource = boto3.resource('s3')
            self.data_frame = spark.createDataFrame(audio_text_pair, ['transcription', 'audio_data'])

        except Exception as e:
            _logger.exception(e)

    def detect_remove_silence(self):
        audio, sr = librosa.load(self.data_frame, sr=8000, mono=True)
        clips = librosa.effects.split(audio, top_db=10)
        wav_data = []
        for c in clips:
            data = audio[c[0]: c[1]]
            wav_data.extend(data)
        return wav_data

    def remove_noise(self):
        audio, sr = librosa.load(self.data_frame, sr=8000, mono=True)
        reduced_noise = nr.reduce_noise(y=self.data_frame, sr=sr, n_std_thresh_stationary=1.5, stationary=True)

        return reduced_noise

    def validate_audio(self):
        pass

    def store_on_s3(self, temp_file: SpooledTemporaryFile):
        try:
            self.s3_client.upload_fileobj(
                Fileobj=temp_file, Bucket='bucket_name', Key='file_name', ExtraArgs={'ACL': 'public-read'})

            _logger.info('File uploaded to s3')

        except Exception as e:
            _logger.exception(e)

    def run_all(self):
        if __name__ == '__main__':
            Thread(target=self.detect_remove_silence).start()
            Thread(target=self.remove_noise).start()
            Thread(target=self.validate_audio).start()
            Thread(target=self.store_on_s3).start()


# transform_upload = TransformUpload([
#     ('transcription', 'audio_data'),
#     ('transcription', 'audio_data'),
#     ('transcription', 'audio_data')
# ])
# transform_upload.run_all()
