

from pathlib import Path
import csv
import yaml

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))


def is_nalanda_text(text_id, nalanda_texts):
    if text_id in nalanda_texts:
        return True
    else:
        return False


if __name__ == "__main__":
    nalanda_texts = Path('./nalanda_text.txt').read_text(encoding='utf-8').splitlines()
    pedurma_index = from_yaml(Path('./pedurma_index.yml'))
    nalanda_text_found_in_pedurma = ''
    nalanda_text_not_found_in_pedurma = ''
    texts = pedurma_index['annotations']
    for uuid, text in texts.items():
        if text['work_id']:
            if is_nalanda_text(text['work_id'], nalanda_texts):
                nalanda_texts.remove(text['work_id'])
                nalanda_text_found_in_pedurma += text['work_id'] + '\n'
    nalanda_text_not_found_in_pedurma = "\n".join(nalanda_texts)
    Path('nalanda_text_found_in_pedurma.txt').write_text(nalanda_text_found_in_pedurma, encoding='utf-8')
    Path('nalanda_text_not_found_in_pedurma.txt').write_text(nalanda_text_not_found_in_pedurma, encoding='utf-8')
            

