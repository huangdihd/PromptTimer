# PromptTimer

一个在预设提示词中添加时间信息以优化大模型聊天体验的插件

## 安装

配置完成 [LangBot](https://github.com/RockChinQ/LangBot) 主程序后即可到插件管理页面安装  
或查看详细的[插件安装说明](https://docs.langbot.app/plugin/plugin-intro.html#%E6%8F%92%E4%BB%B6%E7%94%A8%E6%B3%95)

## 使用
插件安装后,会自动在预设提示词后面加一条:
```json
{
  "role": "system",
  "content": "现在的时间是:<时间>, 时区为<当前时区>, 距离上次对话已经过去了<自消息发出到准备调用调用模型的间隔,若没发过消息则此分句不会存在>秒"
}
```

以上对话间隔信息会根据`session_id`分别储存

