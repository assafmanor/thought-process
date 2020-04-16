from datetime import datetime


def print_lists_with_padding(lists):
	col_width_lst = [(max([len(str(col[i])) for col in lists]) + 3) for i in range(len(lists[0]))]
	for lst in lists:
		print("".join(str(item).ljust(col_width_lst[i]) for i, item in enumerate(lst)))

def print_listed_dict(d):
    keys_width = max([len(str(key)) for key in d.keys()]) + 3
    for key,val in d.items():
        print(f'{str(key).ljust(keys_width)}{val}')

def make_dict_into_lists(d):
    lists = []
    lists.append(list(d.keys()))
    lists.append(list(d.values()))
    return lists


def make_list_of_dicts_into_lists(lst):
    lists = []
    lists.append(list(lst[0].keys()))
    for d in lst:
        lists.append(list(d.values()))
    return lists


def format_timestamp(data_dict, key, dt_format):
    ts = data_dict[key]
    data_dict[key] = datetime.fromtimestamp(ts).strftime(dt_format)