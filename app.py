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
    .call-box {
        background-color: #1e293b;
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
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
    </style>
""", unsafe_allow_html=True)

# સેસન સ્ટેટ (નોટ્સ અને કોલ હિસ્ટ્રી સેવ રાખવા માટે)
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

# બ્રાઉઝર વોઇસ (Text-to-Speech) ફંક્શન
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

# કેરેક્ટર ડેટાબેઝ (પર્સનાલિટી, વોઇસ પિચ અને ડાયલોગ્સ)
CHARACTERS = {
    "Erwin Smith": {
        "pitch": 0.75, "rate": 0.95,
        "greeting": "My soldiers, do not buckle or yield! Tell me, what is the situation on your end?",
        "replies": [
            "We must look beyond the walls of this problem. Give your heart and move forward!",
            "A good commander always has a backup plan. Tell me your next move.",
            "Sacrifice is necessary for victory. Stay focused on your goal."
        ]
    },
    "Floch Forster": {
        "pitch": 1.05, "rate": 1.1,
        "greeting": "Listen carefully! Only a devil can save us now. Why are you calling?",
        "replies": [
            "We don't have time for hesitation. Crush the obstacles in front of you!",
            "I will do whatever it takes to ensure our survival and success.",
            "If you don't fight, you can't win. Tell me what needs to be done."
        ]
    },
    "Eren Yeager": {
        "pitch": 0.85, "rate": 1.0,
        "greeting": "I keep moving forward... until all my enemies are destroyed. Speak.",
        "replies": [
            "Because I was born into this world, I am free to choose my own path.",
            "Stop waiting for someone else to save you. Take control right now.",
            "Tatakae. Fight. That is the only answer."
        ]
    },
    "Johan Liebert": {
        "pitch": 0.90, "rate": 0.85,
        "greeting": "The only thing all humans are equal in is death... Tell me, what is your deepest wish?",
        "replies": [
            "Look at me... Look at how large the monster inside me has become.",
            "People are so easy to manipulate when you know what they fear most.",
            "Everything is going exactly according to the scenario I wrote."
        ]
    },
    "Orochimaru": {
        "pitch": 0.65, "rate": 0.90,
        "greeting": "Kukuku... How fascinating. What brings you to my hideout today?",
        "replies": [
            "True power comes from knowing all the secrets of this world.",
            "Humans are merely fragile vessels, yet their ambition is quite entertaining.",
            "Tell me what you desire, and perhaps I shall grant you forbidden knowledge."
        ]
    },
    "Askeladd": {
        "pitch": 0.80, "rate": 1.0,
        "greeting": "Oi, listen up kid. Better make this quick, my time isn't cheap.",
        "replies": [
            "Stop whining and use your head! A real warrior survives by wit, not just strength.",
            "Everyone is a slave to something. Make sure you are the one holding the chains.",
            "Not bad. Now show me how you actually plan to pull this off."
        ]
    }
}

st.title("⚡ J.A.R.V.I.S. Command Hub")
st.markdown("<p style='text-align:center; color:#94a3b8;'>સ્માર્ટ AI આસિસ્ટન્ટ & એનિમે વોઇસ કોલ સિમ્યુલેટર</p>", unsafe_allow_html=True)

# બે મુખ્ય ટેબ: ૧. સ્માર્ટ કમાન્ડ્સ, ૨. એનિમે વોઇસ કોલ
tab1, tab2 = st.tabs(["📞 Anime Voice Call", "⚡ સ્માર્ટ કમાન્ડ્સ"])

# ==========================================
# TAB 1: ANIME VOICE CALL & LIVE SUBTITLES
# ==========================================
with tab1:
    st.subheader("📲 કોન્ટેક્ટ અને એનિમે કેરેક્ટર સેટઅપ")
    
    # નવો નંબર અને કેરેક્ટર લિંક કરવા માટે
    with st.expander("➕ નવો કોન્ટેક્ટ નંબર ઉમેરો / બદલો"):
        new_name_num = st.text_input("કોન્ટેક્ટ નામ અને નંબર (દા.ત. રાજ +91 9825012345):")
        assigned_char = st.selectbox("આ નંબર માટે કયું કેરેક્ટર સેટ કરવું છે?", list(CHARACTERS.keys()), key="new_assign")
        if st.button("કોન્ટેક્ટ સેવ કરો"):
            if new_name_num:
                st.session_state.contacts[new_name_num] = assigned_char
                st.success(f"સેવ થઈ ગયું: {new_name_num} -> {assigned_char}")

    # કોલ સિલેક્શન
    selected_contact = st.selectbox("કોનો કોલ આવી રહ્યો છે / કોને કોલ કરવો છે?", list(st.session_state.contacts.keys()))
    default_char = st.session_state.contacts[selected_contact]
    
    active_character = st.selectbox(
        "એક્ટિવ એનિમે વોઇસ કેરેક્ટર (તમે બદલી પણ શકો છો):", 
        list(CHARACTERS.keys()), 
        index=list(CHARACTERS.keys()).index(default_char)
    )

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
            st.info("કોલ ડિસ્કનેક્ટ થયો અને સબટાઇટલ લોગ ક્લિયર થયો.")

    # લાઈવ વાતચીત / સબટાઇટલ ઇનપુટ
    st.markdown("---")
    user_speech = st.text_input("🎙️ તમે કોલમાં શું બોલો છો? (અહીં લખો, સામે કેરેક્ટર વોઇસમાં જવાબ આપશે):")
    if st.button("🗣️ બોલો (Send Voice Reply)"):
        if user_speech:
            st.session_state.call_history.append(("User", "તમે (You)", user_speech))
            char_data = CHARACTERS[active_character]
            ai_reply = random.choice(char_data["replies"])
            st.session_state.call_history.append(("AI", active_character, ai_reply))
            speak_voice(ai_reply, char_data["pitch"], char_data["rate"])

    # લાઈવ સબટાઇટલ્સ સ્ક્રીન
    if st.session_state.call_history:
        st.markdown("### 📝 લાઈવ કોલ સબટાઇટલ્સ (Live Transcript)")
        for sender, name, msg in st.session_state.call_history:
            if sender == "User":
                st.markdown(f"<div class='transcript-user'><b>{name}:</b> {msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='transcript-ai'><b>🎭 {name}:</b> {msg}</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: J.A.R.V.I.S. SMART COMMANDS
# ==========================================
with tab2:
    st.subheader("⚡ ક્વિક સ્માર્ટ કમાન્ડ્સ")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🕒 સમય અને તારીખ"):
            now = datetime.now().strftime("%d-%m-%Y | %I:%M:%S %p")
            st.success(f"અત્યારનો સમય: {now}")
    with c2:
        if st.button("📢 શોપ ઓફર બનાવો"):
            offers = [
                "🔥 MEGA SALE: આજે દરેક ઓર્ડર પર મેળવો Flat 20% OFF!",
                "🎁 SPECIAL COMBO: 2 પ્રોડક્ટ ખરીદો અને 1 સરપ્રાઇઝ ગિફ્ટ ફ્રી મેળવો!",
                "⚡ FLASH DEAL: માત્ર આજના દિવસ માટે ફ્રી હોમ ડિલિવરી!"
            ]
            st.info(random.choice(offers))

    cmd = st.text_input("💬 તમારો કમાન્ડ લખો (દા.ત. 'note: દૂધ લાવવું', '250 * 12'):")
    if st.button("▶️ કમાન્ડ ચલાવો (Execute)"):
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
            st.info(f"કમાન્ડ પ્રોસેસ થયો: {cmd}")

    if st.session_state.notes:
        st.markdown("### 📝 તમારી સ્માર્ટ નોટ્સ")
        for idx, n in enumerate(st.session_state.notes, 1):
            st.write(f"{idx}. {n}")
