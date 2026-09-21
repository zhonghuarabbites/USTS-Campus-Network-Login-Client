# 苏州科技大学校园网登录器
<img width="700" height="607" alt="image" src="https://github.com/user-attachments/assets/2e7a0c47-afb1-4758-8b3a-48f20f6467cd" />

## 功能说明

- 一键登录校园网
- 支持多种运营商选择
- 保存账号密码（可选）
- 登录/注销功能

## 使用方法

1. 填写账号和密码
2. 选择运营商
3. 点击"登录"按钮
4. 需要注销时点击"注销"按钮

## 打包成exe

1. 安装Python 3.6+
2. 安装依赖：`pip install pyinstaller`
3. 运行打包脚本：`build.bat`
4. 在dist文件夹中找到生成的exe文件

## 运营商选项

- 校园用户 (@xyw)
- 校园电信 (@dx)
- 校园联通 (@lt)
- 校园移动 (无后缀)

## 文件说明

- `campus_login.py` - 主程序
- `campus_login.spec` - PyInstaller配置
- `build.bat` - 打包脚本
