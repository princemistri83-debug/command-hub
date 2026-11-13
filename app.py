import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import random

# પેજ સેટિંગ્સ
st.set_page_config(page_title="J.A.R.V.I.S. Command Hub", page_icon="⚡", layout="centered")

# ડાર્ક અને ફ્યુચરિસ્ટિક UI સ્ટાઇલ
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1e293b;
        color: #38bdf8;
        border: 1px solid #38bdf8;
        font-weight: bold;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #38bdf8;
        color: #0f172a;
    }
    .transcript-user {
        background-color: #0284c7;
        color: white;
        padding: 8px 12px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .transcript-ai {
        background-color: #334155;
        color: #f8fafc;
        padding: 8px 12px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
        border-left: 3px solid #38bdf8;
    }
    .quote-box {
        background-color: #1e293b;
        border: 1px dashed #38bdf8;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-style: italic;
        color: #38bdf8;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# સેસન સ્ટેટ
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'call_history' not in st.session_state:
    st.session_state.call_history = []
if 'contacts' not in st.session_state:
    st.session_state.contacts = {
        "મમ્મી / ઘર (+91 98765 00001)": "Erwin Smith",
        "બેસ્ટ ફ્રેન્ડ (+91 98765 00002)": "Floch Forster",
        "બિઝનેસ / ઓફિસ (+91 98765 00003)": "Johan Liebert",
        "અજાણ્યો નંબર (+91 99999 88888)": "Eren Yeager"
    }

# ઓટોમેટિક બ્રાઉઝર વોઇસ (TTS) ફંક્શન
def speak_voice(text, pitch=1.0, rate=1.0):
    clean_text = text.replace('"', '').replace("'", "")
    js_code = f"""
    <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{clean_text}");
        msg.pitch = {pitch};
        msg.rate = {rate};
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# કેરેક્ટર ડેટાબેઝ
CHARACTERS = {
    "Erwin Smith": {
        "pitch": 0.75, "rate": 0.95,
        "greeting": "My soldiers, do not buckle or yield! Tell me, what is the situation on your end?",
        "replies": [
            "We must look beyond the walls of this problem. Give your heart and move forward!",
            "A good commander always has a backup plan. Tell me your next move.",
            "Sacrifice is necessary for victory. Stay focused on your goal."
        ],
        "quotes": ["Give your heart! (Shinzo wo Sasageyo)", "If we don't fight, we can't win."]
    },
    "Floch Forster": {
        "pitch": 1.05, "rate": 1.1,
        "greeting": "Listen carefully! Only a devil can save us now. Why are you calling?",
        "replies": [
            "We don't have time for hesitation. Crush the obstacles in front of you!",
            "I will do whatever it takes to ensure our survival and success.",
            "If you don't fight, you can't win. Tell me what needs to be done."
        ],
        "quotes": ["Only the devils can save Eldia!", "Someone has to become a monster."]
    },
    "Eren Yeager": {
        "pitch": 0.85, "rate": 1.0,
        "greeting": "I keep moving forward... until all my enemies are destroyed. Speak.",
        "replies": [
            "Because I was born into this world, I am free to choose my own path.",
            "Stop waiting for someone else to save you. Take control right now.",
            "Tatakae. Fight. That is the only answer."
        ],
        "quotes": ["I will keep moving forward, until my enemies are destroyed.", "Tatakae! Fight!"]
    },
    "Johan Liebert": {
        "pitch": 0.90, "rate": 0.85,
        "greeting": "The only thing all humans are equal in is death... Tell me, what is your deepest wish?",
        "replies": [
            "Look at me... Look at how large the monster inside me has become.",
            "People are so easy to manipulate when you know what they fear most.",
            "Everything is going exactly according to the scenario I wrote."
        ],
        "quotes": ["The only thing all humans are equal in... is death.", "Do you see the monster inside?"]
    },
    "Orochimaru": {
        "pitch": 0.65, "rate": 0.90,
        "greeting": "Kukuku... How fascinating. What brings you to my hideout today?",
        "replies": [
            "True power comes from knowing all the secrets of this world.",
            "Humans are merely fragile vessels, yet their ambition is quite entertaining.",
            "Tell me what you desire, and perhaps I shall grant you forbidden knowledge."
        ],
        "quotes": ["Everything in this world is meaningless unless you master it.", "Kukuku... fascinating."]
    },
    "Askeladd": {
        "pitch": 0.80, "rate": 1.0,
        "greeting": "Oi, listen up kid. Better make this quick, my time isn't cheap.",
        "replies": [
            "Stop whining and use your head! A real warrior survives by wit, not just strength.",
            "Everyone is a slave to something. Make sure you are the one holding the chains.",
            "Not bad. Now show me how you actually plan to pull this off."
        ],
        "quotes": ["Everyone's a slave to something.", "A real warrior needs no sword."]
    }
}

st.title("⚡ J.A.R.V.I.S. Command Hub")
st.markdown("<p style='text-align:center; color:#94a3b8;'>એનિમે વોઇસ કોલ સિમ્યુલેટર & સ્માર્ટ નોટ્સ હબ</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📞 Anime Voice Call", "📜 Anime Quote Vault", "📝 Smart Notes"])

# ==========================================
# TAB 1: ANIME VOICE CALL (AUTO SPEAK MODE)
# ==========================================
with tab1:
    st.subheader("📲 એનિમે કેરેક્ટર ઓટો-કોલ સિમ્યુલેટર")
    
    selected_contact = st.selectbox("કોનો કોલ આવી રહ્યો છે / કોને કોલ કરવો છે?", list(st.session_state.contacts.keys()))
    default_char = st.session_state.contacts[selected_contact]
    
    active_character = st.selectbox(
        "એક્ટિવ એનિમે કેરેક્ટર:", 
        list(CHARACTERS.keys()), 
        index=list(CHARACTERS.keys()).index(default_char)
    )

    st.markdown("🎵 **Background Vibe:** `Epic OST Active 🎧`")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("📞 ઇનકમિંગ કોલ ઉપાડો (Start Call)"):
            char_data = CHARACTERS[active_character]
            greeting = char_data["greeting"]
            st.session_state.call_history.append(("AI", active_character, greeting))
            speak_voice(greeting, char_data["pitch"], char_data["rate"])
            
    with col_c2:
        if st.button("🔴 કોલ કટ કરો (Clear Log)"):
            st.session_state.call_history = []
            st.info("કોલ ડિસ્કનેક્ટ થયો.")

    st.markdown("---")
    
    user_speech = st.text_input("🎙️ તમે કોલમાં જે લખશો તે સામે કેરેક્ટર ઓટોમેટિક બોલશે (ટાઇપ કરીને એન્ટર દબાવો):", key="user_input_box")

    if user_speech:
        last_msg = st.session_state.call_history[-1][2] if st.session_state.call_history else ""
        if last_msg != user_speech:
            st.session_state.call_history.append(("User", "તમે (You)", user_speech))
            char_data = CHARACTERS[active_character]
            ai_reply = random.choice(char_data["replies"])
            st.session_state.call_history.append(("AI", active_character, ai_reply))
            speak_voice(ai_reply, char_data["pitch"], char_data["rate"])

    if st.session_state.call_history:
        st.markdown("### 📝 લાઈવ કોલ સબટાઇટલ્સ (Live Transcript)")
        for sender, name, msg in st.session_state.call_history:
            if sender == "User":
                st.markdown(f"<div class='transcript-user'><b>{name}:</b> {msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='transcript-ai'><b>🎭 {name}:</b> {msg}</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: ANIME QUOTE VAULT
# ==========================================
with tab2:
    st.subheader("📜 એનિમે માસ્ટરમાઇન્ડ કોટ્સ વૉલ્ટ")
    quote_char = st.selectbox("કેરેક્ટર પસંદ કરો:", list(CHARACTERS.keys()), key="quote_char_select")
    
    if st.button("✨ પાવરફુલ કોટ જનરેટ કરો"):
        selected_quotes = CHARACTERS[quote_char]["quotes"]
        chosen_quote = random.choice(selected_quotes)
        speak_voice(chosen_quote, CHARACTERS[quote_char]["pitch"], CHARACTERS[quote_char]["rate"])
        st.markdown(f"<div class='quote-box'><b>{quote_char}:</b><br>“{chosen_quote}”</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: SMART NOTES
# ==========================================
with tab3:
    st.subheader("📝 સ્માર્ટ નોટ્સ અને કેલ્ક્યુલેટર")
    
    cmd = st.text_input("💬 નોંધ લખો (દા.ત. 'note: પ્રોજેક્ટ પૂરો કરવો') અથવા ગણતરી કરો (દા.ત. '250 * 12'):")
    if st.button("▶️ પ્રોસેસ કરો"):
        if cmd.lower().startswith("note:"):
            note_text = cmd[5:].strip()
            st.session_state.notes.append(note_text)
            st.success(f"નોટ સેવ થઈ ગઈ: {note_text}")
        elif any(op in cmd for op in ['+', '-', '*', '/']):
            try:
                ans = eval(cmd)
                st.success(f"ગણતરીનો જવાબ: {ans}")
            except:
                st.error("ગણતરીમાં ભૂલ છે.")
        else:
            st.info(f"ઇનપુટ સેવ થયું: {cmd}")

    if st.session_state.notes:
        st.markdown("### 📋 તમારી સેવ કરેલી નોટ્સ")
        for idx, n in enumerate(st.session_state.notes, 1):
            st.write(f"{idx}. {n}")
