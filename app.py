"""K-Town Roast: a self-contained premium cafe demo for Streamlit."""

from __future__ import annotations

import html
import re
from typing import Any

import streamlit as st
import streamlit.components.v1 as components


# Configuration
st.set_page_config(page_title="K-Town Roast | Karachi", page_icon="☕", layout="wide", initial_sidebar_state="collapsed")
BRAND = "K-Town Roast"
TAX_RATE = 0.05

# Menu Data
MENU: dict[str, list[dict[str, Any]]] = {
    "Hot Brews": [
        {"id": "espresso", "name": "Premium Espresso", "price": 450, "description": "A balanced, rich double shot with a smooth finish.", "category": "Hot Brews"},
        {"id": "vanilla-latte", "name": "DHA French Vanilla Latte", "price": 850, "description": "Velvety espresso, steamed milk and a gentle vanilla note.", "category": "Hot Brews"},
        {"id": "cortado", "name": "Spanish Cortado", "price": 680, "description": "Equal parts espresso and warm milk, served short.", "category": "Hot Brews"},
    ],
    "Cold Coffee": [
        {"id": "sea-view-frappe", "name": "Sea View Iced Frappe", "price": 1200, "description": "A chilled, creamy coffee made for long Karachi afternoons.", "category": "Cold Coffee"},
        {"id": "cold-brew", "name": "Signature Cold Brew", "price": 950, "description": "Slow-steeped for a clean, mellow cup over ice.", "category": "Cold Coffee"},
    ],
    "Gourmet Bites": [
        {"id": "cajun-sandwich", "name": "Smoked Cajun Chicken Sandwich", "price": 1650, "description": "Smoked chicken, Cajun seasoning and crisp greens.", "category": "Gourmet Bites"},
        {"id": "lava-cake", "name": "Belgian Chocolate Lava Cake", "price": 1450, "description": "Warm chocolate cake with a soft, molten centre.", "category": "Gourmet Bites"},
    ],
}
ITEMS = {item["id"]: item for group in MENU.values() for item in group}

