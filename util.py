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