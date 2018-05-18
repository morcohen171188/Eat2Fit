from operator import itemgetter
def parse_url_data(data):
    data_list = data.split('&')
    rest_name = data_list[0]
    user_data = data_list[1].split('=')
    user_id = user_data[1]
    return (rest_name, user_id)

def clean_string(string_data):
    string_data = string_data.replace('\r', '')
    string_data = string_data.replace('\n', '')
    return string_data

def get_top_5_dishes(result_list):
    newlist = sorted(result_list, key=lambda k: k)
    print (newlist)

if __name__ == "__main__":
    result_list = [{'chicken in butter': 0}, {'beef rice': 50}]
    print(result_list[0])
    get_top_5_dishes(result_list)