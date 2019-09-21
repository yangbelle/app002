from Base.Base import Base
from Page.pageElements import PageElements


class LoginPage(Base):

    def __init__(self, driver):
        Base.__init__(self, driver)

    def login(self, account, passwd):
        """
        登录
        :param account: 账号
        :param passwd: 密码
        :return:
        """

        # 输入账号
        self.send_element(PageElements.login_account_id, account)
        # 输入密码
        self.send_element(PageElements.login_passwd_id, passwd)
        # 点击登录按钮
        self.click_element(PageElements.login_logon_btn_id)

    def is_exsit_login_btn(self):
        """查看登录页面是否存在登录按钮"""
        try:
            return self.get_element(PageElements.login_logon_btn_id)
        except:
            return False

    def close_login(self):
        """点击关闭登录页面"""
        self.click_element(PageElements.login_logo_exit)


