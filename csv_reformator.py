

import csv
import re
import yaml
from pathlib import Path

def parse_note(note):
    reformat_notes = {
        '《པེ་》': '',
        '《སྣར་》': '',
        '《སྡེ》': '',
        '《ཅོ་》': ''
    }
    note_parts = re.split('(《.+?》)', note)
    pubs = note_parts[1::2]
    notes = note_parts[2::2]
    for walker, (pub, note_part) in enumerate(zip(pubs, notes)):
        if note_part:
            reformat_notes[pub] = note_part.replace(' ', '')
        else:
            if notes[walker+1]:
                reformat_notes[pub] = notes[walker+1].replace(' ', '')
            else:
                reformat_notes[pub] = notes[walker+2].replace(' ', '')
            
    return reformat_notes

def reformat_csv(text_id):
    text = {}
    cur_page = {}
    pg_no = []
    with open(f'input/{text_id}.csv', newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row_num, row in enumerate(rows,1):
            if row_num < 2:
                 pass
            else:
                notes = parse_note(" ".join(row[4:]))
                if row[1]:
                    if cur_page:
                        text[pg_no[-1]] = cur_page
                        cur_page = {}
                        cur_page[row[3]] = notes
                        pg_no.append(row[1])
                    else:
                        cur_page[row[3]] = notes
                        pg_no.append(row[1])
                else:
                    cur_page[row[3]] = notes
    if cur_page:
        text[pg_no[-1]] = cur_page
    return text


if __name__ == "__main__":
    INPUT_PATH = './input'

    text_paths = list(Path(INPUT_PATH).rglob('*.csv'))
    text_paths.sort()

    for text_path in text_paths:
        text_id = text_path.stem
        text = reformat_csv(text_id)
        text_yml = yaml.safe_dump(text, default_flow_style=False, sort_keys=False,  allow_unicode=True)
        Path(f'./notes_reformated/{text_id}.yaml').write_text(text_yml, encoding='utf-8')
        print(f'{text_id} completed...')

