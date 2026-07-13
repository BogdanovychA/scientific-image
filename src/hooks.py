"""src/hooks.py — трансформація контенту при збірці MkDocs.

НЕ редагує вихідні файли у `data/`. Лише зчитує `wiki/index.md`
і перетворює його тіло на алфавітний покажчик усіх статей вікі
(концепції + сутності + архів) із розділами-літерами. Джерела
(raw/**) не включаються. Результат підставляється у вихід `site/`
через `page.content`.
"""

import os
import re

import yaml

HOOKS_DIR = os.path.dirname(__file__)

# Завантажуємо конфігурацію
CONFIG_PATH = os.path.join(HOOKS_DIR, "config.yaml")
with open(CONFIG_PATH, encoding="utf-8") as fh:
    CONFIG = yaml.safe_load(fh)

# Завантажуємо шаблони
HEADER_PATH = os.path.join(HOOKS_DIR, "templates", "main_page_header.md")
with open(HEADER_PATH, encoding="utf-8") as fh:
    HEADER_TEMPLATE = fh.read()

REDIRECT_PATH = os.path.join(HOOKS_DIR, "templates", "redirect.html")
with open(REDIRECT_PATH, encoding="utf-8") as fh:
    REDIRECT_TEMPLATE = fh.read()

# Посилання вигляду [Текст](шлях)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

UKRAINIAN_ALPHABET = CONFIG["alphabets"]["ukrainian"]
LATIN_ALPHABET = CONFIG["alphabets"]["latin"]

UKRAINIAN_MAP = {c: i for i, c in enumerate(UKRAINIAN_ALPHABET)}
LATIN_MAP = {c: i for i, c in enumerate(LATIN_ALPHABET)}


def _sort_key(label):
    """Ключ сортування для українських, латинських літер та символів.

    Сортує в порядку: українські літери -> латинські літери -> інші символи.
    """
    key = []
    for c in label.strip().lower():
        if c in UKRAINIAN_MAP:
            key.append((0, UKRAINIAN_MAP[c]))
        elif c in LATIN_MAP:
            key.append((1, LATIN_MAP[c]))
        else:
            key.append((2, ord(c)))
    return key


def on_page_markdown(markdown, page, config, files):
    """Для головної сторінки (wiki/index.md) генеруємо алфавітний покажчик."""
    src_path = getattr(page.file, "src_path", "")
    is_home = getattr(page, "is_homepage", False)

    if not (src_path == "wiki/index.md" or is_home):
        return markdown

    # Зчитуємо оригінальний файл із диска (без мутації самого файлу).
    abs_path = os.path.join(config["docs_dir"], src_path)
    try:
        with open(abs_path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return markdown

    items = []
    seen = set()
    for line in text.splitlines():
        line_stripped = line.strip()
        desc = ""
        # Якщо рядок схожий на рядок таблиці (починається і закінчується на '|')
        if line_stripped.startswith("|") and line_stripped.endswith("|"):
            parts = [p.strip() for p in line_stripped.split("|")]
            # Структура таблиці: | Посилання | Опис | Дата | ...
            # parts має містити як мінімум 4 елементи: ['', посилання, опис, дата, ...]
            if len(parts) >= 4:
                cell_link = parts[1]
                match = LINK_RE.search(cell_link)
                if match:
                    label = match.group(1).strip()
                    target = match.group(2).split("#")[0].strip()
                    desc = parts[2].strip()
                    if not target or target.startswith(
                        ("http://", "https://", "mailto:")
                    ):
                        continue
                    cat = target.split("/")[0]
                    if cat in ("concepts", "entities", "archives"):
                        key = (label, target)
                        if key not in seen:
                            seen.add(key)
                            items.append((label, target, desc))
                    continue

        # Звичайний пошук посилань у рядку для сумісності
        for label, target in LINK_RE.findall(line):
            target = target.split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            cat = target.split("/")[0]
            if cat in ("concepts", "entities", "archives"):
                key = (label.strip(), target)
                if key not in seen:
                    seen.add(key)
                    items.append((label.strip(), target, ""))

    if not items:
        return markdown

    # Сортування за алфавітом
    items.sort(key=lambda x: _sort_key(x[0]))

    # Групування за першою літерою (верхній регістр)
    groups = {}
    for label, target, desc in items:
        first = label[0].upper() if label else "#"
        if desc:
            groups.setdefault(first, []).append(
                CONFIG["templates"]["list_item_with_desc"].format(
                    label=label, target=target, desc=desc
                )
            )
        else:
            groups.setdefault(first, []).append(
                CONFIG["templates"]["list_item_no_desc"].format(
                    label=label, target=target
                )
            )

    # Порядок літер за алфавітом
    letters = sorted(groups.keys(), key=_sort_key)

    header = HEADER_TEMPLATE.rstrip() + "\n\n"

    body_parts = []
    for letter in letters:
        # Використовуємо <p> (а не <h3>/###), щоб Material НЕ додавав
        # ці розділи в автоматичний TOC (лівий/правий сайдбар)
        body_parts.append(CONFIG["templates"]["letter_section"].format(letter=letter))
        body_parts.append("\n".join(groups[letter]))
        body_parts.append("")  # порожній рядок між літерами

    return header + "\n".join(body_parts) + "\n"


def on_post_build(config):
    """Генеруємо файл index.html в корені папки site для редіректу на wiki/."""
    site_dir = config.get("site_dir", "site")
    index_path = os.path.join(site_dir, "index.html")

    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(REDIRECT_TEMPLATE)
    except OSError:
        pass


def on_config(config):
    """Динамічно генеруємо навігаційне меню при збірці."""
    docs_dir = config["docs_dir"]
    nav = [{CONFIG["navigation"]["home_title"]: "wiki/index.md"}]

    # 1. Статті (wiki/concepts/, wiki/entities/, wiki/archives/)
    articles = []
    for category in ("concepts", "entities", "archives"):
        cat_dir = os.path.join(docs_dir, "wiki", category)
        if os.path.isdir(cat_dir):
            for file in sorted(os.listdir(cat_dir)):
                if file.endswith(".md"):
                    rel_path = f"wiki/{category}/{file}"
                    articles.append(rel_path)
    if articles:
        nav.append({CONFIG["navigation"]["articles_title"]: articles})

    # 2. Джерела (raw/**)
    sources = []
    raw_dir = os.path.join(docs_dir, "raw")
    if os.path.isdir(raw_dir):
        for root, dirs, files in os.walk(raw_dir):
            for file in files:
                if file.endswith(".md"):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, docs_dir).replace("\\", "/")
                    sources.append(rel_path)
        sources.sort()
    if sources:
        nav.append({CONFIG["navigation"]["sources_title"]: sources})

    # 3. Інформаційні сторінки (pages/**)
    pages_dir = os.path.join(docs_dir, "pages")
    if os.path.isdir(pages_dir):
        for file in sorted(os.listdir(pages_dir)):
            if file.endswith(".md"):
                rel_path = f"pages/{file}"
                nav.append(rel_path)

    config["nav"] = nav
    return config
