import sys
import re
from collections import Counter
import argparse

alphabet_re = {
    'en' : r'[^A-Za-z ]',
    'ru' : r'[^А-Яа-я ]'
}

def clean_text(src_path, src_lang, tgt_path, tgt_lang, output_dir = None, val_size = 0.001, test_size = 0.0001, split = False):
    '''
    Cleans parallel corpora from irrelevant entries
    Arguments:
    source_files (list<str>): paths to corpora
    output_dir(str): path to output directory (optional)
    Returns: None
    Creates train, val and test files for each source file
    '''
    if output_dir is None:
        output_dir = ''
        
    least_common_src_ids = set(least_common_ids(src_path, alphabet_re[src_lang]))
    least_common_tgt_ids = set(least_common_ids(tgt_path, alphabet_re[tgt_lang]))
    sparse_src_ids = set(sparse_ids(src_path, alphabet_re[src_lang]))
    sparse_tgt_ids = set(sparse_ids(tgt_path, alphabet_re[tgt_lang]))
    bad_ids = set.union(least_common_src_ids, least_common_tgt_ids, sparse_src_ids, sparse_tgt_ids)
    
    if not split:
        with open(src_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        with open(output_dir+'src_full', 'w') as f:
            for i, item in enumerate(content):
                if i not in bad_ids:
                    f.write(item+'\n')
        with open(tgt_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        with open(output_dir+'tgt_full', 'w') as f:
            for i, item in enumerate(content):
                if i not in bad_ids:
                    f.write(item+'\n')
    else:
        train_val_test_split(src_path, tgt_path, bad_ids, output_dir, val_size, test_size)
    

def least_common_ids(filename, alphabet_regex, min_num = 1):
    with open(filename) as f:
        content = f.read()
    result = re.sub(alphabet_regex, ' ', content)
    result = re.sub(r'[ ]+', ' ', result).lower()
    cnt = Counter(result.split())
    bad_words = set([a[0] for a in cnt.items() if a[1] <= min_num])
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    bad_ids = []
    for i, item in enumerate(content):
        res = re.sub(alphabet_regex, ' ', item)
        res = re.sub(r'[ ]+', ' ', res).lower()
        for word in res.split():
            if word in bad_words:
                bad_ids.append(i)
                break
    return bad_ids
                    
def sparse_ids(filename, alphabet_regex, percentage = 0.8):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    
    bad_ids = []
    for i, item in enumerate(content):
        clean = re.sub(alphabet_regex, ' ', item)
        clean = re.sub(r'[ ]+', ' ', clean).lower()
        if len(clean) < percentage*len(item):
            bad_ids.append(i)
    return bad_ids            
    
def train_val_test_split(src_file, tgt_file, bad_ids, dir_path = None, val_size = 0.001, test_size = 0.0001):
    with open(src_file) as f:
        src = f.readlines()
    src = [x.strip() for x in src]
    
    with open(tgt_file) as f:
        tgt = f.readlines()
    tgt = [x.strip() for x in tgt]
    
    assert len(src) == len(tgt)
    
    length = len(src)
    val_size = round(length*val_size)
    test_size = round(length*test_size)
    
    #train
    with open(dir_path+'src-train', 'w') as f:
        for i, item in enumerate(src[:-(val_size+test_size)]):
            if i not in bad_ids:
                f.write(item+'\n')
                
    with open(dir_path+'tgt-train', 'w') as f:
        for i, item in enumerate(tgt[:-(val_size+test_size)]):
            if i not in bad_ids:
                f.write(item+'\n')
    #val
    with open(dir_path+'src-val', 'w') as f:
        for i, item in enumerate(src[-(val_size+test_size):-test_size]):
            if i not in bad_ids:
                f.write(item+'\n')
            
    with open(dir_path+'tgt-val', 'w') as f:
        for i, item in enumerate(tgt[-(val_size+test_size):-test_size]):
            if i not in bad_ids:
                f.write(item+'\n')
                
    #test
    with open(dir_path+'src-test', 'w') as f:
        for i, item in enumerate(src[-test_size:]):
            if i not in bad_ids:
                f.write(item+'\n')
                
    with open(dir_path+'tgt-test', 'w') as f:
        for i, item in enumerate(tgt[-test_size:]):
            if i not in bad_ids:
                f.write(item+'\n')
    
def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help="source language corpus file", action = 'store', type = str, required = True)
    parser.add_argument('-sl', '--sourcelang', help="source language", action = 'store', type = str, required = True)
    parser.add_argument('-t', '--target', help="target language corpus file", action = 'store', type = str, required = True)
    parser.add_argument('-tl', '--targetlang', help="target language", action = 'store', type = str, required = True)
    parser.add_argument('-o', '--output', help="output dir path", action = 'store', type = str, required = False)
    parser.add_argument('-val', '--valsize', help="val fraction of dataset", action = 'store', type = float, default = 0.001)
    parser.add_argument('-test','--testsize', help="test fraction of dataset", action = 'store', type = float, default = 0.0001)
    parser.add_argument('--split', help = "whether to make train-val-test split", action = 'store_true')
    args = parser.parse_args()
#     print(args.source)
#     print(args.target)
#     print(args.output)
#     print(args.valsize)
#     print(args.testsize)
#     print(args.split)
    clean_text(args.source, args.sourcelang, args.target, args.targetlang, args.output, args.valsize, args.testsize, args.split)
    
if __name__ == '__main__':
    Main()