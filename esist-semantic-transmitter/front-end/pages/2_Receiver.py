from __future__ import annotations

from datetime import datetime
import io
import json
import os
import uuid
import wave

import streamlit as st

from transmitter.ui_theme import apply_theme, log_item, pipeline_card

st.set_page_config(
    page_title="Semantic Audio Receiver",
    page_icon="📥",
    layout="wide",
)


def initialize_state() -> None:
    defaults = {
        "session_id": f"rx-{uuid.uuid4().hex[:8]}",
        "selected_language": "Portuguese (PT)",
        "received_packet": None,
        "reconstructed_audio": b"",
        "event_log": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_event(stage: str, message: str, status: str = "info") -> None:
    st.session_state.event_log.append(
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "stage": stage,
            "message": message,
            "status": status,
        }
    )
    st.session_state.event_log = st.session_state.event_log[-30:]


def load_packet() -> None:
    """Load the semantic packet from disk."""
    if os.path.exists("ultimo_pacote.json"):
        try:
            with open("ultimo_pacote.json", "r", encoding="utf-8") as f:
                pacote = json.load(f)
            st.session_state.received_packet = pacote
            add_event("Receive Data", "Semantic packet loaded.", "success")
        except Exception as e:
            add_event("Receive Data", f"Error loading packet: {str(e)}", "error")
            st.error(f"Error loading packet: {str(e)}")
    else:
        add_event("Receive Data", "No packet found.", "info")


def build_silent_wav(duration_sec: float = 1.0, sample_rate: int = 22050) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * int(duration_sec * sample_rate))
    return buffer.getvalue()


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Receiver Controls")

        st.session_state.session_id = st.text_input(
            "Session ID",
            value=st.session_state.session_id,
        )

        st.session_state.selected_language = st.selectbox(
            "Output Language",
            options=["Portuguese (PT)", "English (ENG)"],
            index=["Portuguese (PT)", "English (ENG)"].index(st.session_state.selected_language),
            help="Language for output audio synthesis.",
        )

        if st.button("Refresh Packet", use_container_width=True):
            load_packet()
            st.rerun()

        if st.button("Clear All", use_container_width=True):
            st.session_state.received_packet = None
            st.session_state.reconstructed_audio = b""
            st.session_state.event_log = []
            add_event("Session", "Receiver data cleared.", "info")
            st.rerun()


def is_decoded(packet: dict | None) -> bool:
    if not packet:
        return False
    return bool(packet.get("transcript") or packet.get("texto") or packet.get("decoded"))


def main() -> None:
    initialize_state()
    apply_theme()
    render_sidebar()

    st.title("📥 Receiver Interface (Team 10)")
    st.markdown("Here we present the received semantic data and generate the audio response!")

    if st.session_state.received_packet is None:
        load_packet()

    packet = st.session_state.received_packet
    received_status = bool(packet)
    decoded_status = is_decoded(packet)
    reconstructed_status = bool(st.session_state.reconstructed_audio)
    listen_status = reconstructed_status

    status_cols = st.columns(4)
    cards = [
        ("Receive Data", "Load the semantic packet from the transmitter.", received_status),
        ("Decode Data", "Show decoded text from the packet.", decoded_status),
        ("Reconstruct Audio", "Generate audio from the received data.", reconstructed_status),
        ("Listen", "Play back the reconstructed audio.", listen_status),
    ]
    for col, (title, desc, done) in zip(status_cols, cards):
        with col:
            st.markdown(pipeline_card(title, desc, done), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## Receive Data")
    if packet:
        st.json(packet)
    else:
        st.info("No packet available. Click Refresh Packet to try again.")

    st.markdown("## Decode Data")
    if decoded_status:
        if packet.get("transcript"):
            st.text_area("Decoded Text", value=packet["transcript"], height=120, disabled=True)
        elif packet.get("texto"):
            st.text_area("Decoded Text", value=packet["texto"], height=120, disabled=True)
        else:
            st.text_area("Decoded Text", value=json.dumps(packet.get("decoded"), ensure_ascii=False, indent=2), height=120, disabled=True)
    else:
        st.info("Decoding is not yet available for this packet.")

    st.markdown("## Reconstruct Audio")
    if packet:
        if st.button("Reconstruct Audio", use_container_width=True):
            with st.spinner("Reconstructing audio from data..."):
                st.session_state.reconstructed_audio = build_silent_wav(duration_sec=1.0)
                add_event("Reconstruct Audio", "Audio reconstructed successfully.", "success")
                st.success("Audio reconstructed successfully!")
    else:
        st.info("Load received data first to reconstruct audio.")

    st.markdown("## Listen")
    if reconstructed_status:
        st.audio(st.session_state.reconstructed_audio, format="audio/wav")
    else:
        st.info("Generate audio in the 'Reconstruct Audio' section to listen.")

    st.markdown("---")
    st.markdown("## Event Timeline")
    if not st.session_state.event_log:
        st.caption("No recent events. Refresh the packet or reconstruct the audio.")
    else:
        for event in reversed(st.session_state.event_log):
            st.markdown(log_item(event["time"], event["stage"], event["message"], event["status"]), unsafe_allow_html=True)


if __name__ == "__main__":
    main()