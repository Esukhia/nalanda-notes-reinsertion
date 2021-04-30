from antx.core import from_yaml
from pathlib import Path
from reinsert_note import reinsert_manual_note_2_text


def test_reinsert_notes():
    hfml_text = Path('./test/data/derge_hfml.txt').read_text(encoding='utf-8')
    pedurma_text= Path('./test/data/pedurma_hfml.txt').read_text(encoding='utf-8')
    notes = yaml.safe_load(Path('./test/data/notes.yml').read_text(encoding="utf-8"))
    new_text = reinsert_manual_note_2_text(hfml_text, pedurma_text, notes, parma="pedurma")
    Path('./test/data/expected_text.txt').write_text(new_text, encoding='utf-8')