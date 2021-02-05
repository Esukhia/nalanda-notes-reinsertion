from antx.core import from_yaml
import yaml
import re
from pathlib import Path
from reinsert_note import reinsert_manual_note_2_text


def test_reinsert_notes():
    hfml_text = Path('./test/data/derge_hfml.txt').read_text(encoding='utf-8')
    pedurma_text= Path('./test/data/pedurma_hfml.txt').read_text(encoding='utf-8')
    notes = from_yaml(Path('./test/data/notes.yml'))
    new_text = reinsert_manual_note_2_text(hfml_text, pedurma_text, notes, parma="derge")
    expected_text = Path('./test/data/expected_text.txt').read_text(encoding='utf-8')
    assert new_text == expected_text