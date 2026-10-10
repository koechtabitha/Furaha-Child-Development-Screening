"""Responsive Furaha visual styling."""

import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
        :root { --green:#276f32; --green-dark:#205d2a; --ink:#151b18; --muted:#626b64; --cream:#f5f6ef; --yellow:#f4d34b; --page-gutter:clamp(1rem,3.7vw,4.5rem); }
        .stApp { background:var(--cream); color:var(--ink); }
        .block-container { max-width:none!important; width:100%; padding:0 var(--page-gutter) 2.5rem!important; margin:0!important; border:0; border-radius:0; background:transparent; box-shadow:none; }
        header[data-testid="stHeader"], [data-testid="stToolbar"] { display:none; }
        html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
        h1,h2,h3,h4 { font-family:'Manrope',sans-serif!important; color:var(--ink); }
        h1 { font-size:clamp(2rem,3vw,2.8rem)!important; letter-spacing:-.04em; }
        h2 { font-size:1.45rem!important; letter-spacing:-.02em; }
        .furaha-topbar { display:flex; align-items:center; justify-content:space-between; padding:.85rem var(--page-gutter); margin:0 calc(-1 * var(--page-gutter)) 1rem; border-radius:0; color:white; background:#201d1a; border-bottom:4px solid var(--yellow); }
        .furaha-brand { display:flex; align-items:center; gap:.75rem; font-family:Manrope,sans-serif; font-size:1.2rem; font-weight:800; }
        .furaha-mark { display:grid; place-items:center; width:2.8rem; height:2.8rem; background:#e9f2df; border-radius:50%; overflow:hidden; }
        .furaha-mark svg { width:2.45rem; height:2.45rem; }
        .furaha-brand-copy { display:flex; flex-direction:column; line-height:1.12; }
        .furaha-brand-copy small { font:500 .76rem 'DM Sans',sans-serif; color:#e6e4df; margin-top:.15rem; }
        .furaha-step { color:#f2eddf; font-size:.9rem; font-weight:600; }
        .furaha-hero { padding:.5rem 0 .2rem; }
        .furaha-kicker { color:var(--green); font-size:.78rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
        .furaha-subtitle { color:var(--muted); font-size:1.05rem; max-width:58rem; }
        .furaha-card { padding:1.2rem 1.3rem; border:1px solid #e5e9e0; border-radius:14px; background:#fff; margin:.6rem 0 1rem; }
        .furaha-card h3 { margin:.55rem 0 .35rem; font-size:1.1rem!important; }
        .furaha-card p { margin:.2rem 0 .65rem; color:#454e44!important; line-height:1.55; }
        .furaha-privacy { background:#f2f7ed; border-color:#d8e8d0; }
        .furaha-help { background:#fffaf0; border-color:#f1df9c; }
        .furaha-card-icon { display:grid; place-items:center; width:2.5rem; height:2.5rem; border-radius:50%; background:#e1eedc; font-size:1.25rem; }
        .furaha-help .furaha-card-icon { background:#f6df93; font-weight:800; }
        [data-testid="stVerticalBlockBorderWrapper"] { border-color:#e0e3dc!important; border-radius:16px!important; background:#fff!important; }
        .furaha-illustration { width:min(100%,360px); margin:-.5rem auto -.9rem; }
        [class*="st-key-step_nav_"] { position:relative; display:flex; justify-content:center; }
        [class*="st-key-step_nav_"] button { position:relative; z-index:1; }
        [class*="st-key-step_nav_"]:not([class*="st-key-step_nav_4"])::after { content:""; position:absolute; z-index:0; top:1.15rem; left:50%; right:-50%; height:3px; background:#dfe2dd; }
        [class*="st-key-step_nav_"] button { width:2.35rem!important; min-width:2.35rem!important; height:2.35rem!important; min-height:2.35rem!important; padding:0!important; border-radius:50%!important; border:1px solid #d9dfd5!important; border-bottom:1px solid #d9dfd5!important; font-size:1rem!important; }
        [class*="st-key-step_nav_"] button[kind="primary"] { background:var(--green)!important; border-color:var(--green)!important; color:white!important; }
        [class*="st-key-step_nav_"] button[kind="secondary"] { background:#edf0eb!important; color:#30372f!important; }
        [class*="st-key-step_nav_"] + div [data-testid="stCaptionContainer"] { text-align:center; }
        .furaha-mobile-stepper { display:none; }
        .furaha-note { padding:1rem 1.1rem; background:#f1f7ec; border:1px solid #dbe9d4; border-radius:12px; color:#384436; font-size:.93rem; }
        [data-testid="stWidgetLabel"] p, label, .stApp label, [data-testid="stMarkdownContainer"] p { color:var(--ink)!important; }
        [role="radiogroup"] { gap:.45rem; }
        [role="radiogroup"] label { padding:.55rem .8rem; border:1px solid #dce4d8; border-radius:9px; background:#fff; color:#354132!important; font-weight:700; }
        [role="radiogroup"] label:has(input:checked) { border-color:var(--green); background:#edf5e9; color:var(--green-dark)!important; }
        div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input { min-height:46px!important; padding:.55rem .85rem!important; border:1px solid #d2d5d0!important; border-radius:10px!important; background:#fff!important; color:var(--ink)!important; box-shadow:none!important; }
        div[data-baseweb="select"]>div { min-height:46px!important; border:1px solid #d2d5d0!important; border-radius:10px!important; background:#fff!important; box-shadow:none!important; }
        [data-testid="stWidgetLabel"] { margin-bottom:.32rem; }
        .furaha-form-heading { display:flex; align-items:center; gap:.8rem; margin:.1rem 0 .15rem; }
        .furaha-form-heading h2 { margin:0; font-size:1.5rem!important; }
        .furaha-form-icon { display:grid; place-items:center; flex:0 0 3.1rem; width:3.1rem; height:3.1rem; border-radius:50%; color:#246a35; background:#e7f0e2; }
        .furaha-form-icon svg { width:1.6rem; height:1.6rem; }
        .furaha-location-heading { display:flex; align-items:center; gap:.6rem; margin:1.2rem 0 .55rem; font-size:1.1rem; font-weight:800; }
        .furaha-location-heading svg { width:1.35rem; height:1.35rem; color:var(--green); }
        .furaha-time { display:flex; align-items:center; justify-content:flex-end; gap:.4rem; width:100%; color:var(--muted); white-space:nowrap; }
        .furaha-time svg { width:1.15rem; height:1.15rem; }
        .furaha-results-kicker { margin-top:1.5rem; color:var(--green); font-size:.76rem; font-weight:800; letter-spacing:.1em; }
        .furaha-result-meta { height:100%; padding:.85rem 1rem; border:1px solid #e1e5dc; border-radius:12px; background:#fff; }
        .furaha-result-meta small { display:block; margin-bottom:.2rem; color:var(--muted); font-size:.75rem; text-transform:uppercase; letter-spacing:.06em; }
        .furaha-result-meta strong { display:block; color:var(--ink); font-size:1rem; }
        .furaha-result-status { margin:1rem 0 1.25rem; padding:1.1rem 1.3rem; border:1px solid #c9dfc4; border-left:6px solid var(--green); border-radius:13px; background:#eff6eb; }
        .furaha-result-status--monitor { border-color:#d8e3cf; border-left-color:#6c8d42; background:#f4f7ed; }
        .furaha-result-status__label { margin-bottom:.3rem; color:#426044; font-size:.72rem; font-weight:800; letter-spacing:.09em; }
        .furaha-result-status strong { display:block; color:#203c25; font-size:1.15rem; }
        .furaha-result-status p { margin:.35rem 0 0; color:#4d5c4d; }
        .furaha-result-urgent { margin:1rem 0; padding:1rem 1.2rem; border:1px solid #efcf84; border-left:6px solid #bf8113; border-radius:12px; background:#fff7e4; color:#563a13; line-height:1.55; }
        .furaha-result-disclaimer { margin-top:1.3rem; padding:1rem 1.2rem; border:1px solid #dce5d7; border-radius:12px; background:#f4f7f1; color:#4b574b; line-height:1.5; }
        .furaha-result-meta + div { min-width:0; }
        button[kind="primary"], button[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primary"] button { min-height:48px; padding:.7rem 1.25rem; border:0; border-bottom:4px solid var(--yellow); border-radius:9px; color:white!important; background:var(--green); font-family:Manrope,sans-serif; font-weight:800; }
        button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover { background:var(--green-dark); color:white; }
        [data-testid="stAlert"] { border-radius:10px; }
        .furaha-nav-hint { color:var(--muted); font-size:.9rem; padding-top:.4rem; }
        .furaha-footer { margin:2rem calc(-1 * var(--page-gutter)) 0; padding:1.4rem var(--page-gutter); color:#e9e9e2; text-align:center; border-radius:0; background:#201d1a; border-top:4px solid var(--yellow); }
        @media(max-width:700px) {
          .block-container { padding:0 .9rem 6.5rem!important; margin:0!important; width:100%; }
          .furaha-topbar { padding:.7rem .9rem; margin-bottom:.8rem; }
          .furaha-brand { font-size:1rem; }
          [role="radiogroup"] { display:flex; flex-wrap:wrap; }
          [role="radiogroup"] label { flex:1; min-width:calc(50% - .5rem); justify-content:center; font-size:.82rem; }
          .furaha-hero { padding:.5rem 0; }
          .st-key-stepper_desktop { display:none!important; }
          .furaha-mobile-stepper { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:0; margin:.45rem 0 1.1rem; }
          .furaha-mobile-step { position:relative; display:flex; min-width:0; flex-direction:column; align-items:center; gap:.35rem; color:#727a73; text-align:center; }
          .furaha-mobile-step:not(:last-child)::after { content:""; position:absolute; z-index:0; top:.86rem; left:calc(50% + .95rem); right:calc(-50% + .95rem); height:2px; background:#dfe3dc; }
          .furaha-mobile-step span { position:relative; z-index:1; display:grid; place-items:center; width:1.75rem; height:1.75rem; border:1px solid #d9dfd5; border-radius:50%; background:#edf0eb; color:#364038; font-size:.78rem; }
          .furaha-mobile-step.is-done span, .furaha-mobile-step.is-active span { border-color:var(--green); background:var(--green); color:#fff; }
          .furaha-mobile-step.is-active small { color:var(--green-dark); font-weight:800; }
          .furaha-mobile-step small { max-width:100%; font-size:.62rem; line-height:1.15; overflow-wrap:anywhere; }
          .furaha-results-kicker { margin-top:.8rem; }
          .furaha-result-meta { padding:.7rem; }
          .furaha-result-meta strong { font-size:.88rem; overflow-wrap:anywhere; }
          .furaha-time { justify-content:center; margin-top:.65rem; }
          .furaha-form-icon { flex-basis:2.7rem; width:2.7rem; height:2.7rem; }
          .furaha-footer { margin-right:-.9rem; margin-left:-.9rem; }
          .furaha-illustration { display:none; }
          [class*="st-key-continue_step"] { position:fixed!important; z-index:999; bottom:.3rem; left:.7rem; width:calc(100% - 1.4rem)!important; padding:.4rem; border:1px solid #e1e5dc; border-radius:12px; background:#fff; box-shadow:0 -4px 16px rgba(0,0,0,.09); }
          [class*="st-key-continue_step"] button { width:100%!important; }
          [class*="st-key-continue_step"] button, [data-testid="stBaseButton-primary"] button { color:#fff!important; }
          [class*="st-key-step_nav_"] button { width:2rem!important; min-width:2rem!important; height:2rem!important; min-height:2rem!important; }
          [class*="st-key-step_nav_"] + div [data-testid="stCaptionContainer"] { font-size:.68rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(step_index, title, subtitle, render_stepper=None, steps=()):
    st.markdown(
        '<div class="furaha-topbar"><div class="furaha-brand"><span class="furaha-mark"><svg viewBox="0 0 64 64" aria-hidden="true"><path fill="#f4bf35" d="M32 4c4 0 5 8 5 12 3-4 8-9 11-6s-2 10-5 13c5-1 13-1 13 4s-8 6-13 5c4 3 9 8 6 11s-10-2-13-6c1 5 1 13-4 13s-6-8-5-13c-3 4-8 9-11 6s2-10 6-13c-5 1-13 1-13-4s8-6 13-5c-4-3-9-8-6-11s10 2 13 6C31 11 28 4 32 4Z"/><circle cx="32" cy="32" r="8" fill="#6b431e"/><path d="M32 40v18M32 51c-8-7-14-5-15-1 5 7 10 8 15 5m0-4c8-7 14-5 15-1-5 7-10 8-15 5" fill="none" stroke="#39824a" stroke-width="4" stroke-linecap="round"/></svg></span><span class="furaha-brand-copy">Furaha<small>Child Development Screening</small></span></div><div class="furaha-step">Guided screening · About 5 minutes</div></div>',
        unsafe_allow_html=True,
    )
    if render_stepper is None:
        return
    hero, art = st.columns([2.2, 1], gap="small", vertical_alignment="center")
    with hero:
        st.markdown(
            f'<div class="furaha-hero"><div class="furaha-kicker">Step {step_index + 1} of 5 · Child development screening</div><h1>{title}</h1><div class="furaha-subtitle">{subtitle}</div></div>',
            unsafe_allow_html=True,
        )
        render_stepper(steps[step_index])
    with art:
        st.markdown(_CHILD_ILLUSTRATION, unsafe_allow_html=True)


_CHILD_ILLUSTRATION = """<svg class="furaha-illustration" viewBox="0 0 360 230" role="img" aria-label="A happy child with flowers" xmlns="http://www.w3.org/2000/svg">
<circle cx="180" cy="120" r="100" fill="#edf5e9"/><path d="M0 212 Q72 178 140 208 T280 204 T360 200 V230 H0Z" fill="#e1efdc"/>
<path d="M52 207 Q48 166 65 133 M307 207 Q310 160 294 126" fill="none" stroke="#347f2b" stroke-width="8" stroke-linecap="round"/><path d="M64 174 Q38 162 31 143 Q58 146 70 161 M297 172 Q323 159 329 139 Q304 143 292 159" fill="#5c9b49"/>
<circle cx="31" cy="126" r="11" fill="#f4d84a"/><circle cx="31" cy="126" r="5" fill="#e3a72c"/><circle cx="329" cy="122" r="12" fill="#f4d84a"/><circle cx="329" cy="122" r="5" fill="#e3a72c"/>
<path d="M130 139 Q180 112 230 139 L244 218 H116Z" fill="#f4d84a"/><path d="M139 111 Q107 92 94 68 M220 111 Q253 91 267 67" fill="none" stroke="#a75f3a" stroke-width="17" stroke-linecap="round"/><circle cx="91" cy="63" r="11" fill="#a75f3a"/><circle cx="270" cy="62" r="11" fill="#a75f3a"/>
<path d="M141 95 Q136 53 158 37 Q183 20 209 37 Q232 54 224 98 L215 123 Q180 143 146 122Z" fill="#7c3f25"/><circle cx="150" cy="54" r="16" fill="#35231c"/><circle cx="172" cy="34" r="17" fill="#35231c"/><circle cx="198" cy="35" r="17" fill="#35231c"/><circle cx="219" cy="57" r="16" fill="#35231c"/><ellipse cx="182" cy="91" rx="37" ry="42" fill="#a75f3a"/><circle cx="169" cy="88" r="3.5" fill="#211d19"/><circle cx="195" cy="88" r="3.5" fill="#211d19"/><path d="M170 105 Q182 119 196 104" fill="none" stroke="#542c20" stroke-width="4" stroke-linecap="round"/><path d="M164 151 Q182 166 199 151" fill="none" stroke="#347f2b" stroke-width="5" stroke-linecap="round"/>
<path d="M176 116 L181 128 L193 128 L184 136 L187 148 L176 141 L166 148 L169 136 L160 128 L172 128Z" fill="#f4d84a"/>
</svg>"""

