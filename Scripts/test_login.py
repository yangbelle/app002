import sys, os, pytest

from selenium.common.exceptions import TimeoutException

sys.path.append(os.getcwd())

from Base.getDriver import get_android_driver
from Base.Page import Page
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
# build_data('fail')


class Test_Login:

    def setup_class(self):
        """初始化driver和统一入口类"""
        self.driver = get_android_driver('com.yunmall.lc', 'com.yunmall.ymctoc.ui.activity.MainActivity')
        self.page_entrance = Page(self.driver)

    def teardown_class(self):
        """关闭驱动对象"""
        self.driver.quit()

    @pytest.fixture(autouse=True)
    def got_to_login(self):
        """进入登录页面，每个数据都需要依赖一次"""
        self.page_entrance.get_home_page().close_update_window()
        self.page_entrance.get_home_page().click_my_btn()
        self.page_entrance.get_choice_login_page().click_exits_account()

    def quit_login(self):
        """退出登录状态"""
        # 退出
        self.page_entrance.get_person_page().click_setting_btn()
        self.page_entrance.get_setting_page().logout('1')

    @pytest.mark.parametrize("case_num, name, pwd, exp_data", build_data('success'))
    def test_suc_login(self, case_num, name, pwd, exp_data):
        """
        预期成功用例
        :param case_num: 用例编号
        :param name: 用户名
        :param pwd: 密码
        :param exp_data: 预期结果
        :return:
        """
        # 执行login页面登录操作 若成功登录会跳转到个人中心页面personPage
        print(name, pwd)
        self.page_entrance.get_login_page().login(name, pwd)
        try:
            # 定位个人中心页面我的收藏元素
            # 1、定位成功
            elemtext = self.page_entrance.get_person_page().get_shoppingcart()
            try:
                # 断言成功
                assert elemtext == exp_data
            except AssertionError:
                # 截图
                self.page_entrance.get_person_page().get_screenshot_attach('断言失败')
                # 断言失败  ＃如果不手动断言失败，程序默认断言成功
                assert False
            finally:
                # 退出
                self.quit_login()

        # 2、定位失败
        except TimeoutException:
            # 查看是否找到登录元素
            # 1、找到了 说明登录失败
            # 关闭登录页面，返回首页
            # 断言失败
            try:
                self.page_entrance.get_login_page().is_exsit_login_btn()
                self.page_entrance.get_login_page().close_login()
            # 2、没找到  说明登录成功
            # 退出登录状态，返回首页
            except:
                # 退出
                self.quit_login()
            #
            assert False

    @pytest.mark.parametrize('case_num, name, pwd, toast, exp_data',build_data('fail'))
    def test_fail_login(self, case_num, name, pwd, toast, exp_data):
        """
        预期失败测试用例
        :param case_num: 用例编号
        :param name: 用户名
        :param pwd: 密码
        :param toast: toast 消息拼接语句
        :param exp_data: 预期结果
        :return:
        """
        print(name, pwd)
        self.page_entrance.get_login_page().login(name, pwd)
        try:
            # 定位toast消息元素
            toast_text = self.page_entrance.get_login_page().get_toast(toast)
            try:
                # 断言toast消息
                assert toast_text == exp_data
                print('1')
            except AssertionError:
                self.page_entrance.get_login_page().get_screenshot_attach('toast消息断言失败')
                assert False
                print('2')
        except TimeoutException:
            # 截图
            print('3')
            self.page_entrance.get_login_page().get_screenshot_attach('定位toast消息失败')
            assert False

        finally:
            try:
                print('5')
                # 断言登录按钮
                assert self.page_entrance.get_login_page().is_exsit_login_btn()
                # 关闭登录页面
                self.page_entrance.get_login_page().close_login()

            except AssertionError:
                # 退出登录状态
                print('6')
                self.quit_login()
                # 断言失败
                assert False
