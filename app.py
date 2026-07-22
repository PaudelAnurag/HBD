import streamlit as st
import streamlit.components.v1 as components
import base64, mimetypes, os

def file_to_data_uri(path):
    """Turn local file into data URI so browser iframe can play it (no server path works otherwise)."""
    if not path or path.startswith(("http://","https://","data:")):
        return path
    if not os.path.exists(path):
        return ""  # file missing — leave empty, won't crash
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

FINAL_VIDEO_SRC = file_to_data_uri("assets/video/pranz.mp4")

PHOTOS = [
    {"src": "assets/img/pic1.jpeg", "caption": "Kata hereko ho kunni"},
    {"src": "assets/img/pic2.jpeg", "caption": "Nasalu Ankha"},
    {"src": "assets/img/pic3.jpeg", "caption": "Beauty with cloudy "},
    {"src": "assets/img/pic4.jpeg", "caption": "Women In Black"},
    {"src": "assets/img/pic5.jpeg", "caption": "Chasma Chai Ho K"},
    {"src": "assets/img/pic6.jpeg", "caption": "Yo xai mero fav"},
    {"src": "assets/img/pic7.jpeg", "caption": "Mirror Selfie eklai??"},
]
for p in PHOTOS:
    p["src"] = file_to_data_uri(p["src"])

import json
PHOTOS_JSON = json.dumps(PHOTOS, ensure_ascii=False)

