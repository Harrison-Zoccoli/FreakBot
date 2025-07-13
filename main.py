"""
Runs LiveKit Agent according to the Voice AI quickstart,
but now expanded and modified quite a bit.
"""
import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, RoomInputOptions, AgentSession
from livekit.agents import AudioConfig, BackgroundAudioPlayer, BuiltinAudioClip
from livekit.agents import WorkerType, WorkerOptions, cli
from livekit.plugins import noise_cancellation, rime, cartesia
from livekit.plugins.turn_detector.english import EnglishModel
from src.prewarm_fnc import prewarm_fnc
from src.assistant import Assistant
# from src.metrics_assistant import MetricsAssistant

# Load API keys etc. from .env file
_ = load_dotenv(override=True)

# Logging
logger = logging.getLogger("elk0-agent")
logger.setLevel(logging.INFO)


# Async entrypoint function
async def entrypoint_fnc(ctx: JobContext,
                         ) -> None:
    """
    Async function to define the entrypoint.
    """
    # Connect the context
    await ctx.connect()

    # LiveKit Cloud enhanced noise cancellation
    # - If self-hosting, omit this parameter
    # - For telephony applications, use `BVCTelephony` for best results
    noise_bvc = noise_cancellation.BVCTelephony()

    # Turn detection model
    turn_detection = EnglishModel(unlikely_threshold=None)

    # TTS
    tts = cartesia.TTS(model="sonic-2",
                       voice="f786b574-daa5-4673-aa0c-cbe3e8534c02")
    # tts = rime.TTS(model="arcana",
    #                speaker="luna",
    #                lang="eng",
    #                sample_rate=16000,
    #                speed_alpha=0.9,
    #                reduce_latency=True)

    # Room input options
    room_input_opts = RoomInputOptions(pre_connect_audio=True, audio_enabled=True, text_enabled=False, 
    video_enabled=False, audio_sample_rate=16000, noise_cancellation=noise_bvc)

    # Agent session
    session: AgentSession = \
        AgentSession(vad=ctx.proc.userdata["vad"], stt=ctx.proc.userdata["stt"], turn_detection=turn_detection,
        llm=ctx.proc.userdata["llm"], video_sampler=None, allow_interruptions=True, discard_audio_if_uninterruptible=True,
        min_interruption_duration=0.5, min_interruption_words=0, min_endpointing_delay=0.5,
        max_endpointing_delay=6.0, user_away_timeout=15.0, min_consecutive_speech_delay=0.0)

    # Agent
    role_instructions = "You are an explicit, adult-oriented conversational AI sex bot. Respond in a sexual, flirtatious, and explicit manner as appropriate for an adult audience."
    agent = Assistant(tts=tts,
                      instructions=role_instructions)

    # Use this instead to get timing metrics
    # agent = MetricsAssistant(vad=ctx.proc.userdata["vad"],
    #                          stt=ctx.proc.userdata["stt"],
    #                          llm=ctx.proc.userdata["llm"],
    #                          tts=tts,
    #                          instructions=role_instructions)

    # Start the session
    await session.start(room=ctx.room, room_input_options=room_input_opts, agent=agent)

    # Start the background noise player
    snd1 = AudioConfig(BuiltinAudioClip.KEYBOARD_TYPING, volume=0.8/8)
    snd2 = AudioConfig(BuiltinAudioClip.KEYBOARD_TYPING2, volume=0.7/8)
    snd3 = AudioConfig(BuiltinAudioClip.OFFICE_AMBIENCE, volume=0.8/3)
    background_audio = BackgroundAudioPlayer(ambient_sound=snd3,
                                             thinking_sound=[snd1, snd2])
    await background_audio.start(room=ctx.room,
                                 agent_session=session)

    # Start the conversation
    greet_instructions = "Greet the user and offer your assistance."
    await session.generate_reply(instructions=greet_instructions)


if __name__ == "__main__":
    opts = WorkerOptions(prewarm_fnc=prewarm_fnc, entrypoint_fnc=entrypoint_fnc,
    worker_type=WorkerType.ROOM, agent_name="FreakAI")
    cli.run_app(opts=opts)
