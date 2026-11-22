# ✨ Astraea — Celestial Intelligence Engine (v4.0.0)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/opticblu/hermes-astrology/actions/workflows/ci.yml/badge.svg)](https://github.com/opticblu/hermes-astrology/actions/workflows/ci.yml)
[![Ephemeris: NASA JPL / SwissEph](https://img.shields.io/badge/Ephemeris-JPL%20%7C%20SwissEph-purple.svg)](https://www.astro.com/swisseph/)

**Astraea — The Ultimate Deterministic Multi-Tradition Celestial Intelligence Engine & AI-Agent Backend**  
*Grounded in Classical Texts (Valens, Ptolemy, Lilly, Parashara, Ibn Ezra, Golden Dawn, BaZi) with Zero-Dependency Pure Python Core.*

---

## 📖 About Astraea

Named after **Astraea**, the classical goddess of innocence, celestial stars, and cosmic justice, **Astraea** is a comprehensive, deterministic, zero-dependency computational astrology engine and AI-agent knowledge framework. It unifies three major ancient civilizations' traditions (**Western/Hellenistic**, **Vedic/Jyotish**, and **Chinese BaZi**) alongside medieval mundane, financial astro-trading, and esoteric hermetic systems into a single high-performance library.

Unlike standard LLM chatbots that hallucinate planetary positions, Astraea computes mathematically verified orbital coordinates based on **NASA JPL DE421 / Swiss Ephemeris** models. Furthermore, it features an **Adaptive 3-Level Altitude Delivery System** (`references/fa/metaphors.md`) allowing AI agents to seamlessly deliver warm, human, everyday metaphors to beginners while providing rigorous degrees, virupas, and text citations to professional astrologers.

---

### 🌐 Supported Traditions

| Tradition | Calculation Framework | Core Methodological Focus |
|---|---|---|
| **♈ Western & Hellenistic** | Tropical / Valens, Ptolemy, Lilly | Psychological Archetypes, Time-Lords (ZR, Profections, Firdaria), Progressions, Astrodynes |
| **☪ Vedic / Jyotisha** | Sidereal (Chitrapaksha / Lahiri ~24°) | BPHS Shadbala (6/6), 3-Level Vimshottari Dasha, Jaimini Chara Dasha, Gochara with Ashtakavarga SAV |
| **🏛️ Mundane & Medieval** | National Ingresses / Abraham Ibn Ezra | Bonatti/Lilly Dynamic Validity Resolution, Carter Eclipse Triggers, Ibn Ezra 13 Marriage Lots |
| **木 Chinese BaZi** | Four Pillars of Destiny | Five Elements (Wu Xing), 10-Year Luck Pillars (Da Yun), Ten Gods (Shi Shen) |
| **🔮 Hermetic & Esoteric** | 36 Decans / Golden Dawn & Thoth | 36 Decans mapped to Minor Arcana & Ibn Ezra classical images, 22 Major Arcana on Tree of Life |

---

## 🌟 Key v4.0.0 Capabilities

### 1. Master Forecasting & Time-Lord Systems
* **Zodiacal Releasing (Valens Anthology IV):** Career & physical peak periods, Loosing of the Bond (LOB) pivot detection on a 360-day symbolic year.
* **Annual & Monthly Profections:** Dynamic house activation and Lord of the Year/Month assignment.
* **Medieval Firdaria:** 75-year diurnal/nocturnal planetary period cycles with 7 planetary sub-rulers per Ibn Ezra.
* **Secondary Progressions & Solar Arc:** Progressed chart dynamics, 8-phase progressed lunar cycle, and Solar Arc Directions (~1°/year).
* **3-Level Vimshottari Dasha:** Mahadasha, Antardasha, and Pratyantardasha (3rd level) integrated with Jaimini Chara Dasha.

### 2. Decision Intelligence & Domain Blueprints
* **Electional Date Finder (`find_best_time`):** Scans upcoming 30/60 days per Abraham Ibn Ezra's *Book of Elections* (Sefer ha-Mivharim); multi-factor scoring (0-100) for business, marriage, property, travel, and surgery.
* **Davison Time-Space Chart & Progression (`davison` & `davison_progression`):** Physical midpoint relationship chart with active relationship transits and secondary progressions.
* **Draconic Soul Synastry (`draconic` & `draconic_synastry`):** Nodal soul contracts shifting True North Node to 0° Aries.
* **Wealth & Career Blueprint (`wealth_blueprint`):** Multi-tradition synthesis of Western 2/10/11 houses, Part of Fortune/Commerce, Vedic D10 Dasamsa, Indu Lagna, and BaZi Wealth elements.
* **Love & Marriage Blueprint (`love_blueprint`):** 7th house analysis, Navamsa D9, Ibn Ezra 7 marriage lots, Upapada Lagna (UL), and BPHS Kuja Dosha cancellation engine.

### 3. Advanced Engines: Rectification, Crypto & Upayas
* **Automated Birth Time Rectification (`rectify_birth_time` / BTR):** Scans candidate birth minutes using Solar Arc Directions & Trutine of Hermes prenatal epoch symmetry mapped against biographical milestones.
* **Financial & Crypto Astrology (`crypto` / `financial`):** Tracks transits to verified Genesis charts of Bitcoin (2009), Ethereum (2015), S&P 500, and Gold with an objective Volatility Index.
* **Scientific Astrological Remediation (`remedies_blueprint`):** Functional Benefic gemstone prescription (BPHS rule: gemstones strictly prohibited for Dusthana lords), Karmic Daan (charity), and Liz Greene psychological grounding habits.
* **Tri-Tradition Consensus Engine (`tri_consensus`):** Intersects Western, Vedic, and BaZi vectors into a mathematical **Confidence Score (45% to 98%)**.
* **Daily Panchang & Choghadiya (`daily_panchang` / `choghadiya`):** 8-fold Day/Night Choghadiya cycles, Abhijit & Brahma Muhurta, Rahu Kalam, Yamaganda, Gulika Kalam.
* **Astrodynes Engine (`astrodynes`):** Church of Light quantitative Power (Astrodynes), Harmony (Harmodynes), and Discord (Discordynes) scoring.

---

## 🚀 Quick Start

### Installation & Cloning
```bash
git clone https://github.com/opticblu/hermes-astrology.git
cd hermes-astrology
```

For Swiss Ephemeris, install `pyswisseph==2.10.3.2` in the Python environment that launches the CLI, MCP or API. Otherwise the engine uses its built-in calculator. Check `_meta.engine_backend` in the result. Each Western and Vedic natal chart reports its zodiac and the house system actually used, including whole-sign fallback for polar locations.

When a birth time is unknown, omit the hour or set `time_known: false`. Provide the birthplace’s IANA timezone for the local civil date. On a Moon ingress day the reading returns both possible signs. Houses, the rising sign and the BaZi hour pillar require a known clock time.

### CLI Execution
```bash
# Compute comprehensive 3-tradition natal profile
python scripts/astro_engine.py --json '{"year":1995,"month":4,"day":15,"hour":14,"minute":30,"lat":35.6892,"lng":51.3890,"tz":"Asia/Tehran","systems":["western","vedic","bazi"]}'

# Find best 3 golden windows for business launch in next 30 days
python scripts/astro_engine.py --json '{"lat":35.6892,"lng":51.3890,"mode":"find_best_time","activity":"business_commerce","days_ahead":30}'

# Evaluate Bitcoin market astro-weather
python scripts/astro_engine.py --json '{"mode":"crypto","asset":"BTC"}'

# Run the full test suite
python -m unittest discover tests
```

### Birth details in shared deployments

Supply birth details with each chart request. For `POST /interact`, include `profile` on every call. The optional `session_id` correlates replies. MCP offers chart calculations on demand. Older versions saved named profiles in `~/.astro_profiles.json` or an `ASTRO_PROFILE_DIR` directory. This release leaves those files on disk for their owner to handle. Chat clients may retain their own message history.

### Historical price backtest

Keep the daily price file on local disk and set `ASTRO_MARKET_DATA_DIR` to its
directory. For BTC, download the [Coin Metrics daily BTC CSV](https://github.com/coinmetrics/data/blob/master/csv/btc.csv)
as `btc.csv`. The calculator reads the `time` and `PriceUSD` columns, skips
rows without a price and makes no network requests. Existing
`book/trading_sources/<ticker>_authentic_history.json` and
`<ticker>_daily_history.json` files remain supported.

```sh
ASTRO_MARKET_DATA_DIR=/path/to/prices python scripts/astro_cli.py --mode run_backtest --json '{"asset":"BTC","start_year":2020}'
```

Results are historical simulations. A signal uses the closing data for its
date, enters at the next available close and exits 14 bars after entry. Profit
factor is null when there are no losing trades.

### Python API Integration
```python
import sys
sys.path.insert(0, "scripts")
from astro_engine import calculate_full_profile

# Extract Wealth & Career Blueprint
result = calculate_full_profile({
    "year": 1990, "month": 6, "day": 15, "hour": 11, "minute": 0,
    "lat": 35.6892, "lng": 51.3890, "tz": "Asia/Tehran",
    "mode": "wealth_blueprint"
})

print(result["wealth_blueprint"]["synthesis_summary"])
```

---

## 📜 License
Published under the **MIT License**. Free for personal and commercial integration.  
Developed with ❤️ by **Erfan Ashouri (Erfix404)**.
