import yaml
import re
from pathlib import Path
from antx import transfer

PARMA_META = {
    'derge': {
        'annotation': '《སྡེ》',
        'work_id': 'W2KG209989',
        'img_group_offset': 10051,
        'pref': 'I2KG2',
    },
    'narthang': {
        'annotation': '《སྣར་》',
        'work_id': 'W22704',
        'img_group_offset': 3251,
        'pref': ''
    },
    'co_ne': {
        'annotation': '《ཅོ་》',
        'work_id': 'W1GS66030',
        'img_group_offset': 66031,
        'pref': 'I1GS'
    },
    'pe_cing': {
        'annotation': '《པེ་》',
        'work_id': 'W1KG13126',
        'img_group_offset': 13169,
        'pref': 'I1KG'
    },
    'pedurma': {
        'annotation': '',
        'work_id': 'W1PD95844',
        'img_group_offset': 95845,
        'pref': 'I1PD'
    }
}

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(f"(\[[𰵀-󴉱]?\d+[a-b]+\])", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result

def get_last_syl(chunk):
    chunks = re.split('་', chunk)
    if chunks[-1]: 
        if "\n" == chunk[-1] or chunk[-1] == " ":
            last_syl = "་".join(chunks[-2:])
        else:
            last_syl = chunks[-1]
    else:
        last_syl = "་".join(chunks[-2:])
    return last_syl

def get_old_note(chunk):
    if re.search(':.+?$', chunk):
        old_note = re.search(':.+?$', chunk)[0]
        return old_note
    else:
        old_note = get_last_syl(chunk)
    old_note = re.sub('\[.+\]', "", old_note)
    return old_note

def is_punct(string):
    # put in common
    if '༄' in string or '༅' in string or '༆' in string or '༇' in string or '༈' in string or \
        '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or \
        '༔' in string or '_' in string:
        return True
    else:
        return False

def get_new_note(note, next_chunk):
    new_note = note
    first_char = next_chunk[0]
    if not is_punct(first_char):
        new_note = re.sub('།', '་', new_note)
        new_note = re.sub('་་', '་', new_note)
    elif is_punct(first_char):
        new_note = re.sub('།', '', new_note)
    return new_note

def get_next_chunk(chunk_walker, chunks):
    if chunk_walker < len(chunks):
        return chunks[chunk_walker + 1]
    else:
        return ''

def reinsert_notes(pg, notes, pub):
    new_pg = ''
    chunks = re.split('#', pg)
    for chunk_walker, (chunk, (note_id, note)) in enumerate(zip(chunks, notes.items())):
        next_chunk = get_next_chunk(chunk_walker, chunks)
        new_chunk = ""
        old_note = get_old_note(chunk)
        if note[pub]:
            if "m" in note[pub]:
                new_chunk = re.sub(old_note+"$", '', chunk)
            elif "p" in note[pub]:
                new_chunk = chunk + note[pub][1:]
            else:
                new_note = get_new_note(note[pub], next_chunk)
                new_chunk = re.sub(old_note+"$", new_note, chunk)
        else:
            new_chunk = re.sub(':', '', chunk)
        new_pg += new_chunk
    new_pg += chunks[-1]
    return new_pg


def construct_notes(note):
    combined_notes = '<'
    for pub, note_value in note.items():
        if note_value:
            combined_notes += f"{pub}{note_value},"
    combined_notes += '>'
    return combined_notes


def reinsert_pedurma_notes(pg, notes):
    new_pg = pg
    for note_id, note in notes.items():
        combined_note = construct_notes(note)
        new_pg = re.sub('#', combined_note, new_pg, 1)
    return new_pg


def reinsert_text_footnote(pages, notes, pub = PARMA_META['derge']['annotation']):
    new_text = ''
    for cur_pg, (pg_num, cur_pg_notes) in zip(pages, notes.items()):
        if pub:
            new_text += reinsert_notes(cur_pg, cur_pg_notes, pub)
        else:
            new_text += reinsert_pedurma_notes(cur_pg, cur_pg_notes)
    return new_text

def rm_annotations(text, annotations):
    clean_text = text
    for ann in annotations:
        clean_text = re.sub(ann, '', clean_text)
    return clean_text

def text_with_google_line_break(text, g_text):
    annotations = [['line_break', '(\n)'], ['pagination', '(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])']]
    g_annotations = ['\n', '\[[𰵀-󴉱]?[0-9]+[a-z]{1}\]', '\[\w+\.\d+\]', '\{([𰵀-󴉱])?\w+\}']
    clean_text = rm_annotations(text, g_annotations)
    text_with_google_linebreak = transfer(g_text, annotations, clean_text, output='txt')
    return text_with_google_linebreak

def reformat_text_with_note(original_text, text_with_note):
    annotations = [['line_break', '(\n)'], ['pagination', '(\[[0-9]+[a-z]{1}\])']]
    text_with_note = rm_annotations(text_with_note, ['\n', '\[[0-9]+[a-z]{1}\]'] )
    original_text_with_note = transfer(original_text, annotations, text_with_note, output='txt')
    return original_text_with_note 

def get_page_num(page_pat):
    pg_num = int(page_pat.group(1))*2
    pg_face = page_pat.group(2)
    if pg_face == 'a':
        pg_num -= 1
    return pg_num

def get_link(page, vol, parma = "derge"):
    work = PARMA_META[parma]['work_id']
    img_group_offset = PARMA_META[parma]['img_group_offset']
    page_pat = re.search('\[[𰵀-󴉱]?([0-9]+)([a-z]{1})\]', page)
    pg_num = get_page_num(page_pat)
    pref = PARMA_META[parma]['pref']
    igroup = f"{pref}{img_group_offset+vol}"
    link = f"[https://www.tbrc.org/browser/ImageService?work={work}&igroup={igroup}&image={pg_num}&first=1&last=2000&fetchimg=yes]"
    return link

def add_page_link(text, vol, parma="derge"):
    text_with_page_link = ''
    pages = get_pages(text)
    for page in pages:
        pg_link = get_link(page, vol, parma)
        text_with_page_link += f'{page}\n{pg_link}\n'
    return text_with_page_link

def reinsert_manual_note_2_text(hfml_text, pedurma_google_text, notes, parma = "derge"):
    text_with_google_linebreak = text_with_google_line_break(hfml_text, pedurma_google_text)
    pages = get_pages(text_with_google_linebreak)

    text_with_notes = reinsert_text_footnote(pages, notes, pub = PARMA_META[parma]['annotation'])
    if parma != 'pedurma':
        original_text_with_note = reformat_text_with_note(hfml_text, text_with_notes)
    else:
        original_text_with_note =text_with_notes
    return original_text_with_note
