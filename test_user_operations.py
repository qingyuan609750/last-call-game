import random
import string
import allure
from allure import attach
import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout


def generate_unique_username():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"yangjian_{suffix}"


@allure.feature("用户管理")
@allure.story("登录及用户CRUD操作")
class TestUserOperations:

    def generate_unique_username(self):
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return f"yangjian_{suffix}"

    @allure.step("登录系统")
    def login(self, page: Page):
        page.goto("http://localhost:8088")
        page.wait_for_selector('input[name="username"]', timeout=10000)

        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', '123456')
        page.click('#rememberme')
        page.click('#btnSubmit')

        page.wait_for_selector('//*[@id="side-menu"]/li[3]/a', timeout=10000)
        assert "首页" in page.title() or "若依" in page.title(), "登录失败"
        attach("登录成功", name="登录状态", attachment_type=allure.attachment_type.TEXT)

    @allure.step("进入用户管理页面")
    def enter_user_management(self, page: Page):
        page.click('//*[@id="side-menu"]/li[3]/a')
        page.click('//*[@id="side-menu"]/li[3]/ul/li[1]/a')

        frame = page.frame_locator("#iframe2")
        frame.wait_for_selector("//input[@name='loginName']", timeout=10000)
        attach("已进入用户管理页面", name="页面状态", attachment_type=allure.attachment_type.TEXT)

    @allure.step("新增用户: {username}")
    def add_user(self, page: Page, username: str):
        page.click('//*[@id="toolbar"]/a[1]')

        frame = page.frame_locator('//*[@id="content-main"]/iframe[3]')
        attach("进入新增用户页面", name="页面状态", attachment_type=allure.attachment_type.TEXT)

        frame.fill('//*[@id="form-user-add"]/div[1]/div[1]/div/div/input', username)
        frame.fill('//input[@placeholder="请输入登录账号"]', username)

        frame.click('//*[@id="treeName"]')

        dept_frame = page.frame_locator('//iframe[contains(@src,"selectDeptTree")]')
        dept_frame.click('//*[@id="tree_3_span"]')

        page.click('//div[@class="layui-layer-btn"]/a[1]')
        attach("选择部门完成", name="操作状态", attachment_type=allure.attachment_type.TEXT)

        frame.fill('/html/body/div[1]/form/div[3]/div[1]/div/div/input', '123456')
        frame.click('/html/body/div[2]/div/button[1]')
        attach(f"保存用户成功: {username}", name="操作状态", attachment_type=allure.attachment_type.TEXT)

    @allure.step("编辑用户: {username}")
    def edit_user(self, page: Page, username: str):
        frame = page.frame_locator("#iframe2")
        frame.fill("//input[@name='loginName']", username)
        frame.click('//*[@id="user-form"]/div/ul/li[5]/a[1]')
        page.wait_for_timeout(1000)

        frame.click("//input[@name='btSelectItem']")
        attach("勾选用户", name="操作状态", attachment_type=allure.attachment_type.TEXT)

        page.click('//a[contains(@onclick,"edit")]')

        edit_frame = page.frame_locator('//*[@id="content-main"]/iframe[3]')
        edit_frame.fill("//input[@name='userName']", f'{username}_修改')
        edit_frame.click('/html/body/div[2]/div/button[1]')
        attach("修改用户成功", name="操作状态", attachment_type=allure.attachment_type.TEXT)

    @allure.step("删除用户: {username}")
    def delete_user(self, page: Page, username: str):
        frame = page.frame_locator("#iframe2")
        frame.fill("//input[@name='loginName']", username)
        frame.click('//*[@id="user-form"]/div/ul/li[5]/a[1]')
        page.wait_for_timeout(1000)

        frame.click("//input[@name='btSelectItem']")
        attach("勾选用户准备删除", name="操作状态", attachment_type=allure.attachment_type.TEXT)

        page.click('//a[contains(@onclick,"remove")]')
        page.click('a.layui-layer-btn0')
        attach("删除用户成功", name="操作状态", attachment_type=allure.attachment_type.TEXT)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("测试登录及用户增删改操作")
    def test_login_and_user_operations(self, page: Page):
        unique_username = self.generate_unique_username()
        attach(f"生成的用户名: {unique_username}", name="测试数据", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤1: 登录系统"):
            self.login(page)

        with allure.step("步骤2: 进入用户管理页面"):
            self.enter_user_management(page)

        with allure.step("步骤3: 新增用户"):
            self.add_user(page, unique_username)
            page.wait_for_timeout(2000)

        with allure.step("步骤4: 编辑用户"):
            self.edit_user(page, unique_username)
            page.wait_for_timeout(2000)

        with allure.step("步骤5: 删除用户"):
            self.delete_user(page, unique_username)
