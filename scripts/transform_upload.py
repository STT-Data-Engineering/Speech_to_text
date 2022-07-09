from tempfile import SpooledTemporaryFile
import librosa
import noisereduce as nr
import boto3
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType


def remove_noise(audio_file):
    audio, sr = librosa.load(audio_file, sr=8000, mono=True)
    reduced_noise = nr.reduce_noise(audio_file, sr=sr, n_std_thresh_stationary=1.5, stationary=True)

    return reduced_noise


def detect_remove_silence(audio_file):
    audio, sr = librosa.load(audio_file, sr=8000, mono=True)
    clips = librosa.effects.split(audio, top_db=10)
    wav_data = []
    for c in clips:
        data = audio[c[0]: c[1]]
        wav_data.extend(data)
    return wav_data


class TransformUpload:
    def __init__(self, audio_text_pair):
        try:
            self.spark_session = SparkSession.builder.appName('speech_to_text').getOrCreate()
            self.columns = StructType([StructField('transcription', StringType(), False),
                                       StructField('audio_data', StringType(), False)])
            self.emp_rdd = self.spark_session.sparkContext.emptyRDD()
            self.s3_client = boto3.client('s3')
            self.s3_resource = boto3.resource('s3')
            self.data_frame = self.spark_session.createDataFrame(audio_text_pair, ['transcription', 'audio_data'])
            self.clean_data_frame = self.spark_session.createDataFrame(data=self.emp_rdd, schema=self.columns)

        except Exception as e:
            print(e)

    def remove_noise_silence(self):
        df_collect = self.data_frame.collect()
        for audio_text_data in df_collect:
            # load the audio file
            audio_file = audio_text_data['audio_data']
            # remove silence
            silence_removed_audio_file = detect_remove_silence(audio_file)
            # remove noise
            no_noise_audio_file = remove_noise(silence_removed_audio_file)

            row_to_add = [[audio_text_data['transcription'], no_noise_audio_file]]
            added_df = self.spark_session.createDataFrame(row_to_add, self.columns)
            pandas_added = added_df.toPandas()
            self.clean_data_frame = self.clean_data_frame.toPandas()
            self.clean_data_frame = self.clean_data_frame.append(pandas_added, ignore_index=True)
            self.clean_data_frame = self.spark_session.createDataFrame(self.clean_data_frame)

        return self.clean_data_frame.collect()

    def validate_audio(self):
        pass

    def store_on_s3(self, temp_file: SpooledTemporaryFile):
        try:
            self.s3_client.upload_fileobj(
                Fileobj=temp_file, Bucket='bucket_name', Key='file_name', ExtraArgs={'ACL': 'public-read'})

        except Exception as e:
            print(e)


# transform_upload = TransformUpload([
#     ('transcription', 'audio_data'),
#     ('transcription', 'audio_data'),
#     ('transcription', 'audio_data')
# ])
# transform_upload.remove_noise_silence()
