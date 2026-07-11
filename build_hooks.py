"""build_hooks.py — трансформація контенту при збірці MkDocs.

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


def _sort_key(label):
    """Ключ сортування: спроба українського локалю, інакше lower()."""
    import locale
    try:
        locale.setlocale(locale.LC_COLLATE, "uk_UA.UTF-8")
        return locale.strxfrm(label.strip().lower())
    except (locale.Error, OSError):
        return label.strip().lower()


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

    # Сортування за алфавітом (українським, якщо доступно)
    items.sort(key=lambda x: _sort_key(x[0]))

    # Групування за першою літерою (верхній регістр)
    groups = {}
    for label, target in items:
        first = (label[0].upper() if label else "#")
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
