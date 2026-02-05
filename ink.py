# Auto-loads the already-present image from /images
# Forces the image to display vertically (portrait) via rotation
# Put the image in: images/personal touch_illustration_project.jpg

import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Little Chefs & The Strudel",
    layout="wide",
    initial_sidebar_state="collapsed",  # hide by default
)

# ---------------- Paths ----------------
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_IMAGE_NAME = "personal touch_illustration_project.jpg"
DEFAULT_IMAGE_PATH = IMAGE_DIR / DEFAULT_IMAGE_NAME


def _norm(s: str) -> str:
    return s.lower().replace(" ", "").replace("_", "").replace("-", "")


def find_default_image() -> Path | None:
    """Finds the project image in images/ without any upload step, tolerating spaces/underscores/case."""
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    candidates = [p for p in IMAGE_DIR.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if not candidates:
        return None

    expected = _norm("personal touch_illustration_project")
    for p in candidates:
        if _norm(p.stem) == expected:
            return p

    # 2) contains match
    for p in candidates:
        if expected in _norm(p.stem):
            return p

    # 3) fallback: first file
    return sorted(candidates)[0]


def load_portrait_image(path: Path) -> Image.Image:
    """
    Loads image and ensures a portrait (vertical) presentation.
    - Applies EXIF transpose (fixes phone rotation metadata).
    - If still landscape, rotates 90° to portrait.
    """
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)  # respect EXIF orientation
    w, h = img.size
    if w > h:
        img = img.rotate(90, expand=True)
    return img


# Determine which image to show (no sidebar / no uploads)
discovered_default = find_default_image()
active_image = discovered_default if discovered_default else DEFAULT_IMAGE_PATH

