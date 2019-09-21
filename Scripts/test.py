import sys, os
sys.path.append(os.getcwd())

from Base.getData import GetData


def build_data(tag):
    """

    :param tag:
    :return:
    """
    data_list_success = []
    data_list_fail = []
    data = GetData().get_yml_data('login.yml')
    for key in data:
        # 'success':  case_num, name, pwd, exp_data:
        case_num = key
        name = data.get(key).get('username')
        pwd = data.get(key).get('passwd')
        toast = data.get(key).get('toast')
        exp_data = data.get(key).get('exp_data')
        if tag == 'success' and not toast:  # 正向用例
            data_list_success.append((case_num, name, pwd, exp_data))
        elif tag == 'fail' and toast:
            data_list_fail.append((case_num, name, pwd, toast, exp_data))
    # print("data_list_success: ",data_list_success)
    # print("data_list_fail: ", data_list_fail)
    if tag == 'success':  # 正向用例
        return data_list_success
    else:
        return data_list_fail


# build_data('success')
build_data('fail')
