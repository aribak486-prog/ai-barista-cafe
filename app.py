"""K-Town Roast: a self-contained premium cafe demo for Streamlit."""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components


# Configuration
st.set_page_config(page_title="K-Town Roast | Karachi", page_icon="☕", layout="wide", initial_sidebar_state="collapsed")
BRAND = "K-Town Roast"
TAX_RATE = 0.05
ASSET_DIR = Path(__file__).resolve().parent / "assets"

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


def get_asset_url(name: str, fallback_url: str) -> str:
    asset_path = ASSET_DIR / name
    return str(asset_path) if asset_path.exists() else fallback_url


# CSS
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --ink:#121212; --amber:#D4AF37; --cream:#E6C280; --white:#F5F5F5; --muted:#B8B8B8; }
.stApp { background:radial-gradient(ellipse at 82% 5%, rgba(212,175,55,.09), transparent 30%), #121212; color:var(--white); font-family:'DM Sans', sans-serif; }
[data-testid="stHeader"] { background:rgba(18,18,18,.92); }
[data-testid="stMainBlockContainer"] { max-width:1380px; padding-top:1.25rem; padding-bottom:calc(2rem + 72px + env(safe-area-inset-bottom)); }
h1,h2,h3 { font-family:'Playfair Display', serif !important; color:var(--white) !important; letter-spacing:.01em; }
p,li,label,[data-testid="stMarkdownContainer"] { color:var(--white); }
.eyebrow { color:var(--cream); letter-spacing:.19em; text-transform:uppercase; font-size:.72rem; font-weight:700; }
.topbar { display:flex; align-items:center; justify-content:space-between; gap:1rem; border-bottom:1px solid rgba(255,255,255,.1); padding:.45rem 0 1rem; margin-bottom:1.4rem; }
.brandmark { font-family:'Playfair Display',serif; font-size:1.25rem; color:var(--white); font-weight:700; }
.brandmark span { color:var(--amber); }
.navhint { color:var(--muted); font-size:.88rem; }
.stButton > button { border-radius:999px; border:1px solid rgba(212,175,55,.62); background:rgba(25,25,25,.88); color:var(--white); font-weight:700; min-height:2.65rem; transition:filter .15s ease,transform .15s ease; }
.stButton > button:hover { color:var(--white); filter:brightness(1.08); border-color:var(--cream); transform:translateY(-1px); }
.stButton > button:focus { box-shadow:0 0 0 .2rem rgba(212,175,55,.3); }
.st-key-main_navigation { background:rgba(18,18,18,.96); border-bottom:1px solid rgba(255,255,255,.12); padding:.45rem .8rem .15rem; margin:-.5rem -.8rem .8rem; }
.st-key-main_navigation [data-testid="stHorizontalBlock"] { align-items:center; gap:.5rem; }
.st-key-main_navigation .stButton > button { min-height:2.25rem; padding:.35rem .7rem; font-size:.88rem; line-height:1.15; white-space:nowrap; }
.st-key-main_navigation [data-testid="stCaptionContainer"] { padding-top:.2rem; font-size:.74rem; line-height:1.2; }
.nav-pill { background: rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.08); }
.nav-pill.active { background: rgba(212,175,55,.12); border-color: rgba(212,175,55,.32); }
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
.kt-lava-experience { background:rgba(18,18,18,.95); border:1px solid rgba(212,175,55,.25); border-radius:18px; padding:20px; backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); margin:20px 0; overflow-x:hidden; }
.kt-lava-experience h3 { color:#D4AF37; margin-top:0; margin-bottom:16px; font-size:18px; letter-spacing:.02em; }
.kt-lava-experience .status { color:#E6C280; font-size:13px; margin-bottom:12px; min-height:18px; }
.kt-lava-controls { display:flex; gap:12px; margin-top:16px; justify-content:center; flex-wrap:wrap; }
.kt-lava-controls button { background:rgba(212,175,55,.15); color:#D4AF37; border:1px solid rgba(212,175,55,.3); padding:8px 16px; border-radius:8px; font-size:13px; cursor:pointer; transition:all .2s ease; font-family:'DM Sans',sans-serif; }
.kt-lava-controls button:hover { background:rgba(212,175,55,.25); border-color:#D4AF37; }
.kt-lava-controls button:focus-visible { outline:2px solid #D4AF37; outline-offset:2px; }
.kt-lava-controls button:disabled { opacity:.4; cursor:not-allowed; }
div[data-testid="stTextInput"] input { background:#191919; color:var(--white); border-color:rgba(255,255,255,.15); border-radius:12px; }
div[data-testid="stTabs"] button { color:var(--muted); }
div[data-testid="stTabs"] button[aria-selected="true"] { color:var(--cream); }
[data-testid="stMetric"] { background:#191919; border:1px solid rgba(255,255,255,.09); border-radius:14px; padding:.8rem; }
[data-testid="stMetricValue"] { color:var(--cream); }
.st-key-chat_fab_toggle { position:fixed !important; right:clamp(16px,2vw,28px) !important; bottom:calc(18px + env(safe-area-inset-bottom)) !important; z-index:1002 !important; width:64px !important; height:64px !important; }
.st-key-chat_fab_toggle [data-testid="stButton"],.st-key-chat_fab_toggle [data-testid="stTooltipHoverTarget"] { width:100% !important; height:100% !important; }
.st-key-chat_fab_toggle button { position:relative !important; display:grid !important; place-items:center !important; width:64px !important; min-width:64px !important; height:64px !important; min-height:64px !important; max-height:64px !important; padding:0 !important; overflow:hidden !important; border:1px solid rgba(255,255,255,.34) !important; border-radius:50% !important; background:linear-gradient(145deg,#f2d99e,#d4af37 72%,#b58b24) !important; color:transparent !important; font-size:0 !important; box-shadow:0 10px 28px rgba(0,0,0,.46),inset 0 1px 0 rgba(255,255,255,.5) !important; transition:transform .18s ease,box-shadow .18s ease,filter .18s ease !important; }
.st-key-chat_fab_toggle button:hover { color:transparent !important; filter:brightness(1.06) !important; transform:translateY(-2px) !important; box-shadow:0 14px 34px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.55) !important; }
.st-key-chat_fab_toggle button:focus-visible { outline:3px solid rgba(230,194,128,.85) !important; outline-offset:3px !important; }
.st-key-chat_fab_toggle button > div { position:absolute !important; width:1px !important; height:1px !important; margin:-1px !important; overflow:hidden !important; clip-path:inset(50%) !important; white-space:nowrap !important; }
.st-key-chat_fab_toggle button::before { content:""; display:block; width:31px; height:31px; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cg fill='none' stroke='%23181713' stroke-linecap='round' stroke-linejoin='round' stroke-width='2.5'%3E%3Cpath d='M17 15c-3-3 2-4 0-7m8 7c-3-3 2-4 0-7m8 7c-3-3 2-4 0-7'/%3E%3Cpath d='M9 19h25v13a7 7 0 0 1-7 7h-11a7 7 0 0 1-7-7V19Z' fill='%23f7e7bf'/%3E%3Cpath d='M34 22h3a5 5 0 0 1 0 10h-3M7 42h34'/%3E%3Cpath d='M13 24h17' stroke='%23b58b24'/%3E%3C/g%3E%3C/svg%3E"); background-size:contain; background-repeat:no-repeat; background-position:center; }
[data-testid="stDialog"] > div,[role="dialog"] { background:rgba(18,18,18,.98) !important; border:1px solid rgba(212,175,55,.28) !important; border-radius:22px !important; box-shadow:0 28px 60px rgba(0,0,0,.5) !important; }
[data-testid="stDialog"] { align-items:flex-end !important; justify-content:flex-end !important; padding:24px 24px 100px !important; }
[data-testid="stDialog"] > div { width:min(420px,calc(100vw - 32px)) !important; max-width:calc(100vw - 32px) !important; max-height:calc(100dvh - 136px) !important; margin:0 !important; overflow:hidden !important; }
[data-testid="stDialog"] section[role="dialog"] { position:fixed !important; inset:auto 24px calc(18px + 64px + 12px + env(safe-area-inset-bottom)) auto !important; width:min(420px,calc(100vw - 32px)) !important; max-width:calc(100vw - 32px) !important; max-height:calc(100dvh - 112px - env(safe-area-inset-bottom)) !important; margin:0 !important; overflow-y:auto !important; }
[data-testid="stDialog"] [data-testid="stChatInput"] { border:1px solid rgba(230,194,128,.25) !important; border-radius:14px !important; background:#191919 !important; }
[data-testid="stDialog"] [data-testid="stChatInput"] > div { background-color:#191919 !important; }
[data-testid="stDialog"] [data-testid="stChatInputTextArea"] { background-color:#191919 !important; color:#F5F5F5 !important; -webkit-text-fill-color:#F5F5F5 !important; caret-color:#E6C280 !important; }
[data-testid="stDialog"] [data-testid="stChatInputTextArea"]::placeholder { color:#B8B8B8 !important; -webkit-text-fill-color:#B8B8B8 !important; opacity:1 !important; }
.k-chat-header { padding-bottom:.55rem; border-bottom:1px solid rgba(255,255,255,.1); }
.k-chat-header p { margin:0; color:var(--muted); font-size:.82rem; }
.st-key-chat_close_button button { border-color:rgba(255,255,255,.16) !important; }
.k-chat-message { display:block; border-radius:14px; padding:.7rem .9rem; margin:.5rem 0; max-width:88%; line-height:1.5; white-space:pre-wrap; overflow-wrap:anywhere; opacity:1 !important; filter:none !important; text-shadow:none !important; }
.k-chat-message.user { margin-left:auto; background:#3b2d12 !important; border:1px solid #8a6b2c !important; color:#fff8e8 !important; }
.k-chat-message.assistant { margin-right:auto; background:#24272b !important; border:1px solid #50565d !important; color:#f4f5f7 !important; }
.k-chat-message.user *, .k-chat-message.user *:visited { color:#fff8e8 !important; opacity:1 !important; text-shadow:none !important; }
.k-chat-message.assistant *, .k-chat-message.assistant *:visited { color:#f4f5f7 !important; opacity:1 !important; text-shadow:none !important; }
.k-chat-message.user strong, .k-chat-message.assistant strong { display:block !important; margin-bottom:.25rem !important; color:#f2d58a !important; }
@media(max-width:768px) { [data-testid="stMainBlockContainer"]{padding:1rem .75rem calc(2rem + 72px + env(safe-area-inset-bottom))}.hero{padding:1.4rem;border-radius:18px}.hero h1{font-size:2.65rem}.menu-card{min-height:unset;margin-bottom:.25rem}.navhint{font-size:.75rem}.chat-msg{max-width:96%}.st-key-chat_fab_toggle{width:58px !important;height:58px !important;right:16px !important;bottom:calc(16px + env(safe-area-inset-bottom)) !important}.st-key-chat_fab_toggle button{width:58px !important;min-width:58px !important;height:58px !important;min-height:58px !important;max-height:58px !important}[data-testid="stDialog"]{padding:12px 12px calc(86px + env(safe-area-inset-bottom)) !important}[data-testid="stDialog"] > div{width:calc(100vw - 24px) !important;max-width:calc(100vw - 24px) !important;max-height:calc(100dvh - 116px - env(safe-area-inset-bottom)) !important}[data-testid="stDialog"] section[role="dialog"]{right:16px !important;bottom:calc(16px + 58px + 10px + env(safe-area-inset-bottom)) !important;width:calc(100vw - 32px) !important;max-width:calc(100vw - 32px) !important;max-height:calc(100dvh - 144px - env(safe-area-inset-bottom)) !important} }
@media(max-width:420px) { .topbar{align-items:flex-start;flex-direction:column}.hero h1{font-size:2.25rem}.st-key-chat_fab_toggle{width:56px !important;height:56px !important;right:14px !important;bottom:calc(14px + env(safe-area-inset-bottom)) !important}.st-key-chat_fab_toggle button{width:56px !important;min-width:56px !important;height:56px !important;min-height:56px !important;max-height:56px !important}[data-testid="stDialog"]{padding-left:8px !important;padding-right:8px !important}[data-testid="stDialog"] > div{width:calc(100vw - 16px) !important;max-width:calc(100vw - 16px) !important}[data-testid="stDialog"] section[role="dialog"]{right:8px !important;bottom:calc(14px + 56px + 10px + env(safe-area-inset-bottom)) !important;width:calc(100vw - 16px) !important;max-width:calc(100vw - 16px) !important} }
@media(max-width:600px) { .st-key-main_navigation { padding:.35rem .5rem .1rem; margin:-.35rem -.5rem .65rem; } .st-key-main_navigation [data-testid="stHorizontalBlock"] { gap:.3rem; } .st-key-main_navigation .stButton > button { min-height:2rem; padding:.25rem .35rem; font-size:.78rem; } .st-key-main_navigation .brandmark { font-size:1rem; } }
</style>
"""


# Session State

def init_state() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "text": "Assalam-o-alaikum! I’m your K-Town Barista. Ask me about the menu, prices, recommendations, or your cart."}]
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    if "main_nav" not in st.session_state:
        st.session_state.main_nav = "Home"
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False


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


def normalize_text(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def match_item(query: str) -> dict[str, Any] | None:
    normalized = normalize_text(query)
    if not normalized:
        return None
    exact_matches = []
    for item in ITEMS.values():
        name = normalize_text(item["name"])
        item_id = normalize_text(item["id"])
        if name in normalized or item_id in normalized:
            exact_matches.append(item)
    if len(exact_matches) == 1:
        return exact_matches[0]
    if exact_matches:
        return None

    ignored_terms = {"a", "an", "and", "at", "cost", "for", "how", "i", "is", "me", "much", "of", "price", "the", "to", "what", "whats"}
    query_terms = {term for term in normalized.split() if term not in ignored_terms}
    if not query_terms:
        return None
    scores = []
    for item in ITEMS.values():
        item_terms = set(normalize_text(f"{item['name']} {item['id']}").split())
        score = len(query_terms & item_terms)
        if score:
            scores.append((score, item))
    if not scores:
        return None
    highest = max(score for score, _item in scores)
    winners = [item for score, item in scores if score == highest]
    return winners[0] if len(winners) == 1 else None


# AI Barista Engine
INTENT_TERMS: dict[str, tuple[str, ...]] = {
    "greeting": ("hello", "hi", "hey", "salam", "assalam", "aoa", "good morning", "good evening"),
    "menu": ("menu", "what do you have", "options", "available", "kya hai"),
    "price": ("price", "cost", "how much", "kitne", "qeemat", "rate", "rupees", "rs", "pkr"),
    "timing": ("time", "timing", "hours", "open", "close", "when", "kab"),
    "location": ("where", "location", "address", "karachi", "dha", "clifton", "kidhar", "kahan"),
    "recommendation": ("recommend", "suggest", "best", "what should", "mood", "pasand"),
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


def format_menu_summary() -> str:
    summaries = []
    for category, items in MENU.items():
        item_summary = ", ".join(f"{item['name']} ({money(item['price'])})" for item in items)
        summaries.append(f"{category}: {item_summary}")
    return " | ".join(summaries)


def format_cart_summary() -> str:
    if not st.session_state.cart:
        return "Your cart is currently empty."
    lines = [
        f"{ITEMS[item_id]['name']} x{qty} ({money(ITEMS[item_id]['price'] * int(qty))})"
        for item_id, qty in st.session_state.cart.items()
        if item_id in ITEMS and int(qty) > 0
    ]
    subtotal, tax, total = cart_totals()
    return f"{'; '.join(lines)}. Subtotal: {money(subtotal)}; tax: {money(tax)}; total: {money(total)}."


def parse_cart_action(normalized: str) -> str | None:
    if "clear my cart" in normalized or "empty cart" in normalized or "clear cart" in normalized:
        st.session_state.cart.clear()
        return "Your cart is now clear and ready for a fresh order."

    if "remove " in normalized or "delete " in normalized:
        remainder = normalized.split("remove ", 1)[-1].split("delete ", 1)[-1]
        if "to cart" in remainder:
            remainder = remainder.replace("to cart", "")
        item = match_item(remainder)
        if not item:
            return "I couldn’t match that item in the menu. Try a menu name like espresso, cold brew, or lava cake."
        current_qty = int(st.session_state.cart.get(item["id"], 0))
        if current_qty <= 0:
            return f"{item['name']} is not currently in your cart."
        change_quantity(item["id"], -current_qty)
        return f"Removed {item['name']} from your cart."

    if "add " in normalized or "include " in normalized or "put " in normalized:
        maybe_quantity = re.search(r"\b(\d+)\b", normalized)
        quantity = int(maybe_quantity.group(1)) if maybe_quantity and ("add " in normalized or "include " in normalized or "put " in normalized) else 1
        text = normalized
        for phrase in ("add ", "include ", "put "):
            if phrase in text:
                text = text.split(phrase, 1)[1]
        if " to cart" in text:
            text = text.replace(" to cart", "")
        if " in cart" in text:
            text = text.replace(" in cart", "")
        if " my cart" in text:
            text = text.replace(" my cart", "")
        if " the " in text:
            text = text.replace(" the ", " ")
        item = match_item(text)
        if not item:
            return "I couldn’t match that item in the menu. Try names like espresso, vanilla latte, or lava cake."
        for _ in range(quantity):
            add_to_cart(item["id"])
        if quantity > 1:
            return f"Added {quantity} {item['name']} to your cart."
        return f"Added {item['name']} to your cart."

    return None


def recommend_item(query: str) -> str:
    normalized = normalize_text(query)
    def describe(item: dict[str, Any]) -> str:
        return f"{item['name']} ({money(item['price'])}): {item['description']}"

    if "sweet" in normalized:
        item = ITEMS["lava-cake"]
        return f"For a sweet option, consider {describe(item)}"
    if "strong" in normalized or "espresso" in normalized or "cortado" in normalized:
        options = [ITEMS["espresso"], ITEMS["cortado"]]
        return "Coffee options from the menu: " + " ".join(describe(item) for item in options)
    if "cold" in normalized or "iced" in normalized:
        return "Cold coffee options from the menu: " + " ".join(describe(item) for item in MENU["Cold Coffee"])
    if "for two" in normalized or "two people" in normalized or ("two" in normalized and "people" in normalized):
        return "For two people, you could consider: " + " ".join(describe(item) for item in (ITEMS["cold-brew"], ITEMS["lava-cake"]))
    if "coffee" in normalized:
        return "Coffee options from the menu: " + " ".join(describe(item) for item in MENU["Hot Brews"])
    return "I can recommend from these menu items: " + ", ".join(item["name"] for item in ITEMS.values())


def barista_reply(message: str) -> str:
    if not message or not message.strip():
        return "Ask me about the menu, prices, recommendations, your cart, or the current tax."

    normalized = normalize_text(message)
    action_reply = parse_cart_action(normalized)
    if action_reply:
        return action_reply

    intent, _confidence = detect_intent(message)
    if intent == "greeting":
        return "Wa-alaikum-assalam! Good to have you here. Looking for a coffee, a sweet bite, or a little of both?"
    if ("cart" in normalized and "what" in normalized and "in" in normalized) or "show my cart" in normalized or "cart items" in normalized:
        return format_cart_summary()
    if "how many items are in my cart" in normalized or "items in my cart" in normalized:
        quantity = sum(int(qty) for qty in st.session_state.cart.values())
        return f"You have {quantity} item(s) in your cart." if quantity else "Your cart is empty right now."
    if ("total" in normalized and ("cart" in normalized or "order" in normalized or "my" in normalized)) or "subtotal" in normalized:
        subtotal, tax, total = cart_totals()
        return f"Your subtotal is {money(subtotal)}, tax is {money(tax)}, and your total is {money(total)}."
    if "tax" in normalized:
        _, tax, _ = cart_totals()
        return f"Tax is {money(tax)} at {TAX_RATE:.0%} of your current subtotal."
    if "menu" in normalized and "what" in normalized:
        return format_menu_summary()
    if "what cold coffee" in normalized or ("cold coffee" in normalized and "have" in normalized):
        category_items = ", ".join(f"{item['name']} ({money(item['price'])})" for item in MENU["Cold Coffee"])
        return f"Our cold coffee options are: {category_items}."
    if "what are the gourmet bites" in normalized or "gourmet bites" in normalized:
        category_items = ", ".join(f"{item['name']} ({money(item['price'])})" for item in MENU["Gourmet Bites"])
        return f"The gourmet bites are: {category_items}."
    if "what coffee do you recommend" in normalized or "recommend" in normalized or "what should i get" in normalized:
        return recommend_item(normalized)
    if "sweet" in normalized:
        return recommend_item(normalized)
    if "strong" in normalized:
        return recommend_item(normalized)
    if "cheapest" in normalized:
        item = min(ITEMS.values(), key=lambda entry: entry["price"])
        return f"The cheapest item is {item['name']} at {money(item['price'])}."
    if "most expensive" in normalized or "expensive item" in normalized:
        item = max(ITEMS.values(), key=lambda entry: entry["price"])
        return f"The most expensive item is {item['name']} at {money(item['price'])}."
    if "under" in normalized:
        match = re.search(r"under\s*(?:(?:rs\.?|rupees|pkr|₹)\s*)?(\d[\d,]*)", message, re.IGNORECASE)
        if match:
            target = int(match.group(1).replace(",", ""))
            affordable = [item for item in ITEMS.values() if item["price"] < target]
            if affordable:
                items = ", ".join(f"{item['name']} ({money(item['price'])})" for item in affordable)
                return f"Under {money(target)}, I’d suggest: {items}."
            return f"Nothing in the menu is under {money(target)} right now."
    if "price" in normalized or "how much" in normalized or "cost" in normalized:
        for category in MENU:
            if normalize_text(category) in normalized:
                category_prices = ", ".join(f"{item['name']} ({money(item['price'])})" for item in MENU[category])
                return f"{category} prices: {category_prices}."
        item = match_item(normalized)
        if item:
            return f"{item['name']} is {money(item['price'])}."
        prices = [item["price"] for item in ITEMS.values()]
        return f"Menu prices range from {money(min(prices))} to {money(max(prices))}. Ask me about an item by name for its price."
    item = match_item(normalized)
    if item and any(phrase in normalized for phrase in ("what is", "tell me about", "describe")):
        return f"{item['name']} ({money(item['price'])}): {item['description']}"
    if "what is on the menu" in normalized or "menu" in normalized:
        return format_menu_summary()
    if "hours" in normalized or "open" in normalized or "timing" in normalized:
        return "The app doesn't currently have verified opening hours."
    if "location" in normalized or "where" in normalized or "address" in normalized:
        return "The app doesn't provide a verified cafe address or location."
    if "recommend" in normalized or "suggest" in normalized:
        return recommend_item(message)
    if ("what are the" in normalized and "bites" in normalized) or "gourmet" in normalized:
        return format_menu_summary()
    if "tax" in normalized:
        _, tax, _ = cart_totals()
        return f"Current tax is {money(tax)}."
    if intent == "timing":
        return "The app doesn't currently have verified opening hours."
    if intent == "location":
        return "The app doesn't provide a verified cafe address or location."
    if intent == "recommendation":
        return recommend_item(message)
    return "I can help with the menu, specific prices, recommendations, cart totals, and Karachi sample locations. Ask me something like: 'What cold coffee do you have?' or 'Add a latte to my cart.'"


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
  const crumbCanvas=document.createElement('canvas');crumbCanvas.width=512;crumbCanvas.height=256;const ctx=crumbCanvas.getContext('2d');ctx.fillStyle='#4b2819';ctx.fillRect(0,0,512,256);let seed=28;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
  for(let i=0;i<18000;i++){const x=rand()*512,y=rand()*256,r=.35+rand()*2.1;ctx.fillStyle=rand()>.53?'rgba(213,150,91,.13)':'rgba(20,9,5,.12)';ctx.beginPath();ctx.ellipse(x,y,r,r*(.35+rand()),0,0,Math.PI*2);ctx.fill()}
  const crumbMap=new THREE.CanvasTexture(crumbCanvas);crumbMap.wrapS=crumbMap.wrapT=THREE.RepeatWrapping;crumbMap.repeat.set(2,1);crumbMap.anisotropy=8;
  const baked=new THREE.MeshStandardMaterial({color:0x8b5637,map:crumbMap,roughness:.93});
  const cakeSide=new THREE.MeshStandardMaterial({color:0x70412b,map:crumbMap,bumpMap:crumbMap,bumpScale:.075,roughness:.91});
  const ganache=new THREE.MeshPhysicalMaterial({color:0x32140d,roughness:.14,metalness:.02,clearcoat:.6,clearcoatRoughness:.12});
 const plateMat=new THREE.MeshStandardMaterial({color:0xe8e0d0,roughness:.28,metalness:.08});
 const gold=new THREE.MeshStandardMaterial({color:0xD4AF37,metalness:.48,roughness:.26});
 const plate=new THREE.Mesh(new THREE.CylinderGeometry(1.4,1.33,.11,64),plateMat);plate.position.y=-.22;cake.add(plate);
 const plateLine=new THREE.Mesh(new THREE.TorusGeometry(1.25,.018,8,64),gold);plateLine.rotation.x=Math.PI/2;plateLine.position.y=-.16;cake.add(plateLine);
 const base=new THREE.Mesh(new THREE.CylinderGeometry(.82,.9,.12,64),baked);base.position.y=-.105;cake.add(base);
 const body=new THREE.Mesh(new THREE.CylinderGeometry(.79,.89,1.02,64,1,false),cakeSide);body.position.y=.46;cake.add(body);
  const top=new THREE.Mesh(new THREE.CylinderGeometry(.79,.79,.12,64),baked);top.position.y=1.03;cake.add(top);
  const chocolateTop=new THREE.Mesh(new THREE.CylinderGeometry(.80,.80,.055,64),ganache);chocolateTop.position.y=1.105;cake.add(chocolateTop);
  const molten=new THREE.Mesh(new THREE.SphereGeometry(.28,40,28),ganache);molten.scale.set(1,.3,1);molten.position.set(-.14,1.15,.05);cake.add(molten);
  const flow=new THREE.Mesh(new THREE.TorusGeometry(.25,.035,14,48),ganache);flow.rotation.x=Math.PI/2;flow.position.set(-.14,1.15,.05);cake.add(flow);
  for(let i=0;i<11;i++){const a=i*Math.PI*2/11+.12;const len=[.13,.27,.19,.36,.16,.3,.12,.24,.34,.15,.26][i];const drop=new THREE.Mesh(new THREE.SphereGeometry(1,24,18),ganache);drop.scale.set(.055+(i%3)*.012,len,.055+(i%3)*.012);drop.position.set(Math.cos(a)*.775,1.03-len*.55,Math.sin(a)*.775);cake.add(drop)}
  const berryMat=new THREE.MeshPhysicalMaterial({color:0xa10e24,roughness:.3,clearcoat:.45});
  for(let i=0;i<3;i++){const a=2.15+i*.48;const berry=new THREE.Mesh(new THREE.SphereGeometry(.13,24,20),berryMat);berry.scale.set(.82,1.08,.82);berry.position.set(Math.cos(a)*.37,1.22,Math.sin(a)*.37);cake.add(berry);for(let j=0;j<7;j++){const b=j*2.4;const seedDot=new THREE.Mesh(new THREE.SphereGeometry(.009,6,5),new THREE.MeshStandardMaterial({color:0xf5d58c,roughness:.65}));seedDot.position.set(berry.position.x+Math.cos(b)*.09,berry.position.y+(j%3-.8)*.045,berry.position.z+Math.sin(b)*.09);cake.add(seedDot)}}
  const mint=new THREE.MeshStandardMaterial({color:0x315b32,roughness:.72,side:THREE.DoubleSide});
  for(let i=0;i<3;i++){const leaf=new THREE.Mesh(new THREE.SphereGeometry(1,16,10),mint);leaf.scale.set(.2,.025,.085);leaf.position.set(-.37+i*.09,1.29,.12+i*.055);leaf.rotation.y=-.5+i*.55;cake.add(leaf)}
  const crumbs=new THREE.MeshStandardMaterial({color:0x9a6540,roughness:.92});
  for(let i=0;i<24;i++){const a=i*2.399;const r=.55+(i%5)*.055;const crumb=new THREE.Mesh(new THREE.SphereGeometry(.014+(i%3)*.005,8,6),crumbs);crumb.position.set(Math.cos(a)*r,1.142,Math.sin(a)*r);cake.add(crumb)}
 cake.rotation.z=-.045;
 const clock=new THREE.Clock();function animate(){requestAnimationFrame(animate);const t=clock.getElapsedTime();cake.rotation.y=Math.sin(t*.22)*.24;cake.position.y=Math.sin(t*.8)*.035;renderer.render(scene,camera)}animate();
 addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
} catch(e) { document.getElementById('fallback').style.display='grid'; }
</script></body></html>""", height=330, scrolling=False)


# Header / Navigation

def go_to_menu() -> None:
    st.session_state.main_nav = "Menu"


def render_header() -> None:
    with st.container(key="main_navigation"):
        brand_col, home_col, menu_col, cart_col = st.columns([2.7, 1.0, 1.0, 1.25], vertical_alignment="center", gap="small")
        with brand_col:
            st.markdown('<div class="brandmark">K-TOWN <span>ROAST</span></div>', unsafe_allow_html=True)
        with home_col:
            if st.button("Home", key="nav_home", use_container_width=True):
                st.session_state.main_nav = "Home"
        with menu_col:
            if st.button("Menu", key="nav_menu", use_container_width=True):
                st.session_state.main_nav = "Menu"
        with cart_col:
            cart_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0
            cart_label = f"Cart ({cart_count})" if cart_count else "Cart"
            if st.button(cart_label, key="nav_cart", use_container_width=True):
                st.session_state.main_nav = "Cart"
        st.caption("Karachi, Pakistan · Coffee, considered.")


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


# Chatbot Panel

def handle_chat_prompt(prompt: str) -> None:
    cleaned = (prompt or "").strip()
    if not cleaned:
        return
    st.session_state.chat_history.append({"role": "user", "text": cleaned})
    reply = barista_reply(cleaned)
    st.session_state.chat_history.append({"role": "assistant", "text": reply})


def dismiss_chat() -> None:
    st.session_state.chat_open = False


@st.dialog("K-Barista", on_dismiss=dismiss_chat)
def chat_dialog() -> None:
    st.markdown('<div class="k-chat-header"><p>Newest messages appear first</p></div>', unsafe_allow_html=True)
    with st.container(height=340, border=False, key="chat_history_container"):
        for message in reversed(st.session_state.chat_history[-8:]):
            role = message.get("role", "assistant")
            label = "You" if role == "user" else "K-Barista"
            bubble_class = "k-chat-message user" if role == "user" else "k-chat-message assistant"
            st.markdown(f'<div class="{bubble_class}"><strong>{html.escape(label)}</strong>{html.escape(str(message.get("text", "")))}</div>', unsafe_allow_html=True)
    prompt = st.chat_input("Ask K-Barista")
    if prompt:
        handle_chat_prompt(prompt)
        st.rerun()
    if st.button("Close chat", key="close_chat_button"):
        st.session_state.chat_open = False
        st.rerun()


def render_chat_fab() -> None:
    if st.button("Open K-Barista chat", key="chat_fab_toggle", help="Open K-Barista chat", use_container_width=False):
        st.session_state.chat_open = not st.session_state.chat_open
    if st.session_state.chat_open:
        chat_dialog()


# Social-proof / Brand Section

def render_brand() -> None:
    st.markdown('<div class="section-head"><div class="eyebrow">Crafted in Karachi</div></div>', unsafe_allow_html=True)
    feature_cols = st.columns(3)
    feature_cards = [
        {
            "title": "Coffee ritual",
            "image": get_asset_url("coffee.jpg", "https://images.unsplash.com/photo-1497636577773-f1231844b336?auto=format&fit=crop&w=900&q=80"),
            "caption": "Premium espresso, crema, and slow mornings.",
        },
        {
            "title": "The room",
            "image": get_asset_url("cafe-interior.jpg", "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=900&q=80"),
            "caption": "Warm wood, low light, and a welcoming table.",
        },
        {
            "title": "Kitchen favourites",
            "image": get_asset_url("lava-cake.jpg", "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=900&q=80"),
            "caption": "Belgian chocolate, rich and indulgent.",
        },
    ]
    for col, card in zip(feature_cols, feature_cards):
        with col:
            st.image(card["image"], use_container_width=True, caption=card["caption"])
            st.markdown(f'<div class="brand-panel"><strong>{card["title"]}</strong><p>{card["caption"]}</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    _, menu_cta, _ = st.columns([1, 1.5, 1])
    with menu_cta:
        if st.button("Explore the menu", key="home_explore_menu", use_container_width=True):
            st.session_state.main_nav = "Menu"
            st.rerun()


# Footer

def render_footer() -> None:
    st.markdown('<div class="footer"><b>K-Town Roast</b><br>Brewed for Karachi. Crafted for the Moment.<br><br>Phase 6 DHA · E-Street Clifton · Karachi<br><small>Sample locations shown as application content; business addresses are not verified.<br>© 2026 K-Town Roast</small></div>', unsafe_allow_html=True)


# Main Application

def main() -> None:
    init_state()
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    render_header()
    render_hero()
    if st.session_state.main_nav == "Home":
        render_brand()
    elif st.session_state.main_nav == "Menu":
        render_menu()
    else:
        render_cart()
    render_footer()
    render_chat_fab()


if __name__ == "__main__":
    main()
