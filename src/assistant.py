"""
Makes LiveKit Agent according to the Voice AI quickstart:
https://docs.livekit.io/agents/start/voice-ai
"""
from livekit.agents import Agent
from livekit.agents.vad import VAD
from livekit.agents.stt import STT
from livekit.agents.llm import LLM
from livekit.agents.tts import TTS
from livekit.agents.types import NOT_GIVEN, NotGivenOr

__all__ = ["Assistant"]


class Assistant(Agent):
    """
    Class for an Assistant.
    For now, this is just a LiveKit Agent with basic
    instructions to play the role of an Assistant.

    Optionally, VAD, STT, LLM and TTS can be overridden.

    However, VAD and STT are intimate to the AgentSession
    and logically belong there (apply only once per caller).
    Thus, in practice, only give the LLM and/or TTS, which
    are logically associated with each Agent uniquely.
    """
    def __init__(self,
                 vad: NotGivenOr[VAD | None] = NOT_GIVEN,
                 stt: NotGivenOr[STT | None] = NOT_GIVEN,
                 llm: NotGivenOr[LLM | None] = NOT_GIVEN,
                 tts: NotGivenOr[TTS | None] = NOT_GIVEN,
                 instructions: str = "You are an attractive ",
                 ) -> None:
        """
        vad: optional VAD to override the AgentSession VAD
        stt: optional STT to override the AgentSession STT
        llm: optional LLM to override the AgentSession LLM
        tts: optional TTS to override the AgentSession TTS
        instructions: str to give to the Agent (e.g. for role)
        """
        super().__init__(instructions=instructions,
                         vad=vad,
                         stt=stt,
                         llm=llm,
                         tts=tts)
