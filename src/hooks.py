"""src/hooks.py — трансформація контенту при збірці MkDocs.

НЕ редагує вихідні файли у `data/`. Лише зчитує `wiki/index.md`
і перетворює його тіло на алфавітний покажчик усіх статей вікі
(концепції + сутності + архів) із розділами-літерами. Джерела
(raw/**) не включаються. Результат підставляється у вихід `site/`
через `page.content`.
"""

import os
import re

# Посилання вигляду [Текст](шлях)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


UKRAINIAN_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
LATIN_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

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
    for label, target in LINK_RE.findall(text):
        target = target.split("#")[0].strip()
        if not target:
            continue
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        parts = target.split("/")
        category = parts[0]
        if category in ("concepts", "entities", "archives"):
            key = (label.strip(), target)
            if key in seen:
                continue
            seen.add(key)
            items.append((label.strip(), target))

    if not items:
        return markdown

    # Сортування за алфавітом
    items.sort(key=lambda x: _sort_key(x[0]))

    # Групування за першою літерою (верхній регістр)
    groups = {}
    for label, target in items:
        first = label[0].upper() if label else "#"
        groups.setdefault(first, []).append(f"- [{label}]({target})")

    # Порядок літер за алфавітом
    letters = sorted(groups.keys(), key=_sort_key)

    header = (
        "# Науковий образ світу\n\n"
        "База знань курсу «Науковий образ світу» — серія науково-популярних "
        "лекцій про сучасну наукову картину світу: від будови матерії та "
        "походження Всесвіту до еволюції життя, свідомості й штучного "
        "інтелекту.\n\n"
        "<p class=\"section-title\">Усі статті</p>\n\n"
    )

    body_parts = []
    for letter in letters:
        # Використовуємо <p> (а не <h3>/###), щоб Material НЕ додавав
        # ці розділи в автоматичний TOC (лівий/правий сайдбар)
        body_parts.append(f'<p class="alpha-section">{letter}</p>')
        body_parts.append("\n".join(groups[letter]))
        body_parts.append("")  # порожній рядок між літерами

    return header + "\n".join(body_parts) + "\n"


def on_post_build(config):
    """Генеруємо файл index.html в корені папки site для редіректу на wiki/."""
    site_dir = config.get("site_dir", "site")
    index_path = os.path.join(site_dir, "index.html")

    html_content = (
        '<!DOCTYPE html>\n'
        '<html lang="uk">\n'
        '<head>\n'
        '  <meta charset="utf-8">\n'
        '  <title>Науковий образ світу</title>\n'
        '  <meta http-equiv="refresh" content="0; url=wiki/">\n'
        '  <script>window.location.replace("wiki/")</script>\n'
        '</head>\n'
        '<body>\n'
        '  <p>Завантаження... Якщо вас не перенаправило автоматично, <a href="wiki/">перейдіть за цим посиланням</a>.</p>\n'
        '</body>\n'
        '</html>\n'
    )

    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    except OSError:
        pass


def on_config(config):
    """Динамічно генеруємо навігаційне меню при збірці."""
    docs_dir = config["docs_dir"]
    nav = [{"Головна": "wiki/index.md"}]

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
        nav.append({"Статті": articles})

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
        nav.append({"Джерела": sources})

    config["nav"] = nav
    return config
