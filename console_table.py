import unicodedata

def display_width(text: str) -> int:
    width = 0

    for char in text:
        if unicodedata.category(char) in ("Mn", "Me", "Cf"):
            continue
        if unicodedata.east_asian_width(char) in ("W", "F"):
            width += 2
        else:
            width += 1

    return width


def cell_text(value) -> str:
    if value is None:
        return "N/A"

    text = str(value)
    text = " ".join(text.splitlines())
    text = text.expandtabs(4)

    return unicodedata.normalize("NFC", text)


def format_row(row, widths, right_align) -> str:
    cells = []

    for index, text in enumerate(row):
        padding = " " * (widths[index] - display_width(text))

        if index in right_align:
            cells.append(padding + text)
        else:
            cells.append(text + padding)

    return " | ".join(cells)


def format_table(headers, rows, right_align=()) -> str:
    headers = tuple(cell_text(value) for value in headers)
    rows = tuple(
        tuple(cell_text(value) for value in row)
        for row in rows
    )

    for row in rows:
        if len(row) != len(headers):
            raise ValueError("제목과 데이터의 열 개수가 일치해야 합니다.")

    widths = [display_width(header) for header in headers]

    for row in rows:
        for index, text in enumerate(row):
            width = display_width(text)
            if width > widths[index]:
                widths[index] = width

    separator = "-+-".join("-" * width for width in widths)
    lines = [
        separator,
        format_row(headers, widths, right_align),
        separator,
    ]

    for row in rows:
        lines.append(format_row(row, widths, right_align))

    lines.append(separator)

    return "\n".join(lines)
