# coding: utf-8
#

import uiautomator2 as u2
import time
import pytest
import adbutils
import allure
import inspect


def setup_function(fn):
    source = inspect.getsource(fn)
    allure.attach(source, "Source code", allure.attachment_type.TEXT)


def test_login():
    print("Everything is going")


@pytest.fixture(scope="session")
def device():
    d = u2.connect()
    d.xpath.when("服务条款和隐私政策提示").when("同意").click()
    d.xpath.when("拒绝").when("允许").click()
    # d.xpath.when("@com.netease.cloudmusic:id/aug").click()  # 同意

    d.xpath.watch_background(interval=1)
    d.xpath.global_set("timeout", 30)
    return d


@pytest.fixture
def d(device):
    _d = device
    _d.app_clear("com.netease.cloudmusic")
    _d.app_start("com.netease.cloudmusic")

    _d(text="立即体验").wait(timeout=20)
    time.sleep(1)
    _d.click(0.261, 0.96)
    _d(text="立即体验").click()

    _adb = adbutils.adb.device(_d.serial)
    v = _adb.screenrecord()
    yield _d
    v.stop_and_pull("v.mp4")
    allure.attach.file("v.mp4")


def test_每日歌曲(d: u2.Session):
    d.xpath('//*[@text="每日推荐"]').click()
    d.xpath('播放全部').click()
    assert d.xpath('//*[@content-desc="分享"]').wait()
    assert d.xpath("播放暂停").exists
    assert d.xpath("下一首").exists


def test_搜索播放音乐(d: u2.Session):
    d.xpath('//*[@content-desc="搜索"]').click()
    d.xpath(
        '//*[@resource-id="com.netease.cloudmusic:id/search_src_text"]').click()  # 搜索框
    d.send_keys("水手", clear=True)
    d.send_action("search")
    d.xpath(
        '//*[@resource-id="com.netease.cloudmusic:id/a0w" and @text="水手"]').click()
    assert d.xpath("播放暂停").wait()
