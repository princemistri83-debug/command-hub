import streamlit as st
import datetime
import time
import urllib.parse

# પેજ સેટઅપ અને સ્માર્ટ ડાર્ક UI
st.set_page_config(page_title="AI Smart Command Hub", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .command-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #38bdf8;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        margin-bottom: 20px;
    }
    .status-badge {
        background-color: #0284c7;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# હેડર
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🤖 J.A.R.V.I.S. Command Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>તમારો સ્માર્ટ AI આસિસ્ટન્ટ — કમાન્ડ આપો અને સ્ક્રીન પર ઓટો-એક્શન જુઓ</p>", unsafe_allow_html=True)

# સેસન સ્ટેટ (નોટ્સ અને હિસ્ટ્રી સેવ રાખવા માટે)
if "notes" not in st.session_state:
    st.session_state.notes = []
if "logs" not in st.session_state:
    st.session_state.logs = []

# ક્વિક કમાન્ડ બટન્સ (એક ટચમાં સ્માર્ટ એક્શન)
st.markdown("### ⚡ ક્વિક સ્માર્ટ કમાન્ડ્સ")
col1, col2, col3 = st.columns(3)
quick_cmd = ""
with col1:
    if st.button("🕒 સમય અને તારીખ"):
        quick_cmd = "time"
with col2:
    if st.button("📢 શોપ ઓફર બનાવો"):
        quick_cmd = "shop_offer"
with col3:
    if st.button("🚀 ઓટો વર્કફ્લો ચલાવો"):
        quick_cmd = "workflow"

# કમાન્ડ ઇનપુટ બોક્સ
user_cmd = st.text_input("💬 તમારો કમાન્ડ અહીં લખો (દા.ત. 'youtube kholo', 'note: દૂધ લાવવું', '250 * 12', 'search: surat weather'):", value=quick_cmd)

if st.button("▶️ કમાન્ડ ચલાવો (Execute)", type="primary", use_container_width=True) or quick_cmd:
    cmd = user_cmd.strip().lower()
    
    if cmd:
        with st.spinner("AI કમાન્ડ પ્રોસેસ કરી રહ્યું છે..."):
            time.sleep(0.6)
        
        st.markdown("<div class='command-box'>", unsafe_allow_html=True)
        st.markdown("<span class='status-badge'>ACTION EXECUTED</span>", unsafe_allow_html=True)
        
        # 1. સમય અને તારીખ
        if "time" in cmd or "સમય" in cmd:
            now = datetime.datetime.now().strftime("%d-%m-%Y | %I:%M:%S %p")
            st.success(f"🕒 હાલનો સમય અને તારીખ: **{now}**")
            st.session_state.logs.append(f"સમય ચેક કર્યો: {now}")

        # 2. શોપ માટે સ્માર્ટ ઑફર જનરેટર
        elif "shop_offer" in cmd or "ઓફર" in cmd or "offer" in cmd:
            offer_text = "🎉 **મેગા ધમાકા ઑફર!** 🎉\nઆજે જ અમારી શોપની મુલાકાત લો અને દરેક ખરીદી પર મેળવો **ખાસ 20% થી 50% સુધીનું ડિસ્કાઉન્ટ!**\n📍 સ્થળ: સુરત | ⏰ મર્યાદિત સમય માટે!"
            st.info(offer_text)
            st.code(offer_text.replace("**", ""), language="text")
            st.session_state.logs.append("શોપ પ્રોમો ઑફર જનરેટ કરી")

        # 3. સ્ટેપ-બાય-સ્ટેપ ઓટો વર્કફ્લો (RPA ડેમો)
        elif "workflow" in cmd or "સ્ટેપ" in cmd:
            st.write("🔄 **ઓટોમેટિક વર્કફ્લો શરૂ થઈ રહ્યો છે...**")
            progress = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "Step 1: સિસ્ટમ અને સિક્યોરિટી ચેક થઈ રહી છે...",
                "Step 2: ડેટાબેઝ કનેક્ટ થઈ રહ્યો છે...",
                "Step 3: સ્માર્ટ ડેશબોર્ડ તૈયાર થઈ રહ્યું છે...",
                "✅ બધા સ્ટેપ્સ સફળતાપૂર્વક પૂર્ણ થયા!"
            ]
            for i, step in enumerate(steps):
                status_text.markdown(f"**{step}**")
                progress.progress((i + 1) * 25)
                time.sleep(0.8)
            st.balloons()
            st.session_state.logs.append("ઓટો વર્કફ્લો રન કર્યો")

        # 4. સ્માર્ટ નોટ સેવ કરવી (ઉદાહરણ: note: સાંજે 5 વાગ્યે મીટિંગ)
        elif cmd.startswith("note:") or cmd.startswith("નોટ:"):
            note_content = user_cmd.split(":", 1)[1].strip()
            st.session_state.notes.append(note_content)
            st.success(f"📝 નવી નોટ સેવ થઈ ગઈ: **{note_content}**")
            st.session_state.logs.append(f"નોટ ઉમેરી: {note_content}")

        # 5. Google / YouTube સર્ચ લિંક ખોલવી
        elif "youtube" in cmd:
            st.markdown("🎬 **YouTube ખોલવા માટે નીચે ક્લિક કરો:**")
            st.link_button("▶️ Open YouTube", "https://www.youtube.com")
            st.session_state.logs.append("YouTube લિંક ઓપન કરી")
            
        elif cmd.startswith("search:") or "શોધો" in cmd:
            query = user_cmd.split(":", 1)[1].strip() if ":" in user_cmd else user_cmd
            encoded_q = urllib.parse.quote(query)
            st.markdown(f"🔍 **'{query}' માટે Google સર્ચ તૈયાર છે:**")
            st.link_button("🌐 Google પર જુઓ", f"https://www.google.com/search?q={encoded_q}")
            st.session_state.logs.append(f"Google સર્ચ: {query}")

        # 6. સ્માર્ટ કેલ્ક્યુલેટર (જો ગણિતનો દાખલો લખ્યો હોય તો)
        elif any(op in cmd for op in ["+", "-", "*", "/"]):
            try:
                # સુરક્ષિત ગણતરી
                allowed_chars = "0123456789+-*/.() "
                if all(c in allowed_chars for c in cmd):
                    ans = eval(cmd)
                    st.success(f"🧮 જવાબ: **{cmd} = {ans}**")
                    st.session_state.logs.append(f"ગણતરી: {cmd} = {ans}")
                else:
                    st.warning("કૃપા કરીને સાચા આંકડા લખો.")
            except:
                st.error("ગણતરી કરવામાં ભૂલ આવી.")

        else:
            st.warning(f"🤖 કમાન્ડ મળ્યો: **'{user_cmd}'** — આ કમાન્ડ માટે તમે કસ્ટમ એક્શન સેટ કરી શકો છો!")
            st.session_state.logs.append(f"કસ્ટમ કમાન્ડ: {user_cmd}")
            
        st.markdown("</div>", unsafe_allow_html=True)

# નીચે સેવ થયેલી નોટ્સ અને કમાન્ડ હિસ્ટ્રી બતાવવી
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 📝 તમારી સ્માર્ટ નોટ્સ")
    if st.session_state.notes:
        for idx, n in enumerate(st.session_state.notes, 1):
            st.write(f"{idx}. {n}")
    else:
        st.caption("હજુ કોઈ નોટ નથી. 'note: તમારો મેસેજ' લખીને ઉમેરો.")

with col_b:
    st.markdown("### 📜 એક્શન હિસ્ટ્રી")
    if st.session_state.logs:
        for log in reversed(st.session_state.logs[-5:]):
            st.caption(f"⚡ {log}")
    else:
        st.caption("હજુ કોઈ કમાન્ડ ચલાવ્યો નથી.")
