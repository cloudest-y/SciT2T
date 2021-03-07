#!/use/bin/python
#coding=utf-8

import os
import json
'''
Input pdf_parse file

{
    "paper_id": "...", 
    "abstract":[{"section","text"...}],
    "body_text": [{"section","text"...}],
    "ref_entries": {
        ...
        "TABREF0": 
            {
                "text": "...caption1...", 
                "type": "table"
            }
        ...
        "TABREFN": {"text": "...captionN...",     "type": "table"},
    }
}
Output Caption File
{
    "paper_id": "", 
    "abstract":[{}],
    "body_text": [{}],
    "TABREF0": "...caption1..."
    "TABREFN": "...captionN..."
    "table_num":N-1
}

'''
# read json file-->dict
def read_file(path,output_file):
    print("------------Loading json file------------")

    files = os.listdir(path)
    new_list = []
    for file in files:
        with open(path+file, "r") as f:
            for line in f:
                new_dict = {}
                sci_dict = json.loads(line)
                if is_dict(sci_dict,'ref_entries'):
                    #paper_id
                    new_dict['paper_id']= sci_dict['paper_id']
                    # abstract & body_text  (all)
                    new_dict['abstract']= sci_dict['abstract']
                    new_dict['body_text']= sci_dict['body_text']

                    # # abstract & body_text  (only text)
                    # abstact = sci_dict['abstract'][0]
                    # new_dict['abstract']= abstact['text']


                    # extract tables from ref_entries
                    new_dict,n = table_exist(sci_dict['ref_entries'],new_dict)
                    if n >0:        
                        new_dict['table_num']= n
                        new_list.append(new_dict)
                        print("The number of table of Paper "+ sci_dict['paper_id'] +" is ",n)

                    else:
                        print("Paper "+ sci_dict['paper_id'] +" has no table!")
    if len(new_list)>0:
        write_json(new_list,output_file)
    print("------------Finish Writing ------------")


# verify dict format-->True/False
def is_dict(dic_json, key):
    if isinstance(dic_json,dict): 
            for key in dic_json:

                # verify dic_json[key] is dict format
                if isinstance(dic_json[key],dict):
                    return True
    print("Paper "+ dic_json['paper_id'] +" is not JSON Foramt")
    return False

# english only -->True/False
def is_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def table_exist(json_dict,new_dict):
    key_list = json_dict.keys()
    i=0
    for key in key_list:
        # if "text"and "type" in json_dict[key].keys():
        # only table
        if "TAB"  in key:
            if json_dict[key]['type'] == "table":
                caption = json_dict[key]['text']
                if is_english(caption):
                    new_dict[key]= json_dict[key]['text']
                    i +=1
                else:
                    print("Paper "+ new_dict['paper_id'] +" is not English Paper!")
                    new_dict={}
                    return new_dict,0
    return new_dict,i

def write_json(dict_list,output_file):

    #list2json
    with open(output_file,"w") as f:
        json.dump(dict_list,f,indent=4)
        
'''
Input metadata file
{
    "paper_id": "...", 
    "title": "...", 
    "authors": [{}], 
    "abstract": ..., 
    "year": ..., 
    "arxiv_id": ..., 
    "venue": ..., 
}
Output 2. Body File
{
    "paper_id": "...", 
    "title": "...", 
    "authors": [{}], 
    "abstract": ..., 
    "year": ..., 
    "arxiv_id": ..., 
}
'''


if __name__ == "__main__":
    # test
    path = '../s2orc/data/pdf_parses/'
    output_pdffile = "pdfparse.json"
    read_file(path,output_pdffile)

    # output paper_id,abstrct,body_text,caption,num file
    PDFPARSE_DIR = 'full/pdf_parses/'
    output_pdffile = "pdfparse.json"
    read_file(path,output_pdffile)

    # output paper_id,authors,avix_id... file
    METADATA_DIR = 'full/metadata/'
    output_metafile = "metadata.json"
    