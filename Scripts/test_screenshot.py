import allure
class TestSave:
    def test001(self):
        with open('./imgs/screenshot01.png','rb') as f:
            allure.attach('截图',f.read(),allure.attach_type.PNG)