# CSS
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --ink:#121212; --amber:#D4AF37; --cream:#E6C280; --white:#F5F5F5; --muted:#B8B8B8; }
.stApp { background:radial-gradient(ellipse at 82% 5%,rgba(212,175,55,.09),transparent 30%),#121212; color:var(--white); font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(18,18,18,.92); }
[data-testid="stMainBlockContainer"] { max-width:1380px; padding-top:3.8rem; padding-bottom:2rem; }
h1,h2,h3 { font-family:'Playfair Display',serif !important; color:var(--white) !important; letter-spacing:.01em; }
p,li,label,[data-testid="stMarkdownContainer"] { color:var(--white); }
.eyebrow { color:var(--cream); letter-spacing:.19em; text-transform:uppercase; font-size:.72rem; font-weight:700; }
.topbar { display:flex; align-items:center; justify-content:space-between; gap:1rem; border-bottom:1px solid rgba(255,255,255,.1); padding:.45rem 0 1.1rem; margin-bottom:1.4rem; }
.brandmark { font-family:'Playfair Display',serif; font-size:1.25rem; color:var(--white); font-weight:700; }
.brandmark span { color:var(--amber); }
.navhint { color:var(--muted); font-size:.88rem; }
.hero { border:1px solid rgba(230,194,128,.2); border-radius:24px; padding:clamp(1.4rem,4vw,3.4rem); background:linear-gradient(120deg,rgba(31,29,25,.96),rgba(21,21,20,.91)); box-shadow:0 22px 65px rgba(0,0,0,.24); }
.hero h1 { font-size:clamp(2.5rem,5vw,4.8rem); line-height:1.05; margin:.75rem 0 1rem; }
.hero h1 em { color:var(--cream); font-style:normal; }
.hero p { color:var(--muted); max-width:590px; line-height:1.75; font-size:1.04rem; }
.hero-meta { margin-top:1.35rem; color:var(--cream); font-size:.82rem; letter-spacing:.06em; }
.section-head { margin:2.5rem 0 1rem; }
.section-head p { color:var(--muted); margin-top:-.5rem; }
.menu-card,.panel,.brand-panel,.chat-shell { height:100%; background:rgba(25,25,25,.88); border:1px solid rgba(255,255,255,.09); border-radius:17px; padding:1.15rem; }
.menu-card { min-height:205px; display:flex; flex-direction:column; }
.menu-card h3 { font-size:1.16rem; margin:.35rem 0 .5rem; }
.menu-card p { color:var(--muted); font-size:.88rem; line-height:1.55; flex:1; }
.price { color:var(--cream); font-weight:700; font-size:1.05rem; }
.category-tag { color:var(--cream); text-transform:uppercase; letter-spacing:.14em; font-size:.65rem; font-weight:700; }
.brand-panel { padding:1.5rem; border-color:rgba(212,175,55,.16); }
.brand-panel strong { color:var(--cream); font-family:'Playfair Display',serif; font-size:1.25rem; }
.brand-panel p { color:var(--muted); margin:.5rem 0 0; }
.chat-shell { padding:1rem; }
.chat-msg { max-width:88%; border:1px solid rgba(255,255,255,.1); border-radius:14px; padding:.75rem .9rem; margin:.5rem 0; overflow-wrap:anywhere; line-height:1.55; white-space:pre-wrap; }
.chat-user { margin-left:auto; background:rgba(212,175,55,.12); border-color:rgba(212,175,55,.27); color:var(--white); }
.chat-assistant { margin-right:auto; background:rgba(255,255,255,.045); color:var(--white); }
.chat-msg small { color:var(--cream); font-weight:700; }
[data-testid="stPopoverBody"] { background:#191919 !important; border:1px solid rgba(230,194,128,.26) !important; color:#F5F5F5 !important; }
[data-testid="stPopoverBody"] p,[data-testid="stPopoverBody"] label { color:#F5F5F5 !important; }
[data-testid="stPopoverBody"] [data-testid="stVerticalBlockBorderWrapper"] { background:#191919 !important; border-color:rgba(255,255,255,.12) !important; }
.footer { border-top:1px solid rgba(255,255,255,.1); margin-top:3rem; padding-top:1.3rem; color:var(--muted); font-size:.84rem; }
.footer b { color:var(--cream); font-family:'Playfair Display',serif; font-size:1.1rem; }
div.stButton > button { border-radius:999px; border:1px solid rgba(212,175,55,.62); background:var(--amber); color:#121212; font-weight:700; min-height:2.65rem; transition:filter .15s ease,transform .15s ease; }
div.stButton > button:hover { color:#121212; filter:brightness(1.08); border-color:var(--cream); transform:translateY(-1px); }
div.stButton > button:focus { box-shadow:0 0 0 .2rem rgba(212,175,55,.3); }
div[data-testid="stTextInput"] input { background:#191919; color:var(--white); border-color:rgba(255,255,255,.15); border-radius:12px; }
div[data-testid="stTabs"] button { color:var(--muted); }
div[data-testid="stTabs"] button[aria-selected="true"] { color:var(--cream); }
[data-testid="stMetric"] { background:#191919; border:1px solid rgba(255,255,255,.09); border-radius:14px; padding:.8rem; }
[data-testid="stMetricValue"] { color:var(--cream); }
@media(max-width:768px) { [data-testid="stMainBlockContainer"]{padding:3.5rem 1rem 2rem}.hero{padding:1.4rem;border-radius:18px}.hero h1{font-size:2.65rem}.menu-card{min-height:unset;margin-bottom:.25rem}.navhint{font-size:.75rem}.chat-msg{max-width:96%} }
@media(max-width:420px) { .topbar{align-items:flex-start;flex-direction:column}.hero h1{font-size:2.25rem} }
</style>
"""


# Session State
def init_state() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "text": "Assalam-o-alaikum! I’m your K-Town Barista. Ask me about the menu, prices, or our Karachi locations."}]
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""


# Utility Functions
def money(amount: int | float) -> str:
    return f"Rs. {amount:,.0f}"


def add_to_cart(item_id: str) -> None:
    if item_id in ITEMS:
        st.session_state.cart[item_id] = max(0, int(st.session_state.cart.get(item_id, 0))) + 1


def change_quantity(item_id: str, delta: int) -> None:
    quantity = max(0, int(st.session_state.cart.get(item_id, 0)) + delta)
    if quantity:
        st.session_state.cart[item_id] = quantity
    else:
        st.session_state.cart.pop(item_id, None)


def cart_totals() -> tuple[int, int, int]:
    subtotal = sum(ITEMS[item_id]["price"] * max(0, int(qty)) for item_id, qty in st.session_state.cart.items() if item_id in ITEMS)
    tax = round(subtotal * TAX_RATE)
    return subtotal, tax, subtotal + tax


# AI Barista Engine: deterministic, Transformer-inspired intent simulation.
INTENT_TERMS: dict[str, tuple[str, ...]] = {
    "greeting": ("hello", "hi", "hey", "salam", "assalam", "aoa", "good morning", "good evening"),
    "menu": ("menu", "what do you have", "options", "serve", "available", "kya hai"),
    "price": ("price", "cost", "how much", "kitne", "qeemat", "rate", "rupees", "rs", "pkr"),
    "timing": ("time", "timing", "hours", "open", "close", "when", "kab"),
    "location": ("where", "location", "address", "karachi", "dha", "clifton", "kidhar", "kahan"),
    "recommendation": ("recommend", "suggest", "best", "what should", "mood", "pasand", "chai"),
}


def detect_intent(message: str) -> tuple[str, float]:
    normalized = re.sub(r"[^a-z0-9\s]", " ", message.lower())
    padded = f" {re.sub(r'\s+', ' ', normalized).strip()} "
    scores: dict[str, int] = {}
    for intent, terms in INTENT_TERMS.items():
        scores[intent] = sum(2 if " " in term else 1 for term in terms if f" {term} " in padded)
    best_intent = max(scores, key=scores.get) if scores else "fallback"
    score = scores.get(best_intent, 0)
    if score < 1:
        return "fallback", 0.0
    total = sum(scores.values())
    confidence = min(0.98, 0.55 + (score / max(total, 1)) * 0.4)
    return best_intent, confidence


def barista_reply(message: str) -> str:
    intent, _confidence = detect_intent(message)
    if intent == "greeting":
        return "Wa-alaikum-assalam! Good to have you here. Looking for a coffee, a sweet bite, or a little of both?"
    if intent == "menu":
        return "Our menu has Hot Brews, Cold Coffee, and Gourmet Bites. Try the Spanish Cortado, Signature Cold Brew, or Belgian Chocolate Lava Cake. Scroll to the menu to see every item and price."
    if intent == "price":
        matches = [item for item in ITEMS.values() if any(word in message.lower() for word in item["name"].lower().split() if len(word) > 3)]
        if matches:
            return "Here you go: " + "; ".join(f"{item['name']} is {money(item['price'])}" for item in matches[:3]) + "."
        return "Our menu runs from Rs. 450 for a Premium Espresso to Rs. 1,650 for the Smoked Cajun Chicken Sandwich. Every item and price is listed in the menu below."
    if intent == "timing":
        return "This demo doesn’t have verified cafe opening hours. Please check directly with the cafe for current timings."
    if intent == "location":
        return "The app lists Phase 6 DHA and E-Street Clifton, Karachi as sample brand locations. These are application content and haven’t been verified as real business addresses."
    if intent == "recommendation":
        return "For a smooth coffee, try our Signature Cold Brew. In the mood for something rich? Pair the Belgian Chocolate Lava Cake with a Premium Espresso."
    return "I can help with our menu, item prices, sample locations, or recommendations. What are you in the mood for?"


# 3D Hero Component
def render_lava_cake_scene() -> None:
    components.html("""<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:transparent}canvas{display:block;width:100%;height:100%}.fallback{position:absolute;inset:0;display:grid;place-items:center;color:#E6C280;font:14px sans-serif}</style></head><body>
<div id="fallback" class="fallback">Belgian chocolate lava cake</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><script>
try {
 const scene=new THREE.Scene(); scene.background=null;
 const camera=new THREE.PerspectiveCamera(34,innerWidth/innerHeight,.1,100);camera.position.set(0,1.7,7.8);camera.lookAt(0,.55,0);
 const renderer=new THREE.WebGLRenderer({alpha:true,antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));renderer.setSize(innerWidth,innerHeight);renderer.outputEncoding=THREE.sRGBEncoding;document.body.appendChild(renderer.domElement);document.getElementById('fallback').style.display='none';
 scene.add(new THREE.AmbientLight(0xffffff,.85));const key=new THREE.PointLight(0xE6C280,2.0,16);key.position.set(3,5,5);scene.add(key);const rim=new THREE.PointLight(0xD4AF37,1.3,14);rim.position.set(-4,2,-3);scene.add(rim);
 const cake=new THREE.Group();scene.add(cake);
 const baked=new THREE.MeshStandardMaterial({color:0x382016,roughness:.82});
 const cakeSide=new THREE.MeshStandardMaterial({color:0x4a291b,roughness:.68});
 const ganache=new THREE.MeshStandardMaterial({color:0x24130f,roughness:.19,metalness:.05});
 const plateMat=new THREE.MeshStandardMaterial({color:0xe8e0d0,roughness:.28,metalness:.08});
 const gold=new THREE.MeshStandardMaterial({color:0xD4AF37,metalness:.48,roughness:.26});
 const plate=new THREE.Mesh(new THREE.CylinderGeometry(1.4,1.33,.11,64),plateMat);plate.position.y=-.22;cake.add(plate);
 const plateLine=new THREE.Mesh(new THREE.TorusGeometry(1.25,.018,8,64),gold);plateLine.rotation.x=Math.PI/2;plateLine.position.y=-.16;cake.add(plateLine);
 const base=new THREE.Mesh(new THREE.CylinderGeometry(.82,.9,.12,64),baked);base.position.y=-.105;cake.add(base);
 const body=new THREE.Mesh(new THREE.CylinderGeometry(.79,.89,1.02,64,1,false),cakeSide);body.position.y=.46;cake.add(body);
 const top=new THREE.Mesh(new THREE.CylinderGeometry(.79,.79,.12,64),baked);top.position.y=1.03;cake.add(top);
 const chocolateTop=new THREE.Mesh(new THREE.CylinderGeometry(.78,.78,.045,64),ganache);chocolateTop.position.y=1.11;cake.add(chocolateTop);
 const molten=new THREE.Mesh(new THREE.SphereGeometry(.34,40,28),ganache);molten.scale.set(1,.26,1);molten.position.y=1.145;cake.add(molten);
 const flow=new THREE.Mesh(new THREE.TorusGeometry(.29,.055,14,48),new THREE.MeshStandardMaterial({color:0x603018,roughness:.22}));flow.rotation.x=Math.PI/2;flow.position.y=1.15;cake.add(flow);
 for(let i=0;i<9;i++){const a=i*Math.PI*2/9+.12;const drop=new THREE.Mesh(new THREE.SphereGeometry(1,18,14),ganache);drop.scale.set(.095,.22+(i%3)*.07,.095);drop.position.set(Math.cos(a)*.755,.91-(i%3)*.08,Math.sin(a)*.755);cake.add(drop)}
 const crumbs=new THREE.MeshStandardMaterial({color:0x9a6540,roughness:.92});
 for(let i=0;i<30;i++){const a=i*2.399;const r=.4+(i%7)*.045;const crumb=new THREE.Mesh(new THREE.SphereGeometry(.018+(i%3)*.006,8,6),crumbs);crumb.position.set(Math.cos(a)*r,1.145,Math.sin(a)*r);cake.add(crumb)}
 cake.rotation.z=-.045;
 const clock=new THREE.Clock();function animate(){requestAnimationFrame(animate);const t=clock.getElapsedTime();cake.rotation.y=Math.sin(t*.22)*.24;cake.position.y=Math.sin(t*.8)*.035;renderer.render(scene,camera)}animate();
 addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
} catch(e) { document.getElementById('fallback').style.display='grid'; }
</script></body></html>""", height=330, scrolling=False)


# Header / Navigation
def go_to_menu() -> None:
    """Select the menu before Streamlit recreates the navigation widget."""
    st.session_state.main_nav = "Menu"


def render_header() -> None:
    brand, location, chat = st.columns([3, 2, .55], vertical_alignment="center")
    with brand:
        st.markdown('<div class="brandmark">K-TOWN <span>ROAST</span></div>', unsafe_allow_html=True)
    with location:
        st.markdown('<div class="navhint">Karachi, Pakistan · Coffee, considered.</div>', unsafe_allow_html=True)
    with chat:
        with st.popover("💬", help="Open the K-Town AI Barista"):
            render_chat()


# Hero Section
def render_hero() -> None:
    left, right = st.columns([1.15, .85], vertical_alignment="center", gap="large")
    with left:
        st.markdown('<div class="hero"><div class="eyebrow">Specialty coffee · Karachi</div><h1>Brewed for Karachi.<br><em>Crafted for the moment.</em></h1><p>A thoughtful coffee ritual, a welcoming table, and the unmistakable energy of the coast. Find your next favourite at K-Town Roast.</p><div class="hero-meta">PREMIUM COFFEE &nbsp;·&nbsp; KARACHI &nbsp;·&nbsp; SINCE 2026</div></div>', unsafe_allow_html=True)
    with right:
        render_lava_cake_scene()


# Menu Section
def render_menu() -> None:
    st.markdown('<div class="section-head"><div class="eyebrow">Made for your moment</div><h2>Explore the menu</h2><p>Small rituals, carefully made. Prices are shown in Pakistani rupees.</p></div>', unsafe_allow_html=True)
    for category, items in MENU.items():
        st.markdown(f"### {html.escape(category)}")
        columns = st.columns(len(items), gap="medium")
        for column, item in zip(columns, items):
            with column:
                st.markdown(f'<div class="menu-card"><div class="category-tag">{html.escape(category)}</div><h3>{html.escape(item["name"])}</h3><p>{html.escape(item["description"])}</p><div class="price">{money(item["price"])}</div></div>', unsafe_allow_html=True)
                if st.button("Add to cart", key=f"add_{item['id']}", use_container_width=True):
                    add_to_cart(item["id"])
                    st.toast(f'{item["name"]} added to your cart.')


# Cart / Checkout
def render_cart() -> None:
    st.markdown('<div class="section-head"><div class="eyebrow">Your order</div><h2>Cart & checkout</h2><p>A simple checkout simulation. No payment is collected.</p></div>', unsafe_allow_html=True)
    with st.container(border=True):
        if not st.session_state.cart:
            st.markdown('<div class="panel"><h3>Your cart is taking a coffee break.</h3><p style="color:#B8B8B8">Add something from the menu and it will appear here.</p></div>', unsafe_allow_html=True)
            return
        for item_id, quantity in list(st.session_state.cart.items()):
            item = ITEMS.get(item_id)
            if not item:
                st.session_state.cart.pop(item_id, None)
                continue
            row = st.columns([4, 1, 1, 1, 1.4], vertical_alignment="center")
            row[0].markdown(f"**{item['name']}**  \n{money(item['price'])} each")
            row[1].markdown(f"Qty **{quantity}**")
            if row[2].button("−", key=f"minus_{item_id}"):
                change_quantity(item_id, -1)
                st.rerun()
            if row[3].button("+", key=f"plus_{item_id}"):
                change_quantity(item_id, 1)
                st.rerun()
            if row[4].button("Remove", key=f"remove_{item_id}"):
                st.session_state.cart.pop(item_id, None)
                st.rerun()
        subtotal, tax, total = cart_totals()
        st.divider()
        a, b = st.columns([2, 1])
        with b:
            st.markdown(f"Subtotal: **{money(subtotal)}**  \nTax (5%): **{money(tax)}**")
            st.markdown(f"### Total: {money(total)}")
            if st.button("Place demo order", key="checkout", use_container_width=True):
                st.success("Order simulation complete. Thank you for stopping by K-Town Roast!")
                st.session_state.cart.clear()
                st.rerun()
        if st.button("Clear cart", key="clear_cart"):
            st.session_state.cart.clear()
            st.rerun()


# AI Chatbot
def submit_chat() -> None:
    message = st.session_state.get("chat_input", "").strip()
    if not message:
        return
    st.session_state.chat_history.append({"role": "user", "text": message})
    try:
        reply = barista_reply(message)
    except (KeyError, TypeError, ValueError):
        reply = "Sorry, I couldn’t quite catch that. Ask me about our menu, prices, or recommendations."
    st.session_state.chat_history.append({"role": "assistant", "text": reply})
    st.session_state.chat_input = ""


def render_chat() -> None:
    st.markdown('<div class="section-head"><div class="eyebrow">A little help, anytime</div><h2>AI Barista</h2><p>Local intent simulation. No external AI service.</p></div>', unsafe_allow_html=True)
    with st.container(border=True):
        for message in st.session_state.chat_history:
            role_class = "chat-user" if message.get("role") == "user" else "chat-assistant"
            label = "You" if message.get("role") == "user" else "K-Town Barista"
            st.markdown(f'<div class="chat-msg {role_class}"><small>{label}</small><br>{html.escape(str(message.get("text", "")))}</div>', unsafe_allow_html=True)
        st.text_input("Message the barista", key="chat_input", placeholder="Try: What cold coffee do you recommend?", on_change=submit_chat, label_visibility="collapsed")
        if st.button("Send message", key="send_chat"):
            submit_chat()
            st.rerun()


# Social-proof / Brand Section
def render_brand() -> None:
    st.markdown('<div class="section-head"><div class="eyebrow">Crafted in Karachi</div></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    brand_content = (
        ("Specialty coffee.", "Thoughtful cups, from first sip to last.", "Explore our espresso, signature cold brew, and other carefully made drinks."),
        ("Late-night conversations.", "A good table makes room for a little longer.", "Tell our Barista what you are in the mood for using the chat icon above."),
        ("Coastal energy.", "Inspired by the city we call home.", "K-Town Roast is imagined around Karachi's coastal pace and neighbourhood spirit."),
    )
    for index, (col, (title, description, detail)) in enumerate(zip(cols, brand_content)):
        with col:
            st.markdown(f'<div class="brand-panel"><strong>{title}</strong><p>{description}</p></div>', unsafe_allow_html=True)
            if st.button("Discover", key=f"brand_discover_{index}", use_container_width=True, on_click=go_to_menu if index == 0 else None):
                st.session_state.selected_brand = title
            if st.session_state.get("selected_brand") == title:
                st.info(detail)
    st.markdown("<br>", unsafe_allow_html=True)
    _, menu_cta, _ = st.columns([1, 1.5, 1])
    with menu_cta:
        st.button("Explore the menu", key="home_explore_menu", use_container_width=True, on_click=go_to_menu)


# Footer
def render_footer() -> None:
    st.markdown('<div class="footer"><b>K-Town Roast</b><br>Brewed for Karachi. Crafted for the Moment.<br><br>Phase 6 DHA · E-Street Clifton · Karachi<br><small>Sample locations shown as application content; business addresses are not verified.<br>© 2026 K-Town Roast</small></div>', unsafe_allow_html=True)


# Main Application
def main() -> None:
    init_state()
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_header()
    render_hero()
    section = st.radio("Navigate", ["Home", "Menu", "Cart"], horizontal=True, key="main_nav", label_visibility="collapsed")
    if section == "Home":
        render_brand()
    elif section == "Menu":
        render_menu()
    else:
        render_cart()
    render_footer()


if __name__ == "__main__":
    main()
