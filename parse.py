import re
from copy import copy
from typing import List, Dict, Tuple

import pandas as pd

from ios import load_sql, load_json


def table_prefix_to_real_name(table_name: str) -> str:
    return table_name


def get_schema_from_table_name(table_name):
    import random

    rand_num = random.randint(0, 4)
    if rand_num == 0:
        return pd.DataFrame(
            {
                "columns": ["c1", "c2", "c3"],
                "type": ["int", "string", "date"],
                "info": ['"info1"', '"info2"', '"info3"'],
            },
        )
    elif rand_num == 1:
        return pd.DataFrame(
            {
                "columns": ["c4", "c5", "SERVICE_ID"],
                "type": ["int", "string", "string"],
                "info": ['"info4"', '"info5"', '"info6"'],
            },
        )
    elif rand_num == 2:
        return pd.DataFrame(
            {
                "columns": ["c4", "c5", "SVC_ID"],
                "type": ["int", "string", "string"],
                "info": ['"info4"', '"info5"', '"info6"'],
            },
        )
    elif rand_num == 3:
        return pd.DataFrame(
            {
                "columns": ["c4", "c5", "PRFL_ID"],
                "type": ["int", "string", "string"],
                "info": ['"info4"', '"info5"', '"info6"'],
            },
        )
    elif rand_num == 4:
        return pd.DataFrame(
            {
                "columns": ["c4", "c5", "PROFILE_ID"],
                "type": ["int", "string", "string"],
                "info": ['"info4"', '"info5"', '"info6"'],
            },
        )


def add_table(quries: list[str]) -> Tuple[str, Dict[str, pd.DataFrame]]:
    pattern = re.compile(r'\bFROM\b\s+([^\s,]+)|\bJOIN\b\s+([^\s,]+)', re.IGNORECASE)
    matches = []
    for query in quries:
        table_names = [name for tpl in pattern.findall(query) for name in tpl if name]
        matches.extend(table_names)

    # New list to hold the modified matches after removing comments
    modified_matches = []

    # Iterate over each match, apply the substitution, and add it to the new list
    # find pattern2 that starts with first -- and the rest of the line
    pattern2 = re.compile(r'--.*')
    for match in matches:
        modified_match = pattern2.sub('', match)
        modified_match = modified_match.replace(")", "")
        # modified_match = modified_match.split(".")[-1].replace("`", "")
        modified_matches.append(modified_match)

    modified_matches = list(map(table_prefix_to_real_name, modified_matches))
    modified_matches = list(set(modified_matches))

    _modified_matches: List[str] = []
    for match in modified_matches:
        _match = match.replace("`", "").replace("`", "").replace(".", "_").strip()
        _match = _match.split(" ")[0]
        # _match = _match.split(".")[-1]
        _modified_matches.append(_match)
    _modified_matches = list(set(_modified_matches))

    schemas = dict(
        zip(
            _modified_matches,
            list(map(get_schema_from_table_name, _modified_matches)),
        )
    )
    out2 = ""
    for _match, schema in schemas.items():
        out = convert_dataframe_into_str(schema)
        out2 += _match + " {" + out + "}\n"

    out2 = out2.replace("\\n", "\t\n")

    return out2, schemas


def table_group_to_string(table_group: Dict[str, List[str]]):
    out = ""
    for relation, tables in table_group.items():
        for i in range(len(tables) - 1):
            for j in range(i + 1, len(tables)):
                out += tables[i] + " ||--o{ " + tables[j] + " : " + relation + "\n"
    return out.strip()


def add_relations(
    queries_paths: List[str],
    relations_path: str,
    tables_dict: Dict[str, pd.DataFrame],
):

    relations: List[List[str]] = load_json(relations_path) # FIXME

    table_group = {relation[0]: [] for relation in relations}
    for table_name, table_schema in tables_dict.items():
        for relation in relations:
            if table_schema["columns"].isin(relation).any():
                table_group[relation[0]].append(table_name)
    
    _relations = table_group_to_string(table_group)


    return _relations


def convert_dataframe_into_str(df: pd.DataFrame):
    return df.to_string(index=False, header=False) 


def parse_sqls_to_template(queries_paths: str, html_template: str, relations_path: str) -> str:
    html_template = copy(html_template)
    quries = []
    for query_path in queries_paths:
        query = load_sql(query_path)
        quries.append(query)

    table_str, tables_dict = add_table(quries)
    html_template = html_template.replace("{tables}", table_str)
    relations_str = add_relations(queries_paths, relations_path, tables_dict)
    html_template = html_template.replace("{relations}", relations_str)
    return html_template