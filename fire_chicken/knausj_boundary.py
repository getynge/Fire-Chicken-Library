from talon import actions

def get_draft_window_text() -> str:
    return actions.user.draft_get_text()

def open_empty_draft_window():
    actions.user.draft_show("")

def close_draft_window():
    actions.user.draft_hide()

def discard_draft_window_draft():
    open_empty_draft_window()
    close_draft_window()
