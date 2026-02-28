# miniprogram-icon-downloader 技能使用指南

## 简介

`miniprogram-icon-downloader` 技能用于为微信小程序项目下载图标和图片，支持从 Icons8 API 搜索和下载图标，适用于 TabBar 和其他界面元素的图标下载。

## 基本用法

### 下载 TabBar 图标

```python
from .scripts.download_icon import download_icons

tabs = [
  { "name": "ai", "text": "AI创作", "search_query": "ai brain artificial intelligence" },
  { "name": "dev", "text": "开发工具", "search_query": "code programming developer" },
  { "name": "text", "text": "文本工具", "search_query": "text document editing" },
  { "name": "material", "text": "素材库", "search_query: "library collection folder" }
]

# 下载图标到指定的小程序项目路径
download_icons('path/to/your/mini-program', tabs)
```

### 自定义 TabBar 配置

```python
customTabs = [
  { 
    "name": "home", 
    "text": "首页", 
    "search_query": "home house main" 
  },
  { 
    "name": "profile", 
    "text": "我的", 
    "search_query": "user profile avatar" 
  }
]

# 使用自定义选项
download_icons('path/to/your/mini-program', customTabs, {
  "iconDir": "assets/icons",
  "states": ["normal"]
})
```

## 高级用法

### 下载自定义图标

```python
customIcons = [
  { "name": "settings", "search_query": "settings gear", "size": 64 },
  { "name": "camera", "search_query": "camera photo image", "size": 64 },
  { "name": "search", "search_query": "search find", "size": 64 }
]

download_icons('path/to/your/mini-program', customIcons, {
  "iconDir": "assets/icons",
  "states": ["normal"] # 只下载正常状态
})
```

### 搜索和下载图标

```python
from .scripts.download_icon import search_icons, download_single_icon

# 搜索图标
icons = search_icons('settings', 81, 'fluent', 3)
print('Found icons:', icons)

# 下载第一个结果
if len(icons) > 0:
  download_single_icon(icons[0]["url"], "settings", "path/to/your/mini-program")
```

## 图标配置

每个图标配置对象支持以下属性：

```javascript
{
  name: 'icon_name',           // 图标文件名前缀
  search_query: 'search term',  // Icons8 搜索查询
  text: 'Tab text',           // TabBar 文本（可选）
  size: 81,                   // 图标尺寸（默认：81）
  platform: 'fluent',         // 图标平台（默认：'fluent'）
  states: ['normal', 'active'] // 图标状态（默认：['normal', 'active']）
}
```

## 选项配置

```javascript
{
  iconDir: 'images',         // 图标目录（默认：'images'）
  states: ['normal', 'active'] // 图标状态（默认：['normal', 'active']）
}
```

## 图标尺寸规范

微信小程序推荐尺寸：
- **TabBar 图标**: 81x81 像素
- **导航图标**: 24x24 到 32x32 像素
- **操作图标**: 48x48 像素
- **大图标**: 128x128 像素

## 搜索技巧

使用这些通用方法来获得更好的图标搜索结果：
- 使用简单的描述性术语（例如 "home"、"user"、"settings"）
- 尝试功能性的动作词（例如 "search"、"download"、"edit"）
- 使用项目名称（例如 "phone"、"computer"、"car"）
- 如果第一次搜索没有结果，考虑同义词
- 考虑图标代表的概念
- 使用单词或短语的搜索词以获得最佳结果

## 错误处理

该技能会自动处理常见的错误情况：
- 图标搜索失败
- 下载过程中断
- 文件系统错误

如果某个图标无法下载，该技能会跳过并继续处理其他图标。

## 依赖要求

- **curl**: 必须在系统中可用
- **Node.js**: v14 或更高版本
- **Icons8 API 访问**: 通过 MCP 服务器
- **child_process**: 用于执行 curl
- **fs**: 用于文件系统操作
- **path**: 用于路径操作

## 注意事项

1. 确保目标目录有写入权限
2. 图标将保存在 `project_path/{iconDir}/` 目录下
3. 文件名遵循 `{name}-{state}.png` 模式
4. 技能自动处理正常和激活状态图标
5. 对于 TabBar，确保图标放置在正确的目录结构中
6. 支持自定义尺寸和平台

## 示例项目结构

```
your-mini-program/
├── images/
│   ├── ai.png
│   ├── ai-active.png
│   ├── dev.png
│   ├── dev-active.png
│   ├── text.png
│   ├── text-active.png
│   ├── material.png
│   └── material-active.png
└── app.json
```

## 故障排除

如果遇到问题：

1. 检查 curl 是否可用：`curl --version`
2. 确认项目路径是否正确
3. 验证网络连接
4. 检查目标目录的权限
5. 确保 Icons8 API 访问正常

---

**提示**: 对于生产环境，建议添加错误重试机制和适当的日志记录。