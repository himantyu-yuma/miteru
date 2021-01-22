def diarization_s2t():
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()

    # speech_file = "for_transcribe/exp1/視線有1_01.wav"

    # with open(speech_file, "rb") as audio_file:
    #     content = audio_file.read()

    # audio = speech.RecognitionAudio(content=content)
    gcs_uri = "gs://exp1_eye1/exp1/視線有3.wav"
    output_file = gcs_uri.replace(
        'gs://exp1_eye1/', 'output/dialization/').replace('.wav', '.txt')

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=22050,
        language_code="ja-JP",
        enable_speaker_diarization=True,
        diarization_speaker_count=3,
    )

    print("Waiting for operation to complete...")
    operation = client.long_running_recognize(config=config, audio=audio)
    # response = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    # result = response.results[-1]
    with open(output_file, mode='w', encoding='utf-8') as f:
        for result in response.results:
            print(u"Transcript: {}".format(result.alternatives[0].transcript))
            print("Confidence: {}".format(result.alternatives[0].confidence))
            f.write(u"Transcript: {}\n".format(
                result.alternatives[0].transcript))
            f.write("Confidence: {}\n".format(result.alternatives[0].confidence))

            words_info = result.alternatives[0].words
            for word_info in words_info:
                print(
                    u"word: '{}', speaker_tag: {}".format(
                        word_info.word, word_info.speaker_tag)
                )
                f.write(
                    u"word: '{}', speaker_tag: {}\n".format(
                        word_info.word, word_info.speaker_tag)
                )

    # words_info = result.alternatives[0].words

    # # Printing out the output:
    # for word_info in words_info:
    #     print(
    #         u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
    #     )


def speaker_count():
    a = 0
    b = 0
    c = 0
    d = 0
    with open('output/dialization/exp1/視線有3.txt', mode='r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            if 'speaker_tag: 0' in line:
                a += 1
            elif 'speaker_tag: 1' in line:
                b += 1
            elif 'speaker_tag: 2' in line:
                c += 1
            elif 'speaker_tag: 3' in line:
                d += 1
            line = f.readline()
        print(a, b, c, d, sep='\n')


if __name__ == "__main__":
    diarization_s2t()
    speaker_count()
