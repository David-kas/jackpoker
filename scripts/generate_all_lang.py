#!/usr/bin/env python3
"""Generate complete lang/en.json and lang/ru.json (unique copy, no template loops)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODIES = ROOT / "lang" / "bodies"
SLUGS = [
    "index",
    "about",
    "how-to-play",
    "bonus",
    "strategy",
    "mobile",
    "faq",
    "contacts",
]


def wc(html: str) -> int:
    t = re.sub(r"<[^>]+>", " ", html)
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def load_body(slug: str, lang: str) -> str:
    return (BODIES / f"{slug}.{lang}.html").read_text(encoding="utf-8").strip()


def faq_dict(pairs: list[tuple[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i, (q, a) in enumerate(pairs, start=1):
        out[f"q{i}"] = q
        out[f"a{i}"] = a
    return out


def build(lang: str) -> dict:
    if lang == "en":
        return build_en()
    if lang == "ru":
        return build_ru()
    raise ValueError(lang)


def build_en() -> dict:
    # yapf: disable
    return {
        "menu": {
            "index": "Home",
            "about": "Review",
            "how-to-play": "How to Play",
            "bonus": "Bonuses",
            "strategy": "Strategy",
            "mobile": "Mobile",
            "faq": "FAQ",
            "contacts": "Contacts",
        },
        "cta": ["Play Now", "Start Playing", "Claim Bonus", "Open Platform"],
        "responsible": "18+. Gambling involves risk. This website is informational only.",
        "disclaimer": "Independent guide—not an official JackPoker site. Partner terms can change; verify live rules before acting.",
        "meta": {
            "index": {
                "title": "JackPoker Guide: Independent Overview and Getting Started",
                "description": "Independent JackPoker guide: what this site covers, how to navigate sections, and realistic expectations.",
            },
            "about": {
                "title": "JackPoker Review: Interface, Features, and Limits",
                "description": "Editorial JackPoker review focused on usability, product surface area, and practical trade-offs.",
            },
            "how-to-play": {
                "title": "How to Play Poker: Rules, Hand Rankings, Table Flow",
                "description": "Beginner-friendly poker rules: rankings, betting rounds, table rhythm, and calm first sessions.",
            },
            "bonus": {
                "title": "JackPoker Bonuses: Reading Terms and Staying in Control",
                "description": "Bonus literacy: activation, wagering, restrictions, and when an offer is not worth the squeeze.",
            },
            "strategy": {
                "title": "Poker Strategy Basics: Position, Bankroll, and Leaks",
                "description": "Strategy essentials for distance play: position, sizing discipline, bankroll rules, and review habits.",
            },
            "mobile": {
                "title": "Mobile Poker: Focus, Connection, and Session Design",
                "description": "Mobile-first notes: ergonomics, fewer tables, connectivity risk, and safer pacing on phone.",
            },
            "faq": {
                "title": "Poker FAQ: 18 Practical Answers",
                "description": "Straight answers on onboarding, bonuses, variance, discipline, and checking partner-side rules.",
            },
            "contacts": {
                "title": "Contacts: Scope, Support Boundaries, Responsible Play",
                "description": "How to reach this editorial project, what we can and cannot help with, plus 18+ notices.",
            },
        },
        "pages": {s: page_en(s) for s in SLUGS},
    }
    # yapf: enable


def page_en(slug: str) -> dict:
    body = load_body(slug, "en")
    base = PAGES_EN_COMMON[slug]
    faq_pairs = FAQ_EN[slug]
    out = {
        **base,
        "body": body,
        "faq": faq_dict(faq_pairs),
    }
    w = wc(body)
    if w < 400:
        print(f"warning {slug}.en words={w}")
    return out


PAGES_EN_COMMON: dict[str, dict] = {
    "index": {
        "breadcrumbs": "Guide / Overview",
        "h1": "JackPoker Guide: Home",
        "lead": "Independent routes through rules, review, bonuses, strategy, mobile play, and FAQs—without hype.",
        "cards": {
            "c1t": "Start with structure",
            "c1d": "Pick one learning path and keep sessions short.",
            "c2t": "Verify partner rules",
            "c2d": "Bonuses and eligibility live on the partner side.",
            "c3t": "Measure decisions",
            "c3d": "Review spots—not just scores—to improve.",
        },
        "sections": {
            "s1": "What this project is",
            "s1d": "Editorial content, not operator support.",
            "s2": "Reading order",
            "s2d": "Rules before strategy; bonuses after baseline skill.",
            "s3": "Safety first",
            "s3d": "Limits, breaks, and stop rules beat impulse.",
            "s4": "Improvement loop",
            "s4d": "Notes after sessions beat vague intentions.",
            "s5": "Responsible play",
            "s5d": "Adults only; never chase losses.",
        },
    },
    "about": {
        "breadcrumbs": "Guide / Review",
        "h1": "JackPoker: Platform Review",
        "lead": "A usability-first look at what matters day to day: clarity, speed, and where friction shows up.",
        "cards": {
            "c1t": "Navigation",
            "c1d": "Can you find tables, filters, and settings quickly?",
            "c2t": "Trust cues",
            "c2d": "Clear limits and visible rules reduce surprises.",
            "c3t": "Honest limits",
            "c3d": "Every client has rough edges—name yours.",
        },
        "sections": {
            "s1": "Review stance",
            "s1d": "Practical observation, not marketing claims.",
            "s2": "Interface flow",
            "s2d": "Lobby to table: fewer taps, fewer mistakes.",
            "s3": "Features that matter",
            "s3d": "What changes decisions versus cosmetics.",
            "s4": "Trade-offs",
            "s4d": "Where convenience costs focus.",
            "s5": "Responsible framing",
            "s5d": "Keep stakes aligned with skill and budget.",
        },
    },
    "how-to-play": {
        "breadcrumbs": "Guide / How to Play",
        "h1": "JackPoker: How to Play Poker",
        "lead": "Compressed rules you can apply tonight—without drowning in jargon.",
        "cards": {
            "c1t": "Hand ranks",
            "c1d": "Know pairs, draws, and made hands cold.",
            "c2t": "Order of play",
            "c2d": "Blinds, streets, and who acts first matter.",
            "c3t": "Pot basics",
            "c3d": "Calls, raises, and fold equity in plain language.",
        },
        "sections": {
            "s1": "Beginner lens",
            "s1d": "Play fewer hands, smaller stakes, clearer plans.",
            "s2": "Hand strength",
            "s2d": "Absolute strength vs. board texture.",
            "s3": "Betting streets",
            "s3d": "Why aggression maps pressure.",
            "s4": "Table etiquette",
            "s4d": "Act in turn; protect your time bank.",
            "s5": "Risk control",
            "s5d": "Stop rules prevent emotional escalation.",
        },
    },
    "bonus": {
        "breadcrumbs": "Guide / Bonuses",
        "h1": "JackPoker: Bonuses",
        "lead": "Treat promos like contracts: read weighting, clocks, and game eligibility before you commit volume.",
        "cards": {
            "c1t": "Wagering math",
            "c1d": "Required rake or volume can erase EV.",
            "c2t": "Eligibility",
            "c2d": "Markets, deposit methods, and exclusions vary.",
            "c3t": "Strategic fit",
            "c3d": "If it forces bad games, skip it.",
        },
        "sections": {
            "s1": "Offer anatomy",
            "s1d": "Match, release, expiration, and caps.",
            "s2": "Hidden constraints",
            "s2d": "Withdrawal holds and partial clears.",
            "s3": "Volume planning",
            "s3d": "Realistic hours vs. forced grind.",
            "s4": "Bankroll link",
            "s4d": "Never increase stakes just to clear.",
            "s5": "Responsible use",
            "s5d": "Bonuses are optional—not recovery tools.",
        },
    },
    "strategy": {
        "breadcrumbs": "Guide / Strategy",
        "h1": "JackPoker: Strategy",
        "lead": "Foundations that survive variance: position, ranges, and honest post-session notes.",
        "cards": {
            "c1t": "Position",
            "c1d": "Late position earns information—use it.",
            "c2t": "Ranges",
            "c2d": "Open tight, defend selectively, adjust reads.",
            "c3t": "Bankroll",
            "c3d": "Buy-ins protect mental game first.",
        },
        "sections": {
            "s1": "Planning",
            "s1d": "Session goals tied to skills—not prizes.",
            "s2": "Preflop discipline",
            "s2d": "Fewer dominated hands, cleaner decisions.",
            "s3": "Postflop themes",
            "s3d": "Board-driven aggression and pot control.",
            "s4": "Leak hunting",
            "s4d": "Tags for tilt, auto-pilot, and curiosity calls.",
            "s5": "Distance mindset",
            "s5d": "One good hour beats five chaotic ones.",
        },
    },
    "mobile": {
        "breadcrumbs": "Guide / Mobile",
        "h1": "JackPoker: Mobile",
        "lead": "Smaller screen, fewer tables, more attention leaks—design sessions around focus and uptime.",
        "cards": {
            "c1t": "Ergonomics",
            "c1d": "Brightness, orientation, and mis-taps.",
            "c2t": "Connectivity",
            "c2d": "Spotty LTE costs timing and buttons.",
            "c3t": "Session length",
            "c3d": "Short bursts beat fatigued marathons.",
        },
        "sections": {
            "s1": "Why mobile differs",
            "s1d": "Attention is the bottleneck—not software pride.",
            "s2": "UI habits",
            "s2d": "Preset bet sizes and intentional delays.",
            "s3": "Table count",
            "s3d": "One table is a feature on phone.",
            "s4": "Security hygiene",
            "s4d": "Lock screen, updates, and trusted networks.",
            "s5": "Responsible pacing",
            "s5d": "Pause when notifications compete with reads.",
        },
    },
    "faq": {
        "breadcrumbs": "Guide / FAQ",
        "h1": "JackPoker: FAQ Hub",
        "lead": "Eighteen direct answers—plus deeper pages if you want structured learning.",
        "cards": {
            "c1t": "Quick clarity",
            "c1d": "Operational answers, not slogans.",
            "c2t": "Cross-links",
            "c2d": "Jump to rules, bonuses, or strategy.",
            "c3t": "Safety",
            "c3d": "Limits and help resources belong in the loop.",
        },
        "sections": {
            "s1": "Using this FAQ",
            "s1d": "Scan headings; expand what matches your situation.",
            "s2": "Housekeeping",
            "s2d": "We do not process balances here.",
            "s3": "Bonuses",
            "s3d": "Always confirm live partner terms.",
            "s4": "Skill path",
            "s4d": "Basics first, optimization later.",
            "s5": "Care",
            "s5d": "If play stops feeling voluntary, seek help.",
        },
    },
    "contacts": {
        "breadcrumbs": "Guide / Contacts",
        "h1": "JackPoker Guide: Contacts",
        "lead": "Editorial scope, realistic response expectations, and where operator support actually lives.",
        "cards": {
            "c1t": "Editorial email",
            "c1d": "Corrections and clarity requests welcome.",
            "c2t": "Not billing support",
            "c2d": "Balances and KYC sit with the partner.",
            "c3t": "Responsible focus",
            "c3d": "We highlight safer play patterns.",
        },
        "sections": {
            "s1": "Purpose",
            "s1d": "Transparency about what we publish.",
            "s2": "Limits of help",
            "s2d": "No account access or dispute handling.",
            "s3": "Accuracy",
            "s3d": "We revise when partners change flows.",
            "s4": "Legal posture",
            "s4d": "Informational content; jurisdiction varies.",
            "s5": "Player wellbeing",
            "s5d": "Tools and timeouts exist for a reason.",
        },
    },
}


FAQ_EN: dict[str, list[tuple[str, str]]] = {
    "index": [
        ("Is this an official JackPoker website?", "No. This is an independent informational guide. Official policies, payments, and support are handled only by the licensed operator you choose."),
        ("Where should I start if I am new?", "Read the rules overview, then play micro stakes with strict time and loss limits. Add strategy notes only after basic flows feel automatic."),
        ("Do you guarantee winnings?", "No. Poker outcomes vary. We teach process and risk control—never profit promises."),
        ("How do I use bonuses safely?", "Compare wagering and eligibility to your real schedule. Skip offers that force you into games or stakes you would not choose otherwise."),
        ("Can you resolve account issues?", "No. For balances, verification, or bonus credit disputes, contact the partner’s official support channels."),
        ("What does responsible play mean here?", "Adults only, pre-set limits, planned breaks, and stopping when emotions—not logic—start steering decisions."),
    ],
    "about": [
        ("What is this review trying to answer?", "Whether the platform’s everyday workflow—navigation, clarity, and stability—fits players who value structured sessions."),
        ("Do you cover every feature?", "We prioritize decision-critical surfaces: lobby-to-table paths, settings visibility, and error recovery—not exhaustive marketing lists."),
        ("How should I interpret drawbacks?", "As trade-offs. A busy lobby may still work if filters are strong; a minimal UI may still fail if key controls hide."),
        ("Is performance the same for everyone?", "No. Device, region, routing, and client version matter. Treat any performance note as directional."),
        ("Does a good UI remove poker risk?", "No. A clear interface reduces mistakes; it does not remove variance or bankroll risk."),
        ("Where do I verify rules that affect me?", "On the operator’s official pages for bonuses, eligibility, and jurisdictional availability."),
    ],
    "how-to-play": [
        ("Which rules matter first?", "Blinds, action order, hand rankings, and what a bet represents on each street—everything else builds on those."),
        ("Why learn rankings before advanced plays?", "You cannot estimate equity or pressure without knowing what beats what on typical runouts."),
        ("What is a simple preflop plan?", "Play fewer hands from early seats, open with clearer intentions, and avoid calling just to see flops."),
        ("How do I avoid beginner tilt?", "Short sessions, fixed loss caps, and pauses after big pots—especially when tired."),
        ("When should I move up stakes?", "Only when your process is stable at current stakes—not because of one lucky session."),
        ("Does reading replace practice?", "No. Reading shrinks mistakes; deliberate reps convert knowledge into timing."),
    ],
    "bonus": [
        ("What should I read first in any promo?", "Eligibility, expiry, wagering or rake requirements, game weighting, and withdrawal conditions tied to the offer."),
        ("Why can wagering make a bonus negative EV?", "Required volume can push you into worse games, higher rake exposure, or rushed decisions."),
        ("Are deposit method restrictions common?", "Yes. Some channels disqualify promos or delay clearance—verify before funding."),
        ("Should I chase the last 10% of a clearing requirement?", "Often no. If it tempts you into bad sessions, the cost exceeds the remaining credit."),
        ("Can terms change while I am clearing?", "Sometimes. Re-check live rules if your campaign spans multiple days or weeks."),
        ("Is a bonus a bankroll rescue tool?", "Never. Bonuses are optional adds; they should not replace disciplined stake selection."),
    ],
    "strategy": [
        ("Why is position emphasized so heavily?", "Acting last yields information that reduces expensive guesses and improves bluff efficiency."),
        ("What is a practical bankroll rule for cash-style play?", "Keep enough buy-ins that normal swings do not force scared money decisions—then adjust to your comfort."),
        ("How do I study without drowning?", "Pick one theme per week—three-bet pots, turn probes, or river bluff catches—and tag hands accordingly."),
        ("What is a leak worth fixing first?", "Anything that repeats under stress: passive calling, auto-steal defense, or sizing tells."),
        ("Does solver study replace fundamentals?", "Solvers refine edges after fundamentals exist; they do not replace attention and discipline."),
        ("How do I measure improvement?", "Cleaner decisions at the same stakes—not necessarily higher immediate winnings."),
    ],
    "mobile": [
        ("Is mobile poker inherently worse?", "Not worse—different. Attention and input precision become the limiting factors."),
        ("How many tables should I play on phone?", "Often one. Multitasking raises mis-click risk and shortens thinking quality."),
        ("What connectivity habits help?", "Stable Wi‑Fi when possible, awareness of hand-off drops, and conservative timing."),
        ("How do I reduce mis-taps?", "Preset bet sizes, deliberate taps, and avoiding play while walking or commuting."),
        ("Should I play the same stakes as desktop?", "Only if decisions feel equally controlled; otherwise drop stakes or shorten sessions."),
        ("When should I stop a mobile session?", "When notifications, glare, or fatigue compete with your reads—pause immediately."),
    ],
    "faq": [
        ("What is JackPoker Guide?", "An independent editorial site that explains poker basics, bonus literacy, and safer session design around the JackPoker product category."),
        ("Is this site affiliated with an operator?", "No. It is informational. Official branding, accounts, and payments belong to licensed operators on their own domains."),
        ("Who is the audience?", "Adults looking for structured learning and safer habits—not “get rich quick” messaging."),
        ("Do you publish live bonus amounts?", "Avoid treating any example as current. Always verify numbers and eligibility on the partner’s live offer pages."),
        ("Can I trust strategy shortcuts online?", "Treat shortcuts as hypotheses. Test them at low stakes and revise with notes—not vibes."),
        ("What is variance?", "Short-term results fluctuate even when decisions are sound. Distance and sample size matter."),
        ("How do I set limits?", "Use deposit, loss, and time caps—before you play—then respect them mechanically."),
        ("What if I feel compelled to keep playing?", "That is a warning signal. Stop, use operator cooling-off tools, and seek professional support if needed."),
        ("Does reading hand charts replace thinking?", "No. Charts start ranges; board texture and opponents adjust them."),
        ("Are HUDs discussed here?", "We focus on universal habits. Third-party tools depend on site rules and fairness norms."),
        ("How important is sleep?", "Critical. Fatigue increases calling mistakes and rage escalations."),
        ("Can I play profitably part-time?", "Some do—usually with strict schedules and modest stakes relative to life expenses."),
        ("What should I track in notes?", "Patterns: positions, sizing tells, emotional triggers, and repeat mistakes—not results alone."),
        ("How do I verify jurisdictional legality?", "Consult local law and the operator’s terms of service for your region."),
        ("Why repeat ‘check partner terms’ so often?", "Because campaigns, payment rules, and eligibility change without this guide updating instantly."),
        ("What if site links fail?", "Operators move campaigns. Open the official destination from the partner’s homepage—not cached hype pages."),
        ("Do you answer medical or legal advice?", "No. For gambling-related harm or legal questions, consult qualified professionals."),
        ("How do I suggest a correction?", "Send a concise note describing the page and the outdated claim; we prioritize safety-critical fixes."),
    ],
    "contacts": [
        ("Can you reset my password or unlock my account?", "No. Account operations are performed only through the operator’s official authentication and support flows."),
        ("Do you provide live chat?", "We do not offer operator-style live support. This project publishes educational content and accepts editorial feedback."),
        ("How fast do you reply?", "If we provide a mailbox on this page, assume non-urgent turnaround. Never use it for financial emergencies."),
        ("Will you forward messages to JackPoker?", "No. We are not a messaging proxy to any operator."),
        ("Can you verify a bonus for me?", "We cannot verify live eligibility. Screen captures and partner support should confirm your specific case."),
        ("What belongs in a good correction request?", "Page URL, what changed on the operator side, and a neutral description—without sharing passwords or payment data."),
    ],
}


def build_ru() -> dict:
    return {
        "menu": {
            "index": "Главная",
            "about": "Обзор",
            "how-to-play": "Как играть",
            "bonus": "Бонусы",
            "strategy": "Стратегия",
            "mobile": "Мобильная",
            "faq": "FAQ",
            "contacts": "Контакты",
        },
        "cta": ["Играть", "Начать", "Бонус", "Открыть площадку"],
        "responsible": "18+. Азартные игры связаны с риском. Сайт носит информационный характер.",
        "disclaimer": "Независимый гайд, не официальный сайт JackPoker. Условия у партнёра могут меняться — проверяйте актуальные правила.",
        "meta": {
            "index": {
                "title": "JackPoker Guide: независимый обзор и с чего начать",
                "description": "Независимый гайд по JackPoker: содержание сайта, порядок разделов и реалистичные ожидания.",
            },
            "about": {
                "title": "JackPoker: обзор интерфейса, функций и ограничений",
                "description": "Редакционный обзор: удобство навигации, возможности клиента и практичные компромиссы.",
            },
            "how-to-play": {
                "title": "Как играть в покер: правила, комбинации, ход раздачи",
                "description": "База для новичков: комбинации, улицы ставок, темп стола и спокойный первый опыт.",
            },
            "bonus": {
                "title": "Бонусы JackPoker: условия, вейджер и здравый смысл",
                "description": "Как читать акции: активация, отыгрыш, ограничения и когда предложение вредит игре.",
            },
            "strategy": {
                "title": "Стратегия покера: позиция, банкролл и типичные ошибки",
                "description": "Основы для дистанции: позиция, дисциплина размеров, банкролл и разбор после сессии.",
            },
            "mobile": {
                "title": "Мобильный покер: фокус, связь и дизайн сессии",
                "description": "Игра с телефона: эргономика, меньше столов, риски связи и безопасный темп.",
            },
            "faq": {
                "title": "FAQ по покеру: 18 практичных ответов",
                "description": "Ответы про старт, бонусы, дисперсию, дисциплину и проверку правил у партнёра.",
            },
            "contacts": {
                "title": "Контакты: границы проекта и ответственная игра",
                "description": "Как связаться с редакцией, чего мы не делаем, и напоминание про 18+.",
            },
        },
        "pages": {s: page_ru(s) for s in SLUGS},
    }


def page_ru(slug: str) -> dict:
    body = load_body(slug, "ru")
    base = PAGES_RU_COMMON[slug]
    faq_pairs = FAQ_RU[slug]
    out = {**base, "body": body, "faq": faq_dict(faq_pairs)}
    w = wc(body)
    if w < 400:
        print(f"warning {slug}.ru words={w}")
    return out


PAGES_RU_COMMON: dict[str, dict] = {
    "index": {
        "breadcrumbs": "Гайд / Обзор",
        "h1": "JackPoker Guide: главная",
        "lead": "Независимые маршруты: правила, обзор, бонусы, стратегия, мобильная игра и ответы без шумихи.",
        "cards": {
            "c1t": "Структура с первого дня",
            "c1d": "Выберите один путь обучения и короткие сессии.",
            "c2t": "Проверяйте у партнёра",
            "c2d": "Бонусы и доступность — только на стороне оператора.",
            "c3t": "Оценивайте решения",
            "c3d": "Разбирайте споты, а не только счёт.",
        },
        "sections": {
            "s1": "Что это за проект",
            "s1d": "Редакционные материалы, не саппорт оператора.",
            "s2": "Порядок чтения",
            "s2d": "Сначала правила, затем стратегия; бонусы — после базы.",
            "s3": "Безопасность важнее",
            "s3d": "Лимиты, паузы и стоп правят импульсом.",
            "s4": "Цикл улучшения",
            "s4d": "Заметки после сессии лучше абстрактных целей.",
            "s5": "Ответственная игра",
            "s5d": "Только 18+; не отыгрывайтесь.",
        },
    },
    "about": {
        "breadcrumbs": "Гайд / Обзор платформы",
        "h1": "JackPoker: обзор",
        "lead": "Практичный взгляд на повседневность: ясность, скорость и места трения.",
        "cards": {
            "c1t": "Навигация",
            "c1d": "Насколько быстро находятся столы и настройки?",
            "c2t": "Сигналы доверия",
            "c2d": "Понятные лимиты снижают сюрпризы.",
            "c3t": "Честные ограничения",
            "c3d": "У любого клиента есть минусы — назовите свои.",
        },
        "sections": {
            "s1": "Позиция обзора",
            "s1d": "Наблюдение, а не маркетинг.",
            "s2": "Поток интерфейса",
            "s2d": "От лобби до стола: меньше лишних нажатий.",
            "s3": "Функции по делу",
            "s3d": "Что меняет решения, а что декоративно.",
            "s4": "Компромиссы",
            "s4d": "Где удобство ценой фокуса.",
            "s5": "Ответственная подача",
            "s5d": "Ставки в рамках навыка и бюджета.",
        },
    },
    "how-to-play": {
        "breadcrumbs": "Гайд / Как играть",
        "h1": "JackPoker: как играть в покер",
        "lead": "Сжатые правила, которые можно применить сегодня — без лишнего жаргона.",
        "cards": {
            "c1t": "Комбинации",
            "c1d": "Пары, дро и готовые руки.",
            "c2t": "Очерёдность",
            "c2d": "Блайнды, улицы и кто ходит первым.",
            "c3t": "Банк и ставки",
            "c3d": "Колл, рейз и фолд эквити простыми словами.",
        },
        "sections": {
            "s1": "Для новичка",
            "s1d": "Меньше рук, ниже лимиты, ясный план.",
            "s2": "Сила руки",
            "s2d": "Абсолютная сила и текстура борда.",
            "s3": "Улицы ставок",
            "s3d": "Как агрессия задаёт давление.",
            "s4": "Этикет",
            "s4d": "Ходите в очереди; берегите тайм-банк.",
            "s5": "Контроль риска",
            "s5d": "Стоп-правила режут эскалацию эмоций.",
        },
    },
    "bonus": {
        "breadcrumbs": "Гайд / Бонусы",
        "h1": "JackPoker: бонусы",
        "lead": "Акции как договор: вейджер, сроки и допустимые игры — до того как брать объём.",
        "cards": {
            "c1t": "Математика отыгрыша",
            "c1d": "Объём может съесть ожидание.",
            "c2t": "Допуск",
            "c2d": "Страны, методы депозита и исключения.",
            "c3t": "Стратегическая пригодность",
            "c3d": "Если тянет в плохие столы — откажитесь.",
        },
        "sections": {
            "s1": "Анатомия оффера",
            "s1d": "Матч, разблокировка, срок, потолки.",
            "s2": "Скрытые ограничения",
            "s2d": "Холды на вывод и частичный клир.",
            "s3": "План объёма",
            "s3d": "Реальные часы против принудительного гринда.",
            "s4": "Связь с банкроллом",
            "s4d": "Не поднимайте лимиты ради отыгрыша.",
            "s5": "Ответственное использование",
            "s5d": "Бонусы опциональны — не инструмент «отбиться».",
        },
    },
    "strategy": {
        "breadcrumbs": "Гайд / Стратегия",
        "h1": "JackPoker: стратегия",
        "lead": "База, которая переживает дисперсию: позиция, диапазоны и честные заметки после игры.",
        "cards": {
            "c1t": "Позиция",
            "c1d": "Поздняя позиция даёт информацию.",
            "c2t": "Диапазоны",
            "c2d": "Ужатый вход, выборочная защита, коррекции по оппонентам.",
            "c3t": "Банкролл",
            "c3d": "Бай-ины спасают ментал в первую очередь.",
        },
        "sections": {
            "s1": "Планирование",
            "s1d": "Цели сессии про навык — не про приз.",
            "s2": "Префлоп-дисциплина",
            "s2d": "Меньше доминируемых рук — чище решения.",
            "s3": "Постфлоп-темы",
            "s3d": "Агрессия от борда и контроль банка.",
            "s4": "Поиск утечек",
            "s4d": "Теги на тилт, автопилот и любопытные коллы.",
            "s5": "Дистанция",
            "s5d": "Один спокойный час лучше пяти хаотичных.",
        },
    },
    "mobile": {
        "breadcrumbs": "Гайд / Мобильная",
        "h1": "JackPoker: мобильная версия",
        "lead": "Меньший экран, меньше столов, больше утечек внимания — стройте сессии вокруг фокуса.",
        "cards": {
            "c1t": "Эргономика",
            "c1d": "Яркость, ориентация, промахи по кнопкам.",
            "c2t": "Связь",
            "c2d": "Обрывы LTE бьют по таймингу.",
            "c3t": "Длина сессии",
            "c3d": "Короткие отрезки лучше усталых марафонов.",
        },
        "sections": {
            "s1": "Чем мобильная отличается",
            "s1d": "Узкое место — внимание, не гордость софта.",
            "s2": "Привычки UI",
            "s2d": "Пресеты сайзинга и осознанные паузы.",
            "s3": "Число столов",
            "s3d": "На телефоне один стол — часто оптимум.",
            "s4": "Гигиена безопасности",
            "s4d": "Экран блокировки, обновления, доверенные сети.",
            "s5": "Ответственный темп",
            "s5d": "Пауза, когда уведомления спорят с чтением.",
        },
    },
    "faq": {
        "breadcrumbs": "Гайд / FAQ",
        "h1": "JackPoker: центр ответов",
        "lead": "Восемнадцать прямых ответов — плюс разделы для глубины.",
        "cards": {
            "c1t": "Быстрая ясность",
            "c1d": "Операционные ответы без лозунгов.",
            "c2t": "Перекрёстные ссылки",
            "c2d": "Переход к правилам, бонусам или стратегии.",
            "c3t": "Безопасность",
            "c3d": "Лимиты и помощь — часть цикла.",
        },
        "sections": {
            "s1": "Как пользоваться FAQ",
            "s1d": "Сканируйте заголовки; раскрывайте релевантное.",
            "s2": "Ограничения сайта",
            "s2d": "Мы не обрабатываем балансы.",
            "s3": "Бонусы",
            "s3d": "Всегда подтверждайте живые условия.",
            "s4": "Путь навыка",
            "s4d": "Сначала база, потом оптимизация.",
            "s5": "Забота",
            "s5d": "Если игра перестала быть выбором — ищите помощь.",
        },
    },
    "contacts": {
        "breadcrumbs": "Гайд / Контакты",
        "h1": "JackPoker Guide: контакты",
        "lead": "Редакционный масштаб, реальные ожидания по ответу и где живёт саппорт оператора.",
        "cards": {
            "c1t": "Почта редакции",
            "c1d": "Правки и уточнения приветствуются.",
            "c2t": "Не биллинг",
            "c2d": "Баланс и KYC — у партнёра.",
            "c3t": "Фокус на безопасности",
            "c3d": "Мы подчёркиваем более спокойные паттерны игры.",
        },
        "sections": {
            "s1": "Цель страницы",
            "s1d": "Прозрачность о том, что публикуем.",
            "s2": "Границы помощи",
            "s2d": "Нет доступа к аккаунтам и спорам.",
            "s3": "Точность",
            "s3d": "Обновляемся, когда меняются потоки у оператора.",
            "s4": "Юридический контекст",
            "s4d": "Информация; юрисдикции различаются.",
            "s5": "Благополучие",
            "s5d": "Тайм-ауты и лимиты существуют не зря.",
        },
    },
}


FAQ_RU: dict[str, list[tuple[str, str]]] = {
    "index": [
        ("Это официальный сайт JackPoker?", "Нет. Это независимый информационный гайд. Официальные правила, платежи и поддержка — только у лицензированного оператора, который вы выбираете."),
        ("С чего начать новичку?", "Сначала обзор правил, затем микролимиты с жёсткими лимитами по времени и потерям. Заметки по стратегии — когда базовый поток уже автоматический."),
        ("Вы гарантируете выигрыш?", "Нет. Покер даёт дисперсию. Мы говорим о процессе и контроле риска — не о прибыли."),
        ("Как аккуратно пользоваться бонусами?", "Сравните отыгрыш и допуск с вашим реальным расписанием. Пропускайте офферы, которые вынуждают играть не те игры или не те лимиты."),
        ("Можете решить проблему с аккаунтом?", "Нет. По балансу, верификации и начислениям — только официальные каналы поддержки партнёра."),
        ("Что здесь значит ответственная игра?", "Только 18+, лимиты заранее, паузы и остановка, когда решения ведут эмоции, а не логика."),
    ],
    "about": [
        ("На какой вопрос отвечает обзор?", "Подходит ли повседневный сценарий — навигация, ясность и стабильность — игрокам, которым важна структура сессии."),
        ("Вы перечисляете все функции?", "Мы приоритизируем путь «лобби → стол», видимость настроек и восстановление после ошибок — не маркетинговые списки."),
        ("Как читать недостатки?", "Как компромиссы. Шумное лобби может быть ок при сильных фильтрах; минимализм не спасает, если ключевые действия спрятаны."),
        ("Одинакова ли производительность для всех?", "Нет. Устройство, регион, маршрут и версия клиента важны. Любые наблюдения — ориентир, не закон."),
        ("Хороший интерфейс убирает риск покера?", "Нет. Он снижает ошибки клика; не убирает дисперсию и банкролл-риск."),
        ("Где проверять правила лично для меня?", "На официальных страницах оператора: бонусы, допуск, доступность в регионе."),
    ],
    "how-to-play": [
        ("Какие правила важнее всего сначала?", "Блайнды, порядок действий, комбинации и что означает ставка на каждой улице — остальное надстраивается."),
        ("Зачем учить комбинации до «трюков»?", "Без базы нельзя честно оценивать эквити и давление на типичных ранаутах."),
        ("Какой простой префлоп-план?", "Меньше рук из ранних позиций, более явные интенты на входе и меньше коллов «просто посмотреть флоп»."),
        ("Как снизить тилт новичка?", "Короткие сессии, потолок потерь, паузы после крупных банков — особенно при усталости."),
        ("Когда поднимать лимиты?", "Когда процесс стабилен на текущих — не из-за одной удачной сессии."),
        ("Чтение заменяет практику?", "Нет. Чтение сокращает ошибки; повторение делает тайминг привычкой."),
    ],
    "bonus": [
        ("Что читать в акции в первую очередь?", "Допуск, срок, отыгрыш или рейк, вес игр и условия вывода, связанные с оффером."),
        ("Почему отыгрыш может сделать бонус минусовым?", "Объём тянет в худшие игры, больше рейка или спешные решения."),
        ("Часты ли ограничения по методу депозита?", "Да. Иногда метод дисквалифицирует промо или задерживает клиринг — проверьте до внесения."),
        ("Гнаться за последними процентами клиринга?", "Часто нет. Если это тянет в плохие сессии, цена выше остатка бонуса."),
        ("Условия могут меняться во время отыгрыша?", "Иногда. Перепроверяйте живые правила, если кампания длятся дни или недели."),
        ("Бонус — способ «спасти» банкролл?", "Нет. Бонусы опциональны; они не заменяют дисциплину выбора лимитов."),
    ],
    "strategy": [
        ("Почему так много про позицию?", "Поздний вход даёт информацию и снижает дорогие угадайки, помогая блефу."),
        ("Практичное правило банкролла для кэша?", "Достаточно бай-инов, чтобы нормальные качели не превращались в «испуганные деньги» — и подстройте под комфорт."),
        ("Как учиться без перегруза?", "Одна тема в неделю — 3-бет-поты, пробы терна, ловля блефов на ривере — и теги рук."),
        ("Какую утечку чинить первой?", "То, что повторяется под стрессом: пассивный колл, автозащита стилов, сайзинг-теллы."),
        ("Солвер заменяет фундамент?", "Солвер уточняет края после базы; не заменяет внимание и дисциплину."),
        ("Как мерить рост?", "Чище решения на тех же лимитах — не обязательно сразу более высокий винрейт."),
    ],
    "mobile": [
        ("Мобильный покер хуже?", "Не хуже — другой. Узкие места — внимание и точность ввода."),
        ("Сколько столов на телефоне?", "Часто один. Мультитаск повышает риск мискликов и режет качество мысли."),
        ("Какие привычки по связи помогают?", "Стабильный Wi‑Fi, понимание обрывов при хендовере и консервативный тайминг."),
        ("Как меньше промахиваться по кнопкам?", "Пресеты сайзинга, осознанные тапы, не играть на ходу без необходимости."),
        ("Те же лимиты, что на ПК?", "Только если контроль решений такой же; иначе снизьте лимит или сократите сессию."),
        ("Когда стопнуть мобильную сессию?", "Когда уведомления, блики или усталость спорят с чтением — сразу пауза."),
    ],
    "faq": [
        ("Что такое JackPoker Guide?", "Независимый редакционный сайт о базе покера, грамотности по бонусам и более безопасном дизайне сессий вокруг продуктовой категории JackPoker."),
        ("Это аффилированный с оператором ресурс?", "Нет. Это информационный проект. Официальный бренд, аккаунты и платежи — на доменах лицензированных операторов."),
        ("Кому это адресовано?", "Взрослым, кто хочет структурное обучение и привычки контроля — не «разбогатеть за неделю»."),
        ("Публикуете ли живые суммы бонусов?", "Не используйте примеры как актуальные. Цифры и допуск — только на живых страницах партнёра."),
        ("Можно ли верить стратегическим «лайфхакам»?", "Как гипотезам. Проверяйте на низких лимитах и заметках — не по ощущению."),
        ("Что такое дисперсия?", "Краткосрочные результаты прыгают даже при адекватных решениях. Важны дистанция и выборка."),
        ("Как ставить лимиты?", "Депозитные, потери и время — до игры — и соблюдайте их механически."),
        ("Что если не могу остановиться?", "Это сигнал. Стоп, инструменты охлаждения у оператора, профессиональная помощь при необходимости."),
        ("Таблицы рук заменяют мышление?", "Нет. Они задают стартовые диапазоны; борд и оппоненты корректируют."),
        ("Обсуждаете ли HUD?", "Мы про универсальные привычки; сторонние инструменты зависят от правил площадки и этики."),
        ("Насколько важен сон?", "Критично. Усталость усиливает ошибочные коллы и эскалацию злости."),
        ("Можно ли стабильно играть вне основной работы?", "У некоторих получается — обычно с жёстким расписанием и скромными лимитами относительно расходов."),
        ("Что записывать в заметки?", "Паттерны: позиции, сайзинг-теллы, триггеры эмоций, повторяющиеся ошибки — не только результаты."),
        ("Как проверить легальность в регионе?", "Изучите местное право и пользовательское соглашение оператора для вашей страны."),
        ("Почему так часто «проверьте у партнёра»?", "Кампании, платежи и допуск меняются быстрее, чем мы обновляем каждую строку."),
        ("Что если ссылки не работают?", "Операторы переносят кампании. Открывайте официальный пункт назначения с домашней страницы партнёра."),
        ("Даёте ли медицинские или юридические советы?", "Нет. По вреду от азартных игр или правовым вопросам — к квалифицированным специалистам."),
        ("Как предложить исправление?", "Коротко: страница, что устарело на стороне оператора, без паролей и платёжных данных."),
    ],
    "contacts": [
        ("Можете сбросить пароль или разблокировать аккаунт?", "Нет. Операции с аккаунтом — только через официальную аутентификацию и поддержку оператора."),
        ("Есть ли живой чат у гайда?", "Нет операторского чата. Проект публикует обучающий контент и принимает редакционные замечания."),
        ("Как быстро вы отвечаете?", "Если указан ящик — ориентируйтесь на несрочный срок. Финансовые срочности — только у партнёра."),
        ("Пересылаете ли сообщения в JackPoker?", "Нет. Мы не посредник между вами и оператором."),
        ("Можете подтвердить бонус за меня?", "Нет. Живой допуск и условия подтверждает поддержка и ваш аккаунт у партнёра."),
        ("Что указать в запросе на исправление?", "URL страницы, что изменилось у оператора, нейтральное описание — без паролей и платёжных данных."),
    ],
}


def main() -> None:
    for lang in ("en", "ru"):
        data = build(lang)
        path = ROOT / "lang" / f"{lang}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path}")
        for slug in SLUGS:
            b = data["pages"][slug]["body"]
            print(f"  {slug}.{lang}: {wc(b)} words")


if __name__ == "__main__":
    main()
