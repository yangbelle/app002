from Base.Base import Base
from Page.pageElements import PageElements


class HomePage(Base):

    def __init__(self, driver):
        Base.__init__(self, driver)

    def click_my_btn(self):
        """点击首页我"""

        self.click_element(PageElements.home_my_btn_id)

    def close_update_window(self):
        # com.yunmall.lc:id/img_close
        try:
            self.click_element(PageElements.close_window_update)
        except Exception:
            return
