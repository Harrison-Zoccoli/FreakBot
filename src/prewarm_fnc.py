"""
This has the prewarm function for the LiveKit Assistant.
This pre-loads the various external plugins (STT, TTS, LLM, etc.).
"""
from livekit.agents import JobProcess
from livekit.plugins import silero, deepgram, openai

__all__ = ["prewarm_fnc"]


# Prewarm function
def prewarm_fnc(proc: JobProcess,
                ) -> None:
    """
    Non-async prep before entrypoint.
    This initializes the component models (STT, LLM, TTS, etc.).
    """
    # Silero VAD
    proc.userdata["vad"] = silero.VAD.load(sample_rate=16000,
                                           min_speech_duration=0.05,
                                           min_silence_duration=0.55,
                                           prefix_padding_duration=0.5,
                                           max_buffered_speech=60.0,
                                           activation_threshold=0.5,
                                           force_cpu=True)

    # STT
    proc.userdata["stt"] = deepgram.STT(model="nova-3",
                                        language="en-US",
                                        detect_language=False,
                                        keyterms=[],
                                        sample_rate=16000,
                                        endpointing_ms=25,
                                        interim_results=True,
                                        punctuate=True,
                                        smart_format=True,
                                        numerals=False,
                                        no_delay=True,
                                        filler_words=True,
                                        profanity_filter=False,
                                        mip_opt_out=True)

    # LLM
    proc.userdata["llm"] = openai.LLM(model="gpt-4o-mini",
                                      client=None)
