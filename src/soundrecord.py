import os
import wave
import time
import json
import logging
import os.path
import pyaudio

logger = logging.getLogger(__name__)
logger.setLevel(10)

audio = pyaudio.PyAudio()  # Create an interface to PortAudio


class Record(object):
    def __init__(self, chans, samp_rate, chunk, record_secs, dev_index) -> None:
        self.wav_output_filename = str(time.strftime("%Y%m%d-%H%M%S")) + ".wav"
        # self.wav_output_filename = time.strftime("%Y%m%d-%H%M%S")
        self.dirName = 'AudioFiles'
        self.chans = chans
        self.samp_rate = samp_rate
        self.chunk = chunk
        self.record_secs = record_secs
        self.dev_index = dev_index
        self.form_1 = pyaudio.paInt16
        self.frames = []

    def isavailable(self):
        if not os.path.isdir(self.dirName):
            os.mkdir(self.dirName)
        path = os.path.join(self.dirName, self.wav_output_filename)
        return path

    def makeStream(self) -> None:
        stream = audio.open(format=self.form_1,
                            rate=self.samp_rate,
                            channels=self.chans,
                            input_device_index=self.dev_index,
                            input=True,
                            frames_per_buffer=self.chunk
                            )
        logger.info("Audio is being Recorded..")

        for _ in range(0, int((self.samp_rate/self.chunk)*self.record_secs)):
            data = stream.read(self.chunk)
            self.frames.append(data)

        logger.info("Audio has Finished Recording..")

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def saveFile(self):
        path = self.isavailable()
        wavefile = wave.open(path, 'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()
        return path


def convertToParam() -> None:
    path = './config/configuration.json'
    with open(path) as f:
        return json.load(f)


# Helper Function
def main() -> None:
    params = convertToParam()
    print(params)
    obj = Record(
        int(params['chans']),
        int(params["samp_rate"]),
        int(params["chunk"]),
        int(params["record_secs"]),
        int(params["dev_index"])
    )
    print(obj)
    obj.makeStream()
    obj.saveFile()


if __name__ == '__main__':
    main()
    print('Audio Saved.')