st.set_page_config(page_title="For You, Idiot", layout="centered")

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; }
.stApp { background: #2a1020 !important; }
</style>
""", unsafe_allow_html=True)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap');
  *{margin:0;padding:0;box-sizing:border-box;}
  *::-webkit-scrollbar{display:none;}
  *{-ms-overflow-style:none;scrollbar-width:none;}
  body{min-height:100vh;background:radial-gradient(ellipse at top,#4a1a35 0%,#3a1228 50%,#220d1c 100%);font-family:'Lato',sans-serif;overflow:hidden;}
  #flowerCanvas{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;}
  #burstCanvas{position:fixed;inset:0;pointer-events:none;z-index:95;display:none;}
  @keyframes fadeUp{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
  @keyframes flFloat{0%,100%{transform:translateY(0) rotate(0deg);}50%{transform:translateY(-10px) rotate(6deg);}}
  @keyframes dotBlink{0%,80%,100%{opacity:0.2;}40%{opacity:1;}}

  /* SPLASH */
  #splashScreen{position:fixed;inset:0;z-index:50;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity 1s ease,visibility 1s ease;}
  #splashScreen.hide{opacity:0;visibility:hidden;}
  .flower-logo{position:relative;width:90px;height:90px;margin-bottom:32px;}
  .petal{position:absolute;width:28px;height:40px;background:linear-gradient(180deg,#e8729a 0%,#c94f7a 100%);border-radius:50% 50% 50% 50%/60% 60% 40% 40%;top:50%;left:50%;transform-origin:bottom center;opacity:0;animation:petalBloom 2s ease forwards;}
  .petal:nth-child(1){--r:0deg;animation-delay:.00s}.petal:nth-child(2){--r:60deg;animation-delay:.15s}.petal:nth-child(3){--r:120deg;animation-delay:.30s}.petal:nth-child(4){--r:180deg;animation-delay:.45s}.petal:nth-child(5){--r:240deg;animation-delay:.60s}.petal:nth-child(6){--r:300deg;animation-delay:.75s}
  @keyframes petalBloom{0%{opacity:0;transform:translate(-50%,-100%) rotate(var(--r,0deg)) scale(0.2);}60%{opacity:1;transform:translate(-50%,-100%) rotate(var(--r,0deg)) scale(1.1);}100%{opacity:1;transform:translate(-50%,-100%) rotate(var(--r,0deg)) scale(1);}}
  .flower-center{position:absolute;width:18px;height:18px;background:radial-gradient(circle,#fff9f9 0%,#f0c4d4 100%);border-radius:50%;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2;box-shadow:0 0 10px rgba(255,200,220,0.8);opacity:0;animation:centerPop 0.4s ease 0.9s forwards;}
  @keyframes centerPop{from{opacity:0;transform:translate(-50%,-50%) scale(0);}to{opacity:1;transform:translate(-50%,-50%) scale(1);}}
  .flower-glow{position:absolute;width:100px;height:100px;border-radius:50%;background:radial-gradient(circle,rgba(220,80,130,0.25) 0%,transparent 70%);top:50%;left:50%;transform:translate(-50%,-50%);animation:glowPulse 2.5s ease-in-out infinite;}
  @keyframes glowPulse{0%,100%{transform:translate(-50%,-50%) scale(1);opacity:0.6;}50%{transform:translate(-50%,-50%) scale(1.3);opacity:1;}}
  .preparing-text{font-size:14px;color:rgba(255,255,255,0.55);letter-spacing:1.5px;font-weight:300;opacity:0;animation:fadeUp 1s ease 1.2s forwards;}
  .dots span{display:inline-block;animation:dotBlink 1.4s infinite;color:rgba(255,255,255,0.55);}
  .dots span:nth-child(2){animation-delay:0.2s}.dots span:nth-child(3){animation-delay:0.4s}
  .progress-bar-wrap{position:fixed;bottom:0;left:0;width:100%;height:3px;background:rgba(255,255,255,0.08);z-index:60;}
  .progress-bar{height:100%;width:0%;background:linear-gradient(90deg,#c94f7a,#ff9aba);animation:fillBar 5s linear forwards;box-shadow:0 0 8px rgba(255,107,157,0.7);}
  @keyframes fillBar{from{width:0%}to{width:100%}}

  /* PIN */
  #pinScreen{position:fixed;inset:0;z-index:40;display:flex;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity 1s ease,visibility 1s ease;}
  #pinScreen.show{opacity:1;visibility:visible;}
  .card{background:rgba(255,255,255,0.07);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,0.13);border-radius:28px;padding:32px 28px 26px;width:320px;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,0.45);}
  .top-flower-icon{font-size:40px;display:block;margin-bottom:10px;animation:floatFlower 3s ease-in-out infinite;filter:drop-shadow(0 0 12px rgba(255,150,180,0.7));}
  @keyframes floatFlower{0%,100%{transform:translateY(0) rotate(-5deg);}50%{transform:translateY(-9px) rotate(5deg);}}
  .card-title{font-family:'Playfair Display',serif;font-size:26px;color:#fff;margin-bottom:5px;}
  .card-sub{font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:22px;letter-spacing:0.5px;}
  .pin-dots{display:flex;justify-content:center;gap:12px;margin-bottom:26px;}
  .pin-dot{width:13px;height:13px;border-radius:50%;border:2px solid rgba(255,255,255,0.3);background:transparent;transition:all 0.25s ease;}
  .pin-dot.filled{background:#ff6b9d;border-color:#ff6b9d;box-shadow:0 0 10px rgba(255,107,157,0.7);}
  .numpad{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-bottom:16px;}
  .num-btn{width:72px;height:72px;border-radius:50%;border:1.5px solid rgba(255,255,255,0.18);background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.88);font-size:21px;cursor:pointer;margin:0 auto;display:flex;align-items:center;justify-content:center;transition:all 0.15s ease;user-select:none;}
  .num-btn:hover{background:rgba(255,107,157,0.28);border-color:rgba(255,107,157,0.55);transform:scale(1.07);}
  .num-btn:active{transform:scale(0.93);}
  .enter-btn{background:rgba(255,107,157,0.25)!important;border-color:rgba(255,107,157,0.5)!important;}
  .hint{font-size:12px;color:rgba(255,255,255,0.3);}
  @keyframes shake{0%,100%{transform:translateX(0);}20%{transform:translateX(-8px);}40%{transform:translateX(8px);}60%{transform:translateX(-5px);}80%{transform:translateX(5px);}}
  .shake{animation:shake 0.4s ease;}

  /* GIFT */
  #giftScreen{position:fixed;inset:0;z-index:70;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity 0.9s ease,visibility 0.9s ease;background:radial-gradient(ellipse at center,#5a1f40 0%,#3a1228 55%,#220d1c 100%);}
  #giftScreen.show{opacity:1;visibility:visible;}
  .tap-hint{font-size:14px;color:rgba(255,255,255,0.6);letter-spacing:0.5px;margin-bottom:44px;font-weight:300;opacity:0;}
  .tap-hint.vis{animation:fadeUp 0.8s ease 0.3s forwards;}
  .gift-wrap{position:relative;cursor:pointer;animation:giftFloat 3s ease-in-out infinite;filter:drop-shadow(0 18px 40px rgba(0,0,0,0.5));}
  @keyframes giftFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-12px);}}
  .sparkle{position:absolute;border-radius:50%;background:rgba(255,220,240,0.75);animation:sparklePop 2.5s ease-in-out infinite;}
  .sparkle:nth-child(1){width:5px;height:5px;top:-10px;left:30px;animation-delay:0s}
  .sparkle:nth-child(2){width:4px;height:4px;top:20px;left:-18px;animation-delay:0.6s}
  .sparkle:nth-child(3){width:4px;height:4px;top:60px;left:-22px;animation-delay:1.1s}
  .sparkle:nth-child(4){width:5px;height:5px;top:30px;right:-20px;animation-delay:0.3s}
  .sparkle:nth-child(5){width:3px;height:3px;bottom:10px;right:-14px;animation-delay:0.9s}
  .sparkle:nth-child(6){width:4px;height:4px;bottom:-5px;left:50px;animation-delay:1.5s}
  @keyframes sparklePop{0%,100%{opacity:0.2;transform:scale(0.8);}50%{opacity:1;transform:scale(1.4);}}
  @keyframes giftShakeAnim{0%,100%{transform:translateY(0) rotate(0deg);}15%{transform:translateY(-4px) rotate(-6deg);}30%{transform:translateY(-8px) rotate(6deg);}45%{transform:translateY(-4px) rotate(-4deg);}60%{transform:translateY(-10px) rotate(3deg);}75%{transform:translateY(-5px) rotate(-2deg);}90%{transform:translateY(-2px) rotate(1deg);}}
  .gift-shake-anim{animation:giftShakeAnim 0.6s ease forwards!important;}
  @keyframes giftExplodeAnim{0%{transform:scale(1) rotate(0deg);opacity:1;}40%{transform:scale(1.25) rotate(-8deg);opacity:1;}100%{transform:scale(0) rotate(20deg);opacity:0;}}
  .gift-explode-anim{animation:giftExplodeAnim 0.6s ease forwards!important;}

  /* MAIN SCROLL */
  #mainScroll{position:fixed;inset:0;z-index:75;overflow-y:scroll;overflow-x:hidden;opacity:0;visibility:hidden;transition:opacity 0.9s ease,visibility 0.9s ease;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;}
  #mainScroll.show{opacity:1;visibility:visible;}

  /* SEC 1 BIRTHDAY */
  #sec-birthday{min-height:100vh;width:100%;background:radial-gradient(ellipse at center,#5a1535 0%,#3d1228 55%,#2a0e20 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 28px;position:relative;overflow:hidden;}
  .bd-fl{position:absolute;font-size:20px;animation:flFloat 4s ease-in-out infinite;pointer-events:none;}
  .bd-tag{font-size:11px;letter-spacing:3px;color:rgba(255,200,200,0.6);margin-bottom:28px;display:flex;align-items:center;gap:10px;}
  .bd-tag::before,.bd-tag::after{content:'';display:block;width:30px;height:1px;background:rgba(255,200,200,0.3);}
  .bd-happy{font-family:'Playfair Display',serif;font-size:56px;color:#fff;line-height:1.1;text-shadow:0 2px 20px rgba(255,100,150,0.3);}
  .bd-birthday{font-family:'Playfair Display',serif;font-size:56px;font-style:italic;color:#ff9aba;line-height:1.1;}
  .bd-name{font-family:'Playfair Display',serif;font-size:62px;color:#fff;margin-top:8px;text-shadow:0 0 30px rgba(255,150,180,0.5);}
  .bd-divider{width:40px;height:1px;background:rgba(255,255,255,0.3);margin:24px auto;}
  .bd-date{font-size:11px;letter-spacing:4px;color:rgba(255,255,255,0.4);font-weight:300;}
  .scroll-down-hint{margin-top:48px;display:flex;flex-direction:column;align-items:center;gap:6px;animation:fadeUp 1s ease 2s forwards;opacity:0;}
  .scroll-down-hint span{font-size:11px;letter-spacing:2px;color:rgba(255,255,255,0.35);}
  .arrow-d{width:18px;height:18px;border-right:2px solid rgba(255,255,255,0.35);border-bottom:2px solid rgba(255,255,255,0.35);transform:rotate(45deg);animation:arrowB 1.4s ease-in-out infinite;}
  @keyframes arrowB{0%,100%{transform:rotate(45deg) translateY(0);}50%{transform:rotate(45deg) translateY(5px);}}

  /* SEC 2 BOUQUET */
  #sec-bouquet{min-height:100vh;width:100%;background:radial-gradient(ellipse at center,#4a1030 0%,#3a1228 55%,#220d1c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden;padding:20px 0 30px;gap:16px;}
  .bq-heading-wrap{text-align:center;z-index:2;flex-shrink:0;}
  .bq-tag{font-size:10px;letter-spacing:3px;color:rgba(255,200,220,0.55);margin-bottom:6px;display:flex;align-items:center;justify-content:center;gap:8px;}
  .bq-tag::before,.bq-tag::after{content:'';display:block;width:20px;height:1px;background:rgba(255,200,220,0.3);}
  .bq-title{font-family:'Playfair Display',serif;font-size:26px;color:#fff;text-shadow:0 2px 16px rgba(255,100,150,0.4);margin-bottom:4px;}
  .bq-subtitle{font-size:12px;color:rgba(255,255,255,0.4);font-style:italic;}
  #vaseArea{position:relative;width:100%;display:flex;align-items:center;justify-content:center;flex:1;min-height:280px;}
  .sc-outer{position:absolute;font-size:26px;cursor:pointer;animation:flFloat 4s ease-in-out infinite;filter:drop-shadow(0 3px 8px rgba(0,0,0,0.35));user-select:none;transition:transform 0.2s ease;}
  .sc-outer:hover{transform:scale(1.4)!important;}
  @keyframes bloomPop{0%{transform:scale(1);}35%{transform:scale(1.8) rotate(15deg);}65%{transform:scale(1.3) rotate(-8deg);}100%{transform:scale(1) rotate(0deg);}}
  .bloom-once{animation:bloomPop 0.5s ease forwards!important;}
  #msgBar{width:calc(100% - 32px);margin:0 16px;background:rgba(255,255,255,0.1);backdrop-filter:blur(12px);border-radius:18px;padding:18px 22px;text-align:center;border:1px solid rgba(255,255,255,0.15);min-height:76px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
  #msgText{font-family:'Playfair Display',serif;font-style:italic;font-size:15px;color:rgba(255,255,255,0.85);line-height:1.7;transition:opacity 0.4s ease;}
  #msgText.fade{opacity:0;}

  /* SEC 3 LETTER */
  #sec-letter{min-height:100vh;width:100%;background:radial-gradient(ellipse at top,#4a1a35 0%,#3a1228 50%,#220d1c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:50px 24px 60px;position:relative;overflow:hidden;}
  .le-fl{position:absolute;font-size:18px;pointer-events:none;animation:flFloat 5s ease-in-out infinite;opacity:0.55;}
  .ltr-quote{background:rgba(255,255,255,0.09);border-radius:18px;padding:22px 24px;font-size:15px;color:rgba(255,255,255,0.8);line-height:1.75;text-align:center;margin-bottom:32px;border:1px solid rgba(255,255,255,0.1);width:100%;max-width:340px;}
  .ltr-section-tag{text-align:center;font-size:11px;letter-spacing:3px;color:rgba(255,200,220,0.5);margin-bottom:10px;display:flex;align-items:center;justify-content:center;gap:8px;}
  .ltr-title{font-family:'Playfair Display',serif;font-size:28px;color:#fff;text-align:center;margin-bottom:24px;}
  .letter-card{background:linear-gradient(160deg,#f9eef4 0%,#fce8f0 100%);border-radius:18px;padding:30px 26px;color:#5a2a3a;width:100%;max-width:340px;}
  .letter-date{font-size:11px;letter-spacing:2px;text-align:center;color:rgba(90,42,58,0.5);margin-bottom:18px;}
  .letter-dear{font-family:'Playfair Display',serif;font-size:20px;color:#7a2a45;margin-bottom:14px;}
  .letter-body{font-size:13px;line-height:1.9;color:rgba(90,42,58,0.85);font-weight:300;}
  .letter-body p{margin-bottom:14px;}
  .letter-sig{font-family:'Playfair Display',serif;font-style:italic;font-size:16px;color:#7a2a45;margin-top:20px;text-align:right;}

  /* SEC 4 PHOTOS */
  #sec-photos{min-height:100vh;width:100%;background:radial-gradient(ellipse at top,#3d1228 0%,#2a0e20 60%,#1e0918 100%);display:flex;flex-direction:column;align-items:center;padding:60px 20px 60px;position:relative;overflow:hidden;}
  .photos-tag{font-size:11px;letter-spacing:3px;color:rgba(255,200,220,0.5);margin-bottom:10px;display:flex;align-items:center;gap:8px;}
  .photos-title{font-family:'Playfair Display',serif;font-size:34px;color:#fff;text-align:center;margin-bottom:8px;}
  .photos-sub{font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:44px;font-style:italic;}
  .polaroid-wrap{position:relative;width:150px;margin:0 10px 30px;cursor:pointer;}
  .polaroid{background:#fff;padding:8px 8px 34px;border-radius:4px;box-shadow:0 12px 40px rgba(0,0,0,0.45);position:relative;}
  .polaroid-wrap:nth-child(odd) .polaroid{transform:rotate(-2.5deg);}
  .polaroid-wrap:nth-child(even) .polaroid{transform:rotate(2.5deg);}
  .polaroid-img{width:100%;height:130px;border-radius:2px;background:#e8d5e0;display:flex;align-items:center;justify-content:center;font-size:38px;overflow:hidden;}
  .polaroid-caption{font-family:'Playfair Display',serif;font-style:italic;font-size:11px;color:#5a2a3a;text-align:center;position:absolute;bottom:6px;left:0;right:0;padding:0 4px;}
  .tape{position:absolute;top:-10px;left:50%;transform:translateX(-50%);width:50px;height:20px;background:rgba(255,240,200,0.6);border-radius:2px;z-index:2;}
  .photo-deco{position:absolute;font-size:16px;pointer-events:none;animation:flFloat 4s ease-in-out infinite;}
  #lightbox{position:fixed;inset:0;z-index:200;background:rgba(0,0,0,0.88);display:none;align-items:center;justify-content:center;flex-direction:column;backdrop-filter:blur(8px);padding:20px;}
  #lightbox.open{display:flex;}
  #lbImg{width:100%;max-width:340px;background:#fff;padding:14px 14px 50px;border-radius:4px;box-shadow:0 20px 60px rgba(0,0,0,0.6);position:relative;animation:popIn 0.35s cubic-bezier(0.175,0.885,0.32,1.275);}
  @keyframes popIn{from{transform:scale(0.6);opacity:0;}to{transform:scale(1);opacity:1;}}
  #lbImg .polaroid-img{height:240px;font-size:80px;}
  #lbCaption{font-family:'Playfair Display',serif;font-style:italic;font-size:15px;color:#5a2a3a;text-align:center;position:absolute;bottom:10px;left:0;right:0;padding:0 12px;}
  #lbClose{margin-top:20px;font-size:13px;color:rgba(255,255,255,0.6);cursor:pointer;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);padding:8px 24px;border-radius:50px;}

  /* SEC 5 JOURNEY */
  #sec-journey{min-height:100vh;width:100%;background:radial-gradient(ellipse at top,#3a1228 0%,#2a0e20 60%,#1e0918 100%);display:flex;flex-direction:column;align-items:center;padding:60px 20px 80px;position:relative;overflow:hidden;}
  .jrn-tag{font-size:11px;letter-spacing:3px;color:rgba(255,200,220,0.5);margin-bottom:10px;}
  .jrn-title{font-family:'Playfair Display',serif;font-size:30px;color:#fff;text-align:center;margin-bottom:6px;}
  .jrn-star{font-size:16px;color:rgba(255,255,255,0.4);margin-bottom:40px;}
  .timeline{position:relative;width:100%;max-width:340px;}
  .timeline::before{content:'';position:absolute;left:14px;top:0;bottom:0;width:1px;background:linear-gradient(to bottom,rgba(255,107,157,0.6),rgba(255,107,157,0.1));}
  .tl-item{position:relative;padding:0 0 32px 48px;}
  .tl-dot{position:absolute;left:8px;top:18px;width:14px;height:14px;border-radius:50%;background:rgba(255,107,157,0.8);box-shadow:0 0 10px rgba(255,107,157,0.5);border:2px solid rgba(255,150,180,0.6);}
  .tl-card{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px 18px;}
  .tl-icon{font-size:20px;margin-bottom:8px;}
  .tl-label{font-size:10px;letter-spacing:2px;color:rgba(255,200,220,0.6);margin-bottom:6px;text-transform:uppercase;}
  .tl-heading{font-family:'Playfair Display',serif;font-size:18px;color:#fff;margin-bottom:8px;}
  .tl-body{font-size:13px;color:rgba(255,255,255,0.55);line-height:1.75;font-weight:300;}
  .end-row{text-align:center;margin-top:30px;font-size:26px;letter-spacing:10px;animation:flFloat 3s ease-in-out infinite;}

  /* SEC 6 MUSIC (YouTube player) */
  #sec-music{min-height:100vh;width:100%;background:radial-gradient(ellipse at top,#3a1228 0%,#2a0e20 60%,#1a0815 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 24px 60px;position:relative;overflow:hidden;}
  .mus-fl{position:absolute;font-size:14px;color:rgba(255,255,255,0.12);animation:flFloat 5s ease-in-out infinite;pointer-events:none;}
  .mus-sunflower{font-size:32px;margin-bottom:12px;animation:flFloat 3s ease-in-out infinite;}
  .mus-tag{font-size:11px;letter-spacing:3px;color:rgba(255,200,220,0.55);margin-bottom:8px;display:flex;align-items:center;gap:8px;}
  .mus-tag::before,.mus-tag::after{content:'';display:block;width:20px;height:1px;background:rgba(255,200,220,0.3);}
  .mus-title{font-family:'Playfair Display',serif;font-size:32px;color:#fff;margin-bottom:6px;}
  .mus-sub{font-size:13px;color:rgba(255,255,255,0.38);font-style:italic;margin-bottom:28px;}
  .player-card{width:100%;max-width:340px;background:rgba(255,255,255,0.06);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,0.1);border-radius:28px;padding:22px 18px;box-shadow:0 20px 60px rgba(0,0,0,0.5);margin-bottom:20px;}
  .video-wrap{position:relative;width:100%;border-radius:18px;overflow:hidden;margin-bottom:16px;box-shadow:0 10px 30px rgba(0,0,0,0.4);aspect-ratio:16/9;cursor:pointer;}
  .video-wrap img{width:100%;height:100%;object-fit:cover;display:block;}
  .video-wrap iframe{width:100%;height:100%;display:block;border:0;}
  .video-play-overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.25);transition:background 0.2s ease;}
  .video-wrap:hover .video-play-overlay{background:rgba(0,0,0,0.4);}
  .video-play-btn{width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,0.92);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,0.4);}
  .video-play-btn::after{content:'';border-style:solid;border-width:12px 0 12px 20px;border-color:transparent transparent transparent #e0508a;margin-left:5px;}
  .video-tap-hint{position:absolute;bottom:10px;right:12px;font-size:10px;color:rgba(255,255,255,0.85);background:rgba(0,0,0,0.4);padding:4px 10px;border-radius:20px;letter-spacing:0.5px;}
  .song-title{font-family:'Playfair Display',serif;font-size:19px;color:#fff;text-align:center;margin-bottom:4px;}
  .song-artist{font-size:12px;color:rgba(255,255,255,0.45);text-align:center;margin-bottom:6px;}
  .playlist{width:100%;max-width:340px;}
  .pl-label{font-size:11px;letter-spacing:2px;color:rgba(255,255,255,0.3);text-align:center;margin-bottom:14px;}
  .pl-item{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:14px;cursor:pointer;transition:background 0.2s;border:1px solid transparent;margin-bottom:6px;}
  .pl-item:hover{background:rgba(255,255,255,0.07);}
  .pl-item.active{background:rgba(255,107,157,0.15);border-color:rgba(255,107,157,0.25);}
  .pl-num{font-size:12px;color:rgba(255,255,255,0.3);width:18px;text-align:center;flex-shrink:0;}
  .pl-item.active .pl-num{color:#ff6b9d;}
  .pl-info{flex:1;min-width:0;}
  .pl-name{font-size:14px;color:rgba(255,255,255,0.8);}
  .pl-item.active .pl-name{color:#fff;font-family:'Playfair Display',serif;}
  .pl-artist{font-size:11px;color:rgba(255,255,255,0.35);margin-top:2px;}

  /* SEC 7 GRATITUDE JAR */
  #sec-jar{min-height:100vh;width:100%;background:radial-gradient(ellipse at top,#3a1228 0%,#2a0e20 55%,#1a0815 100%);display:flex;flex-direction:column;align-items:center;padding:60px 24px 70px;position:relative;overflow:hidden;text-align:center;}
  .jar-fl{position:absolute;font-size:18px;pointer-events:none;animation:flFloat 4s ease-in-out infinite;opacity:0.7;}
  .jar-tag{font-size:11px;letter-spacing:3px;color:rgba(255,200,220,0.55);margin-bottom:18px;}
  .jar-title{font-family:'Playfair Display',serif;font-size:30px;color:#fff;margin-bottom:10px;}
  .jar-sub{font-size:13px;color:rgba(255,255,255,0.45);font-style:italic;margin-bottom:36px;}
  .jar-svg-wrap{cursor:pointer;user-select:none;transition:transform 0.08s ease;margin-bottom:34px;}
  .jar-svg-wrap.shaking{animation:jarShake 0.5s ease;}
  @keyframes jarShake{
    0%,100%{transform:rotate(0deg) translateX(0);}
    10%{transform:rotate(-8deg) translateX(-6px);}
    20%{transform:rotate(7deg) translateX(6px);}
    30%{transform:rotate(-9deg) translateX(-7px);}
    40%{transform:rotate(8deg) translateX(7px);}
    50%{transform:rotate(-6deg) translateX(-5px);}
    60%{transform:rotate(6deg) translateX(5px);}
    70%{transform:rotate(-4deg) translateX(-3px);}
    80%{transform:rotate(4deg) translateX(3px);}
    90%{transform:rotate(-2deg) translateX(-2px);}
  }
  .jar-btn{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.85);font-size:14px;padding:14px 30px;border-radius:50px;cursor:pointer;margin-bottom:30px;display:flex;align-items:center;gap:8px;}
  .jar-btn:hover{background:rgba(255,107,157,0.18);border-color:rgba(255,107,157,0.35);}
  .jar-note{width:100%;max-width:340px;background:linear-gradient(160deg,#f9eef4 0%,#fce8f0 100%);border-radius:18px;padding:34px 28px;color:#5a2a3a;box-shadow:0 20px 50px rgba(0,0,0,0.4);position:relative;opacity:0;transform:translateY(14px);transition:opacity 0.5s ease,transform 0.5s ease;}
  .jar-note.show{opacity:1;transform:translateY(0);}
  .jar-note-text{font-family:'Playfair Display',serif;font-style:italic;font-size:18px;line-height:1.6;color:#7a2a45;}
  .jar-note-mark{position:absolute;top:14px;right:18px;font-size:13px;color:rgba(90,42,58,0.3);}

  /* SEC 8 FINAL BIRTHDAY CARD */
  #sec-final{min-height:100vh;width:100%;background:radial-gradient(ellipse at top,#3d1228 0%,#2a0e20 55%,#1a0815 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:50px 24px 60px;position:relative;overflow:hidden;text-align:center;}
  #finalFlowerCanvas{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;}
  .final-card{width:100%;max-width:340px;background:linear-gradient(160deg,rgba(255,255,255,0.1) 0%,rgba(255,180,210,0.06) 100%);backdrop-filter:blur(20px);border:1px solid rgba(255,180,210,0.3);border-radius:28px;padding:46px 30px 38px;box-shadow:0 25px 70px rgba(0,0,0,0.55),0 0 40px rgba(255,107,157,0.15),inset 0 1px 0 rgba(255,255,255,0.2);margin:20px 0 34px;position:relative;z-index:2;transition:opacity 0.5s ease,transform 0.5s ease;}
  .final-card::before{content:'';position:absolute;inset:-1px;border-radius:28px;padding:1px;background:linear-gradient(160deg,rgba(255,180,210,0.7),rgba(255,107,157,0.1),rgba(255,180,210,0.5));-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;}
  .final-card.hidden{opacity:0;transform:scale(0.92);pointer-events:none;position:absolute;}
  .final-cake-wrap{position:relative;width:90px;height:90px;margin:0 auto 20px;display:flex;align-items:center;justify-content:center;}
  .final-cake-glow{position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle,rgba(255,200,80,0.35) 0%,transparent 70%);animation:glowPulse 2.5s ease-in-out infinite;}
  .final-cake{font-size:54px;position:relative;z-index:2;animation:floatFlower 3.5s ease-in-out infinite;}
  .final-title{font-family:'Playfair Display',serif;font-size:36px;color:#fff;margin-bottom:10px;text-shadow:0 2px 20px rgba(255,150,180,0.4);}
  .final-sub{font-size:14px;color:rgba(255,220,230,0.7);margin-bottom:30px;letter-spacing:0.3px;}
  .final-close{background:rgba(255,107,157,0.18);border:1px solid rgba(255,107,157,0.4);color:#fff;font-size:13px;padding:12px 28px;border-radius:50px;cursor:pointer;letter-spacing:0.5px;transition:all 0.2s ease;}
  .final-close:hover{background:rgba(255,107,157,0.35);border-color:rgba(255,107,157,0.6);transform:scale(1.04);}
  .final-footer{font-family:'Playfair Display',serif;font-style:italic;font-size:15px;color:rgba(255,255,255,0.55);position:relative;z-index:2;}

  /* WRONG */
  .overlay{position:fixed;inset:0;background:rgba(0,0,0,0.65);display:none;align-items:center;justify-content:center;z-index:999;backdrop-filter:blur(6px);}
  .overlay.show{display:flex;}
  .msg-box{background:linear-gradient(135deg,#6b2d4e,#3d1a2e);border:1px solid rgba(255,150,180,0.3);border-radius:22px;padding:36px 30px;text-align:center;color:#fff;max-width:280px;animation:popIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275);}
  .msg-box .big{font-size:54px;display:block;margin-bottom:12px;}
  .msg-box h2{font-family:'Playfair Display',serif;font-size:21px;color:#ffb3cc;margin-bottom:8px;}
  .msg-box p{font-size:13px;color:rgba(255,255,255,0.7);line-height:1.6;}
  .msg-btn{margin-top:18px;padding:10px 26px;border-radius:50px;cursor:pointer;font-size:13px;color:#fff;background:rgba(255,107,157,0.35);border:1px solid #ff6b9d;transition:background 0.2s;}
  .msg-btn:hover{background:rgba(255,107,157,0.55);}
</style>
</head>
<body>

<canvas id="flowerCanvas"></canvas>
<canvas id="burstCanvas"></canvas>

<!-- SPLASH -->
<div id="splashScreen">
  <div class="flower-logo">
    <div class="flower-glow"></div>
    <div class="petal"></div><div class="petal"></div><div class="petal"></div>
    <div class="petal"></div><div class="petal"></div><div class="petal"></div>
    <div class="flower-center"></div>
  </div>
  <div class="preparing-text">Preparing something special for you<span class="dots"><span>.</span><span>.</span><span>.</span></span></div>
</div>
<div class="progress-bar-wrap"><div class="progress-bar" id="progressBar"></div></div>

<!-- PIN -->
<div id="pinScreen">
  <div class="card" id="card">
    <span class="top-flower-icon">🌸</span>
    <div class="card-title">For You, Idiot</div>
    <div class="card-sub">Enter our secret code</div>
    <div class="pin-dots">
      <div class="pin-dot" id="d0"></div><div class="pin-dot" id="d1"></div>
      <div class="pin-dot" id="d2"></div><div class="pin-dot" id="d3"></div>
      <div class="pin-dot" id="d4"></div><div class="pin-dot" id="d5"></div>
    </div>
    <div class="numpad">
      <button class="num-btn" onclick="press('1')">1</button>
      <button class="num-btn" onclick="press('2')">2</button>
      <button class="num-btn" onclick="press('3')">3</button>
      <button class="num-btn" onclick="press('4')">4</button>
      <button class="num-btn" onclick="press('5')">5</button>
      <button class="num-btn" onclick="press('6')">6</button>
      <button class="num-btn" onclick="press('7')">7</button>
      <button class="num-btn" onclick="press('8')">8</button>
      <button class="num-btn" onclick="press('9')">9</button>
      <button class="num-btn" onclick="del()">✕</button>
      <button class="num-btn" onclick="press('0')">0</button>
      <button class="num-btn enter-btn" onclick="enter()">↵</button>
    </div>
    <div class="hint">Hint: DDMMYY💕</div>
  </div>
</div>

<!-- GIFT -->
<div id="giftScreen">
  <div class="tap-hint" id="tapHint">Tap the gift to open it 🎁</div>
  <div class="gift-wrap" id="giftBox" onclick="tapGift()">
    <div class="sparkle"></div><div class="sparkle"></div>
    <div class="sparkle"></div><div class="sparkle"></div>
    <div class="sparkle"></div><div class="sparkle"></div>
    <svg width="210" height="200" viewBox="0 0 210 200" fill="none">
      <rect x="22" y="90" width="166" height="100" rx="8" fill="#d96fa0"/>
      <rect x="12" y="68" width="186" height="30" rx="7" fill="#e07fb0"/>
      <rect x="90" y="90" width="30" height="100" fill="#f5c200"/>
      <rect x="22" y="130" width="166" height="22" fill="#f5c200"/>
      <rect x="90" y="68" width="30" height="30" fill="#f5c200"/>
      <rect x="12" y="79" width="186" height="10" fill="#f5c200"/>
      <ellipse cx="74" cy="57" rx="30" ry="18" fill="#f5c200" transform="rotate(-18 74 57)"/>
      <ellipse cx="136" cy="57" rx="30" ry="18" fill="#f5c200" transform="rotate(18 136 57)"/>
      <ellipse cx="105" cy="64" rx="15" ry="12" fill="#e6b000"/>
      <polygon points="105,38 93,64 117,64" fill="#f5c200"/>
      <rect x="30" y="98" width="8" height="50" rx="4" fill="rgba(255,255,255,0.18)"/>
      <ellipse cx="105" cy="196" rx="72" ry="6" fill="rgba(0,0,0,0.18)"/>
    </svg>
  </div>
</div>

<!-- MAIN SCROLL -->
<div id="mainScroll">

  <!-- SEC 1: BIRTHDAY -->
  <div id="sec-birthday">
    <span class="bd-fl" style="top:6%;left:10%;animation-delay:0s;">🌸</span>
    <span class="bd-fl" style="top:8%;right:12%;animation-delay:0.5s;">🌺</span>
    <span class="bd-fl" style="top:20%;left:4%;animation-delay:1s;font-size:16px;">🌼</span>
    <span class="bd-fl" style="top:20%;right:5%;animation-delay:0.3s;">🌹</span>
    <span class="bd-fl" style="top:38%;left:3%;animation-delay:0.8s;font-size:16px;">🌷</span>
    <span class="bd-fl" style="top:55%;right:4%;animation-delay:1.2s;">🌸</span>
    <span class="bd-fl" style="bottom:22%;left:8%;animation-delay:0.6s;font-size:14px;">✿</span>
    <span class="bd-fl" style="bottom:14%;right:10%;animation-delay:1s;font-size:16px;">🌺</span>
    <span class="bd-fl" style="bottom:8%;left:30%;animation-delay:0.4s;font-size:12px;">❀</span>
    <div class="bd-tag">— Your Special Day —</div>
    <div class="bd-happy">Happy</div>
    <div class="bd-birthday">Birthday</div>
    <div class="bd-name">Pranzsss</div>
    <div class="bd-divider"></div>
    <div class="bd-date">MAY 25 · THE MOST SPECIAL DAY</div>
    <div class="scroll-down-hint"><div class="arrow-d"></div><span>SCROLL</span></div>
  </div>

  <!-- SEC 2: BOUQUET -->
  <div id="sec-bouquet">
    <div class="bq-heading-wrap">
      <div class="bq-tag">— FOR YOU —</div>
      <div class="bq-title">A Virtual Bouquet for You 💐</div>
      <div class="bq-subtitle">Press the scattered flowers ✦</div>
    </div>

    <div id="vaseArea">
      <span class="sc-outer" data-msg="0"  style="top:4%;left:4%;animation-delay:0s;font-size:24px;">🌸</span>
      <span class="sc-outer" data-msg="1"  style="top:4%;right:5%;animation-delay:0.4s;font-size:22px;">🌺</span>
      <span class="sc-outer" data-msg="2"  style="top:17%;left:1%;animation-delay:0.8s;font-size:20px;">🌹</span>
      <span class="sc-outer" data-msg="3"  style="top:17%;right:1%;animation-delay:1.2s;font-size:20px;">🌼</span>
      <span class="sc-outer" data-msg="4"  style="top:34%;left:1%;animation-delay:0.3s;font-size:18px;">🌷</span>
      <span class="sc-outer" data-msg="5"  style="top:34%;right:1%;animation-delay:0.7s;font-size:16px;">🌻</span>
      <span class="sc-outer" data-msg="6"  style="top:52%;left:2%;animation-delay:1.1s;font-size:18px;">🌸</span>
      <span class="sc-outer" data-msg="7"  style="top:52%;right:2%;animation-delay:0.5s;font-size:16px;">✿</span>
      <span class="sc-outer" data-msg="8"  style="top:70%;left:5%;animation-delay:0.9s;font-size:16px;">🌺</span>
      <span class="sc-outer" data-msg="9"  style="top:70%;right:5%;animation-delay:1.4s;font-size:14px;">❀</span>
      <span class="sc-outer" data-msg="10" style="top:83%;left:16%;animation-delay:0.6s;font-size:14px;">🌼</span>
      <span class="sc-outer" data-msg="11" style="top:83%;right:16%;animation-delay:1.0s;font-size:14px;">✦</span>

      <div style="position:relative;display:flex;align-items:center;justify-content:center;">
        <svg width="260" height="390" viewBox="0 0 260 390" fill="none">
          <line x1="130" y1="295" x2="100" y2="155" stroke="#5a8a5a" stroke-width="3" stroke-linecap="round"/>
          <line x1="130" y1="295" x2="120" y2="140" stroke="#5a8a5a" stroke-width="3" stroke-linecap="round"/>
          <line x1="130" y1="295" x2="130" y2="130" stroke="#5a8a5a" stroke-width="3.5" stroke-linecap="round"/>
          <line x1="130" y1="295" x2="145" y2="143" stroke="#5a8a5a" stroke-width="3" stroke-linecap="round"/>
          <line x1="130" y1="295" x2="162" y2="160" stroke="#5a8a5a" stroke-width="3" stroke-linecap="round"/>
          <line x1="130" y1="295" x2="85"  y2="178" stroke="#5a8a5a" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="130" y1="295" x2="175" y2="182" stroke="#5a8a5a" stroke-width="2.5" stroke-linecap="round"/>
          <ellipse cx="108" cy="228" rx="14" ry="6" fill="#5a8a5a" transform="rotate(-40 108 228)"/>
          <ellipse cx="152" cy="222" rx="14" ry="6" fill="#6aaa5a" transform="rotate(38 152 222)"/>
          <ellipse cx="118" cy="264" rx="10" ry="5" fill="#5a8a5a" transform="rotate(20 118 264)"/>
          <ellipse cx="143" cy="258" rx="10" ry="5" fill="#6aaa5a" transform="rotate(-22 143 258)"/>
          <circle cx="85" cy="173" r="14" fill="#f090b0"/><circle cx="85" cy="173" r="9" fill="#e06090"/><circle cx="85" cy="173" r="5" fill="#c84070"/>
          <ellipse cx="85" cy="158" rx="6" ry="9" fill="#f5a0c0" opacity="0.8"/><ellipse cx="75" cy="167" rx="9" ry="6" fill="#f5a0c0" opacity="0.8"/><ellipse cx="95" cy="167" rx="9" ry="6" fill="#f5a0c0" opacity="0.8"/>
          <ellipse cx="120" cy="133" rx="7" ry="13" fill="#b090d0"/><ellipse cx="113" cy="127" rx="6" ry="11" fill="#c8a8e8"/><ellipse cx="127" cy="127" rx="6" ry="11" fill="#9878c0"/><circle cx="120" cy="120" r="5" fill="#d0b0f0"/>
          <circle cx="130" cy="123" r="13" fill="#f5c200"/><circle cx="130" cy="123" r="8" fill="#b86010"/>
          <ellipse cx="130" cy="107" rx="5" ry="9" fill="#f5c200"/><ellipse cx="130" cy="139" rx="5" ry="9" fill="#f5c200"/><ellipse cx="114" cy="123" rx="9" ry="5" fill="#f5c200"/><ellipse cx="146" cy="123" rx="9" ry="5" fill="#f5c200"/>
          <ellipse cx="145" cy="135" rx="9" ry="16" fill="#e07090"/><ellipse cx="154" cy="131" rx="7" ry="13" fill="#f090aa"/><ellipse cx="136" cy="131" rx="7" ry="13" fill="#c05070"/>
          <circle cx="162" cy="153" r="10" fill="#fff5f8"/><circle cx="162" cy="153" r="5" fill="#f5c200"/>
          <ellipse cx="162" cy="140" rx="4" ry="8" fill="#fff5f8"/><ellipse cx="162" cy="166" rx="4" ry="8" fill="#fff5f8"/><ellipse cx="149" cy="153" rx="8" ry="4" fill="#fff5f8"/><ellipse cx="175" cy="153" rx="8" ry="4" fill="#fff5f8"/>
          <circle cx="100" cy="147" r="9" fill="#ffb3cc"/><circle cx="100" cy="147" r="4" fill="#ff6b9d"/>
          <ellipse cx="100" cy="135" rx="4" ry="7" fill="#ffc8dc"/><ellipse cx="90" cy="145" rx="7" ry="4" fill="#ffc8dc"/><ellipse cx="110" cy="149" rx="7" ry="4" fill="#ffc8dc"/>
          <circle cx="175" cy="176" r="8" fill="#f0a0c0"/><circle cx="175" cy="176" r="3.5" fill="#d06090"/>
          <ellipse cx="175" cy="166" rx="3.5" ry="6" fill="#f8c0d8"/><ellipse cx="165" cy="174" rx="6" ry="3.5" fill="#f8c0d8"/><ellipse cx="185" cy="178" rx="6" ry="3.5" fill="#f8c0d8"/>
          <rect x="90" y="295" width="80" height="78" rx="8" fill="#d96fa0"/>
          <rect x="95" y="285" width="70" height="20" rx="6" fill="#e07fb0"/>
          <circle cx="100" cy="288" r="14" fill="#e8a0b8"/>
          <circle cx="160" cy="288" r="14" fill="#e8a0b8"/>
          <ellipse cx="107" cy="317" rx="6" ry="14" fill="rgba(255,255,255,0.18)" transform="rotate(-10 107 317)"/>
          <ellipse cx="130" cy="376" rx="52" ry="7" fill="rgba(0,0,0,0.2)"/>
        </svg>
      </div>
    </div>

    <div id="msgBar">
      <div id="msgText">🌸 Press any scattered flower to reveal a message for you...</div>
    </div>
  </div>

  <!-- SEC 3: LETTER -->
  <div id="sec-letter">
    <span class="le-fl" style="top:2%;right:8%;animation-delay:0s;">🌸</span>
    <span class="le-fl" style="top:5%;left:6%;animation-delay:0.5s;">✿</span>
    <span class="le-fl" style="top:18%;right:4%;animation-delay:1s;">🌺</span>
    <span class="le-fl" style="top:30%;left:4%;animation-delay:0.7s;">🌼</span>
    <span class="le-fl" style="bottom:18%;right:6%;animation-delay:0.9s;">🌷</span>
    <span class="le-fl" style="bottom:8%;left:15%;animation-delay:1.2s;">🌻</span>
    <div class="ltr-quote">You are as beautiful as cherry blossoms — lovely<br>and bringing joy wherever you go. 🌸</div>
    <div class="ltr-section-tag">— FROM MY HEART 🌸 —</div>
    <div class="ltr-title">A Letter For You</div>
    <div class="letter-card">
      <div style="text-align:center;font-size:13px;color:rgba(90,42,58,0.3);margin-bottom:6px;">✦ + ✦</div>
      <div class="letter-date">May 25</div>
      <div style="display:flex;justify-content:space-between;font-size:18px;margin-bottom:14px;"><span>🌸</span><span>🌼</span><span>🌺</span></div>
      <div class="letter-dear">Dear and Rhino Pranzxsss Gundini,</div>
      <div class="letter-body">
        <p>On this most special day, I want you to know that every single day with you is a gift beyond measure. You bring light into every corner of my life — even on the darkest days.</p>
        <p>Your laughter is the most beautiful music I have ever heard. The way you see the world — with wonder and kindness — inspires me to be better every single day.</p>
        <p>Happy Birthday, Idiot. Today and every day, I am so grateful that you exist. 🌸</p>
        <p>May this day bring you all the joy, warmth, and magic that you bring to my life — and so much more.</p>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:16px;margin:16px 0 8px;"><span>🌹</span><span>💕</span><span>🌷</span></div>
      <div class="letter-sig">Wishing u all the best, with all happiness 💖</div>
    </div>
  </div>

  <!-- SEC 4: PHOTOS -->
  <div id="sec-photos">
    <div class="photos-tag">— A COLLECTION OF MEMORIES —</div>
    <div class="photos-title">Our Photo Memories</div>
    <div class="photos-sub">Every picture holds a beautiful story</div>
    <div id="photosContainer" style="display:flex;flex-wrap:wrap;justify-content:center;max-width:400px;"></div>
  </div>

  <!-- SEC 5: JOURNEY -->
  <div id="sec-journey">
    <div class="jrn-tag">— OUR JOURNEY —</div>
    <div class="jrn-title">Memories We've Written Together</div>
    <div class="jrn-star">✽</div>
    <div class="timeline">
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-card"><div class="tl-icon">✨</div><div class="tl-label">The Very Beginning</div><div class="tl-heading">First Time We Met</div><div class="tl-body">The day the world seemed to spin a little faster and everything felt different from before.</div></div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-card"><div class="tl-icon">💬</div><div class="tl-label">A Magical Moment</div><div class="tl-heading">Our First Conversation</div><div class="tl-body">The first words spoken, the first laughter shared — the beginning of thousands of stories we would write together.</div></div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-card"><div class="tl-icon">🌅</div><div class="tl-label">A Cherished Memory</div><div class="tl-heading">Our First Call</div><div class="tl-body">Lekhda gayeb hunxau so i called u yaad xa malai</div></div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-card"><div class="tl-icon">☕</div><div class="tl-label">Our Little World</div><div class="tl-heading">The Café in the Corner</div><div class="tl-body">Our table. Our orders. Our conversations that stretched from morning into evening. That place will always be ours.</div></div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-card"><div class="tl-icon">🌙</div><div class="tl-label">Quiet and Precious</div><div class="tl-heading">Late Night Talks</div><div class="tl-body">When the world was asleep and it was just us — sharing our dreams, fears, and everything in between.</div></div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-card"><div class="tl-icon">💖</div><div class="tl-label">Today and Always</div><div class="tl-heading">Happy Birthday, Pranzssss</div><div class="tl-body">Every chapter of our story is my favourite. I cannot wait to write every single one that comes next — with you. 🌸</div></div></div>
    </div>
    <div class="end-row">🌸 💖 🌸</div>
  </div>

  <!-- SEC 6: MUSIC PLAYER (YouTube embed, inline) -->
  <div id="sec-music">
    <span class="mus-fl" style="top:3%;left:8%;animation-delay:0s;">✽</span>
    <span class="mus-fl" style="top:3%;right:8%;animation-delay:0.5s;">✦</span>
    <span class="mus-fl" style="top:18%;left:4%;animation-delay:1s;">❊</span>
    <span class="mus-fl" style="top:18%;right:4%;animation-delay:0.8s;">✽</span>
    <span class="mus-fl" style="bottom:18%;left:6%;animation-delay:0.3s;">✦</span>
    <span class="mus-fl" style="bottom:18%;right:6%;animation-delay:1.2s;">❊</span>
    <div class="mus-sunflower">🌻</div>
    <div class="mus-tag">OUR SONGS</div>
    <div class="mus-title">Special Playlist</div>
    <div class="mus-sub">Songs that always remind me of you</div>

    <div class="player-card">
      <div class="video-wrap" id="videoWrap" onclick="playInline()">
        <img id="videoThumb" src="https://img.youtube.com/vi/JGwWNGJdvx8/hqdefault.jpg" alt="song thumbnail"/>
        <div class="video-play-overlay" id="videoOverlay">
          <div class="video-play-btn"></div>
        </div>
        <span class="video-tap-hint" id="videoTapHint">Tap to play</span>
      </div>
      <div class="song-title" id="songTitle">Be my Baby</div>
      <div class="song-artist" id="songArtist">Tap the video to play right here</div>
    </div>

    <div class="playlist">
      <div class="pl-label">— PLAYLIST —</div>
      <div id="playlistItems"></div>
    </div>
  </div>

  <!-- SEC 7: GRATITUDE JAR -->
  <div id="sec-jar">
    <span class="jar-fl" style="top:5%;left:10%;animation-delay:0s;">🌸</span>
    <span class="jar-fl" style="top:8%;right:12%;animation-delay:0.5s;">✿</span>
    <span class="jar-fl" style="bottom:20%;left:8%;animation-delay:1s;">🌺</span>
    <span class="jar-fl" style="bottom:12%;right:10%;animation-delay:0.7s;">❀</span>
    <div class="jar-tag">— FROM MY HEART TO YOURS —</div>
    <div class="jar-title">Reasons I'm Grateful to Know You</div>
    <div class="jar-sub">Shake the jar and pick a note 🎐</div>

    <div class="jar-svg-wrap" id="jarWrap" onclick="shakeJar()">
      <svg width="150" height="230" viewBox="0 0 150 230" fill="none">
        <rect x="45" y="10" width="60" height="26" rx="6" fill="#e0508a"/>
        <rect x="40" y="30" width="70" height="14" rx="4" fill="#d94a80"/>
        <rect x="35" y="42" width="80" height="178" rx="18" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.18)" stroke-width="2"/>
        <rect x="35" y="42" width="80" height="178" rx="18" fill="url(#jarGrad)" opacity="0.5"/>
        <defs>
          <linearGradient id="jarGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#7a2848"/>
            <stop offset="100%" stop-color="#4a1830"/>
          </linearGradient>
        </defs>
        <rect x="55" y="95" width="24" height="15" rx="2" fill="#f6c8d8" opacity="0.9" transform="rotate(-6 55 95)"/>
        <rect x="70" y="118" width="24" height="15" rx="2" fill="#f0a8c0" opacity="0.9" transform="rotate(5 70 118)"/>
        <rect x="52" y="140" width="24" height="15" rx="2" fill="#f6c8d8" opacity="0.9" transform="rotate(-4 52 140)"/>
        <rect x="68" y="163" width="24" height="15" rx="2" fill="#f0a8c0" opacity="0.9" transform="rotate(7 68 163)"/>
        <rect x="54" y="186" width="24" height="15" rx="2" fill="#f6c8d8" opacity="0.9" transform="rotate(-3 54 186)"/>
        <rect x="40" y="46" width="10" height="168" rx="5" fill="rgba(255,255,255,0.12)"/>
      </svg>
    </div>

    <button class="jar-btn" onclick="shakeJar()">🎐 Shake the Jar</button>

    <div class="jar-note" id="jarNote">
      <span class="jar-note-mark">✦</span>
      <div class="jar-note-text" id="jarNoteText">Tap the jar to reveal a reason.</div>
    </div>
  </div>

  <!-- SEC 8: FINAL BIRTHDAY CARD -->
  <div id="sec-final">
    <canvas id="finalFlowerCanvas"></canvas>

    <div class="final-card" id="finalCard">
      <div class="final-cake-wrap">
        <div class="final-cake-glow"></div>
        <div class="final-cake">🎂</div>
      </div>
      <div class="final-title">Happy Birthday!</div>
      <div class="final-sub">The most special Pranzzssssssssssssssssssssssss 🌸</div>
      <button class="final-close" onclick="closeFinalCard()">Close ✕</button>
    </div>

    <video id="finalPhoto" class="final-card hidden" src="" style="object-fit:cover;padding:0;" loop muted playsinline controls></video>

    <div class="final-footer">— With love that never runs out 💕 —</div>
  </div>

</div><!-- end mainScroll -->

<!-- LIGHTBOX -->
<div id="lightbox" onclick="closeLightbox()">
  <div id="lbImg" onclick="event.stopPropagation()">
    <div class="polaroid-img" id="lbEmoji" style="height:240px;font-size:80px;"></div>
    <div id="lbCaption"></div>
  </div>
  <div id="lbClose" onclick="closeLightbox()">✕ Close</div>
</div>

<!-- WRONG -->
<div class="overlay" id="wrongOverlay">
  <div class="msg-box">
    <span class="big">🥺</span>
    <h2>Try Again, Love</h2>
    <p>That's not quite right... Think about our most special day 💭</p>
    <button class="msg-btn" onclick="closeOverlay('wrongOverlay')">Try Again 🌸</button>
  </div>
</div>

<script>
// ══════════════════════════════════════════════════════════
// ✏️  EDIT EVERYTHING HERE — ONE PLACE, UPDATES THE WHOLE PAGE
// ══════════════════════════════════════════════════════════
const CONFIG = {
  // Final section media — shown after "Close ✕" is tapped.
  // type: "video" or "image"
  finalMedia: {
    type: "video",
    src: "%%FINAL_VIDEO_SRC%%"   // put your video (or image) URL / path here
  },

  // Songs — paste any full YouTube URL (youtu.be/..., watch?v=..., or embed/...)
  // "name" is shown as the title and in the playlist.
  songs: [
    { url: "https://www.youtube.com/watch?v=4tPJPE4uOEo", name: "Be My baby" },
    { url: "https://www.youtube.com/watch?v=p-pfPYWjUBY", name: "All I dream of is your eyes" }
  ],

  // Photo memories — one card per entry. "src" can be an emoji (shown big)
  // or an image URL/data-URI (jpg/png/etc).
  photos: %%PHOTOS_JSON%%
};

// Pulls the 11-char YouTube video ID out of any common URL shape
function extractYouTubeId(url){
  const m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_-]{11})/);
  return m ? m[1] : url; // fall back to raw string if it's already just an ID
}

const TRACKS = CONFIG.songs.map(s => ({ id: extractYouTubeId(s.url), name: s.name }));

// ══ CANVAS PETALS ══
const canvas=document.getElementById("flowerCanvas"),ctx=canvas.getContext("2d");
const SYMS=["✿","❀","✽","❁","✦","·","*","❊","✾"];
let petals=[];
function resize(){canvas.width=innerWidth;canvas.height=innerHeight;}
resize();window.addEventListener("resize",resize);
function newPetal(){return{x:Math.random()*canvas.width,y:-20,size:Math.random()*13+6,speed:Math.random()*1+0.35,drift:(Math.random()-0.5)*0.65,rot:Math.random()*Math.PI*2,rotS:(Math.random()-0.5)*0.035,alpha:Math.random()*0.45+0.2,sym:SYMS[Math.floor(Math.random()*SYMS.length)],hue:Math.floor(Math.random()*40+320)};}
for(let i=0;i<45;i++){const p=newPetal();p.y=Math.random()*canvas.height;petals.push(p);}
(function loop(){ctx.clearRect(0,0,canvas.width,canvas.height);if(petals.length<70&&Math.random()<0.18)petals.push(newPetal());petals.forEach((p,i)=>{ctx.save();ctx.globalAlpha=p.alpha;ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.font=p.size+"px serif";ctx.fillStyle=`hsl(${p.hue},75%,80%)`;ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(p.sym,0,0);ctx.restore();p.y+=p.speed;p.x+=p.drift;p.rot+=p.rotS;if(p.y>canvas.height+30)petals[i]=newPetal();});requestAnimationFrame(loop);})();

// ══ SPLASH ══
setTimeout(()=>{document.getElementById("splashScreen").classList.add("hide");document.getElementById("progressBar").parentElement.style.display="none";setTimeout(()=>document.getElementById("pinScreen").classList.add("show"),600);},5000);

// ══ PIN ══
const SECRET="250505",SLOTS=6;let pin="";
function press(k){if(pin.length<SLOTS){pin+=k;renderDots();}}
function del(){pin=pin.slice(0,-1);renderDots();}
function enter(){
  if(!pin.length)return;
  if(pin===SECRET){
    document.getElementById("pinScreen").classList.remove("show");
    setTimeout(()=>{document.getElementById("giftScreen").classList.add("show");setTimeout(()=>document.getElementById("tapHint").classList.add("vis"),400);},600);
  }else{
    document.getElementById("wrongOverlay").classList.add("show");
    const c=document.getElementById("card");c.classList.add("shake");setTimeout(()=>c.classList.remove("shake"),450);pin="";renderDots();
  }
}
function closeOverlay(id){document.getElementById(id).classList.remove("show");}
function renderDots(){for(let i=0;i<SLOTS;i++)document.getElementById("d"+i).classList.toggle("filled",i<pin.length);}

// ══ GIFT ══
let tapCount=0;
function tapGift(){
  tapCount++;
  const box=document.getElementById("giftBox");
  if(tapCount<3){box.classList.remove("gift-shake-anim");void box.offsetWidth;box.classList.add("gift-shake-anim");setTimeout(()=>box.classList.remove("gift-shake-anim"),650);}
  else{box.classList.remove("gift-shake-anim");void box.offsetWidth;box.classList.add("gift-explode-anim");launchBurst();setTimeout(()=>{document.getElementById("giftScreen").classList.remove("show");setTimeout(()=>{const ms=document.getElementById("mainScroll");ms.classList.add("show");ms.scrollTop=0;},400);},800);}
}

// ══ FLOWERS ══
const FLOWER_MSGS=["🌸 You are the most beautiful person I have ever known.","🌺 Your smile lights up every room you walk into.","🌹 I fall in love with you more every single day.","🌼 Your kindness makes the world a warmer place.","🌷 Being with you is my favourite place in the world.","🌻 You inspire me to be the best version of myself.","🌸 Your laughter is the most beautiful sound I know.","✿  Every moment with you is a memory I treasure forever.","🌺 You are my sunshine on the cloudiest of days.","❀  I am so grateful the universe brought us together.","🌼 You make ordinary days feel magical and special.","✦  My love for you grows deeper with every breath."];
document.querySelectorAll(".sc-outer").forEach(el=>{el.addEventListener("click",function(e){e.stopPropagation();const idx=parseInt(this.dataset.msg);this.classList.remove("bloom-once");void this.offsetWidth;this.classList.add("bloom-once");setTimeout(()=>this.classList.remove("bloom-once"),520);miniBloom(this);const msgEl=document.getElementById("msgText");msgEl.classList.add("fade");setTimeout(()=>{msgEl.textContent=FLOWER_MSGS[idx]||FLOWER_MSGS[0];msgEl.classList.remove("fade");},420);});});
function miniBloom(el){const rect=el.getBoundingClientRect(),cx=rect.left+rect.width/2,cy=rect.top+rect.height/2;const ems=["🌸","💕","✿","❀","💗","✦","🌺","🌼"];for(let i=0;i<7;i++){const s=document.createElement("span");s.textContent=ems[Math.floor(Math.random()*ems.length)];s.style.cssText=`position:fixed;left:${cx}px;top:${cy}px;font-size:${13+Math.random()*10}px;pointer-events:none;z-index:300;transition:all 0.7s ease;transform:translate(-50%,-50%);`;document.body.appendChild(s);requestAnimationFrame(()=>{const a=Math.random()*Math.PI*2,d=55+Math.random()*65;s.style.transform=`translate(${Math.cos(a)*d-14}px,${Math.sin(a)*d-14}px)`;s.style.opacity="0";});setTimeout(()=>s.remove(),760);}}

// ══ PHOTO MEMORIES (built from CONFIG.photos) ══
const DECOS=["🌸","🌺","✿","🌼","🌷","🌹"];
// FIX: data: URIs weren't matched before, so base64 image strings were
// dumped into the DOM as raw text instead of rendered as <img>.
function isImageSrc(src){
  return /^data:image\//i.test(src) || /^(https?:)?\/\//.test(src) || /\.(png|jpe?g|gif|webp|svg)(\?.*)?$/i.test(src);
}

function buildPolaroids(){
  const container=document.getElementById("photosContainer");
  container.innerHTML = CONFIG.photos.map((p,i)=>{
    const side = i%2===0 ? "right" : "left";
    const vOff = i%2===0 ? "top:-8px;" : "bottom:-8px;";
    const inner = isImageSrc(p.src)
      ? '<img src="'+p.src+'" alt="memory photo" style="width:100%;height:100%;object-fit:cover;border-radius:2px;"/>'
      : p.src;
    return '<div class="polaroid-wrap" onclick="openLightbox('+i+')"><div class="tape"></div>'+
      '<div class="polaroid"><div class="polaroid-img">'+inner+'</div>'+
      '<div class="polaroid-caption">'+p.caption+'</div></div>'+
      '<span class="photo-deco" style="'+vOff+side+':8px;animation-delay:'+(i*0.3)+'s;">'+DECOS[i%DECOS.length]+'</span></div>';
  }).join('');
}
buildPolaroids();

function openLightbox(idx){
  const p=CONFIG.photos[idx];
  const lbEmoji=document.getElementById("lbEmoji");
  if(isImageSrc(p.src)){
    lbEmoji.innerHTML='<img src="'+p.src+'" alt="memory photo" style="width:100%;height:100%;object-fit:cover;border-radius:2px;"/>';
  }else{
    lbEmoji.innerHTML='';
    lbEmoji.textContent=p.src;
  }
  document.getElementById("lbCaption").textContent=p.caption;
  document.getElementById("lightbox").classList.add("open");
}
function closeLightbox(){document.getElementById("lightbox").classList.remove("open");}

// ══ CONFETTI ══
function launchBurst(){const bc=document.getElementById("burstCanvas");bc.width=innerWidth;bc.height=innerHeight;bc.style.display="block";const bctx=bc.getContext("2d"),cx=innerWidth/2,cy=innerHeight/2,pieces=[],COLORS=["#ff6b9d","#f5c200","#ff9aba","#ffffff","#ffb3cc","#e07fb0","#ffe680"];for(let i=0;i<140;i++){const a=Math.random()*Math.PI*2,s=Math.random()*12+4;pieces.push({x:cx,y:cy,vx:Math.cos(a)*s,vy:Math.sin(a)*s-Math.random()*5,w:Math.random()*10+4,h:Math.random()*6+3,color:COLORS[Math.floor(Math.random()*COLORS.length)],rot:Math.random()*Math.PI*2,rotS:(Math.random()-0.5)*0.22,alpha:1});}let frame=0;(function bloop(){bctx.clearRect(0,0,bc.width,bc.height);pieces.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=0.35;p.vx*=0.98;p.rot+=p.rotS;p.alpha-=0.017;if(p.alpha<=0)return;bctx.save();bctx.globalAlpha=p.alpha;bctx.translate(p.x,p.y);bctx.rotate(p.rot);bctx.fillStyle=p.color;bctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);bctx.restore();});frame++;if(frame<115)requestAnimationFrame(bloop);else bc.style.display="none";})();}

// ══ MUSIC PLAYER (inline YouTube iframe embed, built from CONFIG.songs) ══
let curTrackIdx=0;
let isPlayingInline=false;

function buildPlaylist(){
  const container=document.getElementById("playlistItems");
  container.innerHTML = TRACKS.map((t,i)=>
    '<div class="pl-item'+(i===0?' active':'')+'" id="pl'+i+'" onclick="loadTrack('+i+')">'+
      '<span class="pl-num" id="pn'+i+'">'+(i+1)+'</span>'+
      '<div class="pl-info"><div class="pl-name">'+t.name+'</div></div>'+
    '</div>'
  ).join('');
}

function updatePlaylistUI(idx){for(let i=0;i<TRACKS.length;i++){document.getElementById("pl"+i).classList.toggle("active", i===idx);}}

function renderThumb(idx){
  const wrap=document.getElementById("videoWrap");
  wrap.innerHTML=
    '<img id="videoThumb" src="https://img.youtube.com/vi/'+TRACKS[idx].id+'/hqdefault.jpg" alt="song thumbnail"/>'+
    '<div class="video-play-overlay" id="videoOverlay"><div class="video-play-btn"></div></div>'+
    '<span class="video-tap-hint" id="videoTapHint">Tap to play</span>';
  wrap.onclick=playInline;
  isPlayingInline=false;
}

function renderPlayer(idx){
  const wrap=document.getElementById("videoWrap");
  wrap.onclick=null;
  const origin=encodeURIComponent(window.location.origin);
  wrap.innerHTML=
    '<iframe src="https://www.youtube-nocookie.com/embed/'+TRACKS[idx].id+
    '?autoplay=1&playsinline=1&rel=0&modestbranding=1&origin='+origin+'" '+
    'title="song player" frameborder="0" referrerpolicy="strict-origin-when-cross-origin" '+
    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '+
    'allowfullscreen></iframe>';
  isPlayingInline=true;
}

function loadTrack(idx){
  curTrackIdx=idx;
  document.getElementById("songTitle").textContent=TRACKS[idx].name;
  updatePlaylistUI(idx);
  renderThumb(idx); // switching tracks resets to thumbnail; tap to play the new one
}

function playInline(){
  renderPlayer(curTrackIdx);
}

buildPlaylist();
loadTrack(0);

// ══ GRATITUDE JAR ══
const JAR_NOTES=[
  "Your spirit in the face of challenges inspires me every single day.",
  "The way you make everyone around you feel seen is a rare and beautiful gift.",
  "Your laugh is my favourite sound in the whole world.",
  "I'm grateful for how patient and kind you are, even on hard days.",
  "Knowing you has made my life so much brighter than it was before."
];
let lastJarIdx=-1;
function shakeJar(){
  const wrap=document.getElementById("jarWrap");
  wrap.classList.remove("shaking");
  void wrap.offsetWidth;
  wrap.classList.add("shaking");

  const noteEl=document.getElementById("jarNote");
  const textEl=document.getElementById("jarNoteText");
  noteEl.classList.remove("show");

  setTimeout(()=>{
    let idx;
    do{ idx=Math.floor(Math.random()*JAR_NOTES.length); }while(idx===lastJarIdx && JAR_NOTES.length>1);
    lastJarIdx=idx;
    textEl.textContent=JAR_NOTES[idx];
    noteEl.classList.add("show");
  },400);
}

// ══ FINAL SECTION — merging flower rain ══
const finalCanvas=document.getElementById("finalFlowerCanvas");
const finalCtx=finalCanvas.getContext("2d");
const FINAL_SYMS=["🌸","🌺","💕","🌼","✿","💗","❀","🌷"];
let finalPetals=[];
let finalRunning=false;
let finalRAF=null;

function finalResize(){
  const sec=document.getElementById("sec-final");
  finalCanvas.width=sec.clientWidth;
  finalCanvas.height=sec.clientHeight;
}
window.addEventListener("resize", finalResize);

function newFinalPetal(){
  return{
    x:Math.random()*finalCanvas.width,
    y:-30-Math.random()*200,
    size:Math.random()*22+18,
    speed:Math.random()*1.4+0.6,
    drift:(Math.random()-0.5)*0.8,
    rot:Math.random()*Math.PI*2,
    rotS:(Math.random()-0.5)*0.03,
    alpha:Math.random()*0.35+0.55,
    sym:FINAL_SYMS[Math.floor(Math.random()*FINAL_SYMS.length)]
  };
}
for(let i=0;i<26;i++){const p=newFinalPetal();p.y=Math.random()*400;finalPetals.push(p);}

function finalLoop(){
  if(!finalRunning)return;
  finalCtx.clearRect(0,0,finalCanvas.width,finalCanvas.height);
  if(finalPetals.length<40 && Math.random()<0.25) finalPetals.push(newFinalPetal());
  finalPetals.forEach((p,i)=>{
    finalCtx.save();
    finalCtx.globalAlpha=p.alpha;
    finalCtx.translate(p.x,p.y);
    finalCtx.rotate(p.rot);
    finalCtx.font=p.size+"px serif";
    finalCtx.textAlign="center";
    finalCtx.textBaseline="middle";
    finalCtx.fillText(p.sym,0,0);
    finalCtx.restore();
    p.y+=p.speed;
    p.x+=p.drift;
    p.rot+=p.rotS;
    if(p.y>finalCanvas.height+30) finalPetals[i]=newFinalPetal();
  });
  finalRAF=requestAnimationFrame(finalLoop);
}

const finalObserver=new IntersectionObserver((entries)=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      finalResize();
      if(!finalRunning){ finalRunning=true; finalLoop(); }
    }else{
      finalRunning=false;
      if(finalRAF) cancelAnimationFrame(finalRAF);
    }
  });
},{threshold:0.15});
finalObserver.observe(document.getElementById("sec-final"));

// ══ FINAL CARD ══
// ══ FINAL CARD (media driven by CONFIG.finalMedia) ══
function setupFinalMedia(){
  const old=document.getElementById("finalPhoto");
  if(CONFIG.finalMedia.type==="image"){
    const img=document.createElement("img");
    img.id="finalPhoto";
    img.className=old.className;
    img.style.cssText=old.style.cssText;
    img.src=CONFIG.finalMedia.src;
    img.alt="final photo";
    old.replaceWith(img);
  }else{
    old.src=CONFIG.finalMedia.src;
  }
}
setupFinalMedia();

function closeFinalCard(){
  document.getElementById("finalCard").classList.add("hidden");
  const media=document.getElementById("finalPhoto");
  media.classList.remove("hidden");
  if(media.tagName==="VIDEO") media.play().catch(()=>{});
}
</script>
</body>
</html>"""

HTML = HTML.replace("%%FINAL_VIDEO_SRC%%", FINAL_VIDEO_SRC)
HTML = HTML.replace("%%PHOTOS_JSON%%", PHOTOS_JSON)
components.html(HTML, height=780, scrolling=True)