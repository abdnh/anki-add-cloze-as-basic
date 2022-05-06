import re
from typing import Match, Tuple

from aqt import mw
from aqt.addcards import AddCards
from aqt.gui_hooks import add_cards_did_init
from aqt.qt import *
from aqt.utils import showWarning, tooltip, tr

CONFIG = mw.addonManager.getConfig(__name__)
CLOZE_RE = re.compile(r"(?si){{c(\d+)::(.*?)}}")


def reveal_cloze(text: str, num: int) -> Tuple[str, str]:
    clozed_parts = []

    def repl(match: Match) -> str:
        n = int(match.group(1))
        clozed = match.group(2)
        if num == n:
            clozed_parts.append(clozed)
            return '<span class="cloze">[...]</span>'
        else:
            return clozed

    text = CLOZE_RE.sub(repl, text)
    return text, ", ".join(clozed_parts)


def add_cloze_as_basic(addcards: AddCards) -> None:
    note = addcards.editor.note
    text = note.fields[0]
    notetype = mw.col.models.by_name(tr.notetypes_basic_name())
    did = addcards.deck_chooser.selected_deck_id
    if not notetype:
        showWarning(
            "Basic notetype not found. Please create it from Tools > Manage Note Types."
        )
        return
    cloze_numbers = note.cloze_numbers_in_fields()
    for cloze_num in cloze_numbers:
        front, back = reveal_cloze(text, cloze_num)
        note = mw.col.new_note(notetype)
        # TODO: maybe check for the existence of Front and Back
        note[tr.notetypes_front_field()] = front
        note[tr.notetypes_back_field()] = back
        mw.col.add_note(note, did)

    notes_count = len(cloze_numbers)
    if notes_count:
        if notes_count == 1:
            msg = f"Added one basic note."
        else:
            msg = f"Added {notes_count} basic notes."
        tooltip(msg)
        if hasattr(addcards, "_load_new_note"):
            addcards._load_new_note(sticky_fields_from=addcards.editor.note)
        mw.reset()
    else:
        showWarning("No clozes to add.")


def add_button(addcards: AddCards) -> None:
    buttonBox = addcards.form.buttonBox
    button = buttonBox.addButton(
        "Add cloze as basic", QDialogButtonBox.ButtonRole.ActionRole
    )
    shortcut = CONFIG["shortcut"]
    button.setShortcut(QKeySequence(shortcut))
    button.setToolTip(shortcut)
    qconnect(button.clicked, lambda: add_cloze_as_basic(addcards))


add_cards_did_init.append(add_button)
