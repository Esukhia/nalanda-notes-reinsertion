

import re
import yaml
import shutil
from pathlib import Path

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys = False, allow_unicode=True)

def offset_update(old_notes, offset):
    new_notes = {}
    for page_no, note in old_notes.items():
        image_no = int(page_no) + offset
        new_notes[image_no] = note
    return new_notes

def process_vol(vol, offset):
    texts = list(vol.iterdir())
    texts.sort()
    for text in texts:
        if text.stem == 'D3788':
            print(text.stem)
        old_notes = from_yaml(text)
        new_notes = offset_update(old_notes, offset)
        Path(f'./new_notes/{text.stem}.yml').write_text(to_yaml(new_notes), encoding='utf-8')


if __name__ == "__main__":
    vol_offset = from_yaml(Path('./note_vol_offset.yml'))

    vols = list(Path('./notes_vol/').iterdir())
    vols.sort()

    for vol in vols:
        vol_num = vol.stem
        offset = vol_offset[vol_num]
        process_vol(vol, offset)
        print(f'{vol} completed..')

