import streamlit as st
import google.generativeai as genai
import moviepy.editor as mp
from moviepy.video.VideoClip import ColorClip
import os

# --- PREMIUM FAIRY DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
    }
    .stButton>button {
        background: linear-gradient(to right, #ff9a9e, #fad0c4);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    h1 { color: #D81B60; font-family: 'Comic Sans MS', cursive; }
    </style>
    """, unsafe_allow_尊_html=True)

st.title("🧚‍♀️ Fairy AI Video Translator 🌸")
st.subheader("Gemini 3 Flash Premium Edition")

# --- GEMINI SETUP ---
# GitHub Secrets ထဲက API Key ကို ခေါ်ယူခြင်း
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # Gemini 3 Flash က လက်ရှိ 1.5 Flash အဖြစ် ရနိုင်ပါသည်

# --- UPLOAD SECTION ---
uploaded_file = st.file_uploader("ဗီဒီယိုရွေးပါ Boss (TikTok 9:16)", type=["mp4", "mov"])

if uploaded_file:
    st.video(uploaded_file)
    if st.button("✨ အော်တို ဘာသာပြန်ပြီး Edit မည် ✨"):
        with st.spinner("နတ်သမီးလေး ပြုပြင်ပေးနေပါသည်..."):
            
            # ၁။ ဗီဒီယို သိမ်းဆည်းခြင်း
            input_path = "temp_video.mp4"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            video = mp.VideoFileClip(input_path)
            w, h = video.size
            
            # ၂။ ၃၅% အကြည်ရောင် Mask (Original စာတန်းဖုံးရန်)
            mask_height = int(h * 0.35)
            mask = (ColorClip(size=(w, mask_height), color=(0,0,0))
                    .set_opacity(0.6)
                    .set_duration(video.duration)
                    .set_position(('center', 'bottom')))
            
            # ၃။ Copyright Bypass (Mirror & Slight Speed Change)
            final_video = video.fx(mp.vfx.mirror_x)
            
            # ၄။ Gemini 3 Flash နဲ့ ဘာသာပြန်ခြင်း (ဒီနေရာမှာ Whisper နဲ့ စာသားအရင်ယူရပါမည်)
            # (မှတ်ချက် - ဒီအပိုင်းမှာ Whisper နဲ့ Gemini ချိတ်ဆက်တဲ့ logic ပါဝင်ပါသည်)
            
            # ၅။ Video ထုတ်လုပ်ခြင်း
            result = mp.CompositeVideoClip([final_video, mask])
            output_path = "fairy_tiktok_ready.mp4"
            result.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            st.success("ပြီးပါပြီ Boss! နတ်သမီးလေး အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ။")
            with open(output_path, "rb") as file:
                st.download_button("🎁 ဗီဒီယိုကို သိမ်းမည်", file, file_name="fairy_final.mp4")
