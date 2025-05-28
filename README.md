# 政府留言板数据采集系统

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange)

## 主要功能
✅ 自动抓取指定官员留言板的公开数据  
✅ 智能翻页直至抓取完整数据集  
✅ 自动过滤重复数据（内存标记+DOM标记双重校验）  
✅ 异常处理机制保障程序稳定运行  
✅ 数据格式化存储为标准文本文件

## 技术特性
    A[初始化浏览器] --> B{新数据检测}
    B -->|存在| C[数据提取]
    B -->|不存在| D[终止程序]
    C --> E[数据清洗]
    E --> F[本地存储]
    F --> G[智能翻页]
    G --> B
快速开始
环境要求
bash
pip install selenium webdriver-manager
配置说明
# 修改chromedriver路径（第10行）
service = Service(r"您的/chromedriver路径")
# 设置目标URL（第13行）
driver.get("https://liuyan.people.com.cn/threads/list?fid=573")
运行程序
bash
python ceship.py
数据输出示例
text
问题标题：社区绿化改善建议
回复状态：已回复
留言ID：LY20231123001
留言时间：2023-11-23 14:30:00
留言内容：建议在XX小区增加乔木种植...
留言类型：城建管理
==============================
注意事项
⚠️ 确保chromedriver版本与浏览器一致
⚠️ 首次运行需修改代码中的chromedriver路径
⚠️ 网络不稳定时建议增加time.sleep时长
⚠️ 数据文件默认保存在程序同级目录
