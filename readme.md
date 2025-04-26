# EasyBox——一个多功能工具箱

## 支持的功能

* PDF工具箱
  * 合并PDF✅
* 文档转换
  * PDF转Word
  * 网页转PDF
* 图片工具
  * 根据文件名修改图片拍摄时间

## 相关文章

* [Python合并多个PDF](https://blog.lc044.love/post/11)
* [PyQt5/PySide6自定义可拖拽列表组件](https://blog.lc044.love/post/12)
* [基于文件名修改图片的拍摄日期](https://blog.lc044.love/post/14)
* [基于 PyQt5/PySide6 实现分组列表滚动吸顶效果](https://blog.lc044.love/post/15)

## 运行截图

![img.png](doc/images/img.png)
![img.png](doc/images/img_2.png)
![img_1.png](doc/images/img_1.png)
![img_3.png](doc/images/img_3.png)

## 计划中功能

* PDF工具箱
  * 拆分PDF
  * PDF加密
  * 添加水印
  * 去除水印
* 文档转换
  * PDF转Word
  * PDF转图片
  * PDF转TXT
  * PDF转MarkDown
  * 图片转PDF
* 批量工具
  * 批量重命名
  * 图片批量改格式
  * 文档批量加水印
  * 批量替换文本
* 视频工具
  * 屏幕录制（没有分辨率限制）
  * 定时录制
  * 视频转GIF
  * 视频转avi
  * 视频转MP4

## 安装

```shell
git clone https://github.com/LC044/EasyBox.git
cd EaseBox
pip install -r requirements.txt
```

## 运行

```shell
python main.py
```

## 打包

```shell
pip install pyinstaller
pyinstaller main1.spec
```

## 证书

[AGPL3.0](./LICENSE)