# ---------------- Modern dark styling (with subtle gradients) ----------------
st.markdown(
    """
<style>
  /* Remove sidebar completely (space + toggle + contents) */
  [data-testid="stSidebar"],
  [data-testid="stSidebarNav"],
  [data-testid="collapsedControl"] {
    display: none !important;
  }
  section[data-testid="stSidebar"] { width: 0 !important; }
  section[data-testid="stSidebar"] * { display: none !important; }

  /* App background: deep modern gradient */
  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(1200px 700px at 12% 8%, rgba(124, 92, 255, 0.18), rgba(0,0,0,0) 55%),
      radial-gradient(900px 600px at 88% 14%, rgba(0, 200, 255, 0.14), rgba(0,0,0,0) 52%),
      radial-gradient(900px 700px at 55% 92%, rgba(255, 168, 88, 0.10), rgba(0,0,0,0) 58%),
      linear-gradient(180deg, #070A10 0%, #0B0F14 55%, #070A10 100%);
  }

  /* Layout */
  .block-container { max-width: 1400px; padding-top: 2.2rem; padding-bottom: 3rem; }
  h1, h2, h3 { letter-spacing: -0.02em; }

  /* Make the hero title larger + allow it to breathe */
  .hero h1 { font-size: 3.2rem; line-height: 1.05; margin-bottom: 0.6rem; }
  .hero p { font-size: 1.05rem; }

  /* Cards */
  .card {
    border: 1px solid rgba(255,255,255,0.10);
    background:
      radial-gradient(900px 240px at 15% 0%, rgba(124, 92, 255, 0.10), rgba(0,0,0,0) 60%),
      linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border-radius: 18px;
    padding: 1.1rem 1.1rem;
    box-shadow: 0 14px 40px rgba(0,0,0,.35);
    backdrop-filter: blur(8px);
  }

  .hero {
    border: 1px solid rgba(255,255,255,0.12);
    background:
      radial-gradient(1000px 420px at 18% 10%, rgba(0, 200, 255, 0.14), rgba(0,0,0,0) 55%),
      radial-gradient(900px 420px at 88% 0%, rgba(124, 92, 255, 0.14), rgba(0,0,0,0) 55%),
      linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border-radius: 22px;
    padding: 1.5rem 1.6rem;
    box-shadow: 0 18px 55px rgba(0,0,0,.35);
    backdrop-filter: blur(10px);
  }

  .muted { color: rgba(255,255,255,0.72); }

  .divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.12), rgba(255,255,255,0));
    margin: 1.25rem 0 1.1rem 0;
  }

  /* Chips */
  .chip {
    display: inline-block;
    padding: .25rem .65rem;
    margin: .15rem .25rem .15rem 0;
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 999px;
    background:
      radial-gradient(400px 120px at 20% 20%, rgba(124, 92, 255, 0.14), rgba(0,0,0,0) 55%),
      linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03));
    font-size: .9rem;
  }

  /* Buttons / inputs: gentle glow */
  .stButton button, .stDownloadButton button {
    border: 1px solid rgba(158, 203, 255, 0.28) !important;
    box-shadow: 0 0 0 1px rgba(158, 203, 255, 0.10), 0 10px 22px rgba(0,0,0,0.25);
  }

  /* Links */
  a { color: #9ecbff !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- Main content ----------------
title_col, action_col = st.columns([0.80, 0.20], vertical_alignment="center")

with title_col:
    st.markdown(
        """
<div class="hero">
  <h1>Little Chefs &amp; The Strudel</h1>
  <p class="muted">
    A warm, black-and-white storytelling illustration series: tiny determined chefs,
    dramatic kitchen moments, and one mission — bake the perfect strudel.
  </p>
  <div>
    <span class="chip">Visual storytelling</span>
    <span class="chip">Ink / markers</span>
    <span class="chip">Comic panels</span>
    <span class="chip">Character design</span>
    <span class="chip">Atmosphere &amp; humor</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

left, right = st.columns([0.58, 0.42], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("The storyline")
    st.markdown(
        """
**Meet the little chefs:** tiny **squirrels** in oversized chef hats, running a serious bakery operation.

Tonight’s goal: **strudel** — flaky layers, sweet filling, and the final proud plate moment.  
But the kitchen has its plot twists: ingredients vanish, a rolling pin becomes a challenge,
and the oven door feels like the final boss.

This is a story about **teamwork, curiosity, and small characters doing big things** — with
sound effects, expressive gestures, and cozy “oh no… / oh YES!” beats.
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Project quick view")
    st.write("**Mood:** cozy • playful • a bit chaotic")
    st.write("**Theme:** baking as an adventure")
    st.write("**Format:** panel-based narrative")
    st.write("**Setting:** cozy-night kitchen")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Illustration project")

    if Path(active_image).exists():
        try:
            portrait = load_portrait_image(Path(active_image))
            st.image(portrait, use_container_width=True, caption="Panel page: the strudel mission in motion.")
        except Exception as e:
            st.error(f"Could not open image: {e}")
            st.caption(f"Path: `{Path(active_image).as_posix()}`")
    else:
        st.warning(
            f"No image found at `{Path(active_image).as_posix()}`.\n\n"
            f"Place your file in:\n`{IMAGE_DIR.as_posix()}`\n\n"
            f"Tip: your default name should be:\n`{DEFAULT_IMAGE_NAME}`"
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Characters")
    st.markdown(
        """
- **Head Chef:** confident, dramatic, loves big gestures.  
- **Sous Chef:** precise, timing-obsessed, always checking the oven.  
- **Sneezey Helper:** flour everywhere, chaos energy, heart of gold.  
- **The Critic:** arrives at the end like “*is it done yet?*” and impatiently bites a piece  
- **The Coordinator:** warns “*wait for the cream*”
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Visual language")
    st.markdown(
        """
- **High contrast** black/white for clarity in small panels  
- **Handwritten SFX** (“crack”, “zack”, “nom nom”, “ah...ah...achoo”) for rhythm  
- **Close-ups** of tools & ingredients to build tension  
- **Quiet frames** (steam, shadows) to let moments breathe
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Process")
    st.markdown(
        """
1) Thumbnail storyboard  
2) Character expressions & poses  
3) Clean panel layout  
4) Ink + textures  
5) Lettering / sound effects  
6) Final page composition
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

with st.expander("Read the scene beats (mini storyboard)", expanded=True):
    st.markdown(
        """
- **Beat 1:** recipe appears — the mission is declared.  
- **Beat 2:** ingredients gathered — confidence rises.  
- **Beat 3:** *crack!* the egg breaks — panic flickers.  
- **Beat 4:** rolling + folding — the rhythm of baking.  
- **Beat 5:** oven opens — suspense, heat, steam.  
- **Beat 6:** tasting + plating — relief… and pride.  
- **Beat 7:** last crumbs — “yummy” closure.
"""
    )

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("About this project")
st.markdown(
    """
This illustration project explores how **little repeating characters** can carry a full narrative
through **expressions, pacing, and props**.

The goal is a “cozy kitchen feeling”, where the audience follows the action **panel by panel**
and smiles at the tiny drama of baking.
"""
)
st.markdown("</div>", unsafe_allow_html=True)

