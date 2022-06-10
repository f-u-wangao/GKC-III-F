import wave
import pyaudio
from aip import AipSpeech

APP_ID = '26199800'
API_KEY = 'tuXojuF6LrTfGYAvcwdCSZAh'
SECRET_KEY = 'BtzG3CUntAHth0fgUVFgvsiUvsQFoU47'


def audio_record(filename, rec_time):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 16000  # Record at 16000 samples per second

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording...')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for rec_time
    for i in range(0, int(fs / chunk * rec_time)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def play(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)

    data = wf.readframes(chunk)  # 读取数据
    print(data)
    while data != b'':  # 播放
        stream.write(data)
        data = wf.readframes(chunk)
        # print('while循环中！')
        # print(data)
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def record_and_recognize(filePath, rec_time):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    audio_record(filePath, rec_time)
    fb = client.asr(get_file_content(filePath),
                    'wav', 16000, {'dev_pid': 1537})
    return fb['result'][0]


def string_match(str):
    print("语音识别结果：", str)
    controlWords = []
    with open('controlWords.txt', encoding='utf-8') as file:
        content = file.readlines()
        for row in content:
            tmp_list = row.split(' ')
            tmp_list[-1] = tmp_list[-1].replace('\n', '')   # 去掉换行符
            controlWords.append(tmp_list[0])

    for word in controlWords:
        if str.find(word) != -1:
            print("匹配的命令：", word)
            return word
    print("没有可以匹配的命令!")
    return None


def voiceControl(filePath, rec_time):
    string_match(record_and_recognize(filePath, rec_time))


if __name__ == '__main__':

    filePath = 'records/recordForControl.wav'
    rec_time = 3

    voiceControl(filePath, rec_time)
