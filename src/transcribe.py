# !/usr/bin/env python

# [START transcribe]
from __future__ import division

import re
import sys

# [prameter]------------------->
IS_ROS_ACTIVE = True
# <-----------------------------
if IS_ROS_ACTIVE:
    import rospy
    from std_msgs.msg import String
    from std_msgs.msg import Bool

# どの質問か考慮するやつ
import consider

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

End_flug = False
google_start_sub = False


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

class CallApi(object):
    def __init__(self):
        rospy.init_node('speech_recog')
        rospy.loginfo("Init_node 'speech_recog' ")

        # ROS Subscriber
        self.google_start_sub = rospy.Subscriber('conversation/start', Bool, self.conversationCB)
        # ROS Publisher
        self.google_stop_pub = rospy.Publisher('conversation/stop', Bool, queue_size = 1)

        self.loop_time = 0

    def conversationCB(self, msg):
        self.google_start_sub = msg.data

    def listen_print_loop(self, responses):
        cons = consider.distance()

        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)
                break

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break

                num_chars_printed = 0

        return cons.check(transcript + overwrite_chars)

    def google_speech_api(self):
        # See http://g.co/cloud/speech/docs/languages
        # for a list of supported languages.
        language_code = 'en-US'  # a BCP-47 language tag

        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            self.End_flug = self.listen_print_loop(responses) # Bool

    def conversation(self):
        loop_time = 0
        while not rospy.is_shutdown():
            if loop_time == 4:
                break

            if self.google_start_sub:
                rospy.loginfo("Wating for topic...")
                rospy.sleep(1.5)

            else:
                rospy.loginfo("Subscribed 'conversation/start' Topic")
                try:
                    self.google_speech_api()

                except rospy.ROSInterruptException:
                    rospy.loginfo("Interrupted")
                    pass

                else:
                    if self.End_flug:
                        loop_time+=1
                        rospy.loginfo("Published 'conversation/stop' Topic")
                        self.google_stop_pub.publish(False)
                        self.google_start_sub = True
                        rospy.sleep(1.5)
                    else:
                        continue

if __name__ == '__main__':
    loop_time = 0
    call = CallApi()
    call.conversation()

# [END transcribe]
