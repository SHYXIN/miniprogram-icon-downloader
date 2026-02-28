---
name: miniprogram-icon-downloader
description: Use this skill to download icons and images for WeChat Mini Program projects. Search icons from Icons8 API and download them using curl or other tools. Supports TabBar icon download with 81x81 size specification.
alwaysApply: false
---

## When to use this skill

Use this skill for **downloading icons and images for WeChat Mini Program projects**.

**Use it when you need to:**
- Download TabBar icons for mini program
- Download images from Icons8 API
- Search and download icons with specific sizes
- Download multiple icon sets for different states (normal/active)
- Initialize new mini program projects with standard icon sets

**Do NOT use for:**
- Web projects → use web-specific icon download methods
- Native apps → use platform-specific download methods
- General file downloads not related to mini program icons

---

## Available Functions

### download_icons(project_path, icon_configs, options={})

Download icons for mini program projects with flexible configuration.

**Parameters:**
- `project_path`: Path to mini program project directory
- `icon_configs`: Array of icon configuration objects
- `options`: Configuration options

**Icon Configuration Object:**
```javascript
{
  name: 'icon_name',           // Icon filename prefix
  search_query: 'search term',  // Search query for Icons8
  text: 'Tab text',           // TabBar text (optional)
  size: 81,                   // Icon size (default: 81)
  platform: 'fluent',         // Icon platform (default: 'fluent')
  states: ['normal', 'active'] // Icon states to download (default: ['normal', 'active'])
}
```

**Options:**
```javascript
{
  icon_dir: 'images',         // Icon directory (default: 'images')
  naming convention: 'tab-{name}-{state}.png' // Filename pattern
}
```

**Example:**
```javascript
const icons = [
  { name: 'ai', search_query: 'ai brain artificial intelligence', text: 'AI创作' },
  { name: 'dev', search_query: 'code programming developer', text: '开发工具' },
  { name: 'text', search_query: 'text document editing', text: '文本工具' },
  { name: 'material', search_query: 'library collection folder', text: '素材库' }
];

await download_icons('d:/code_project/AI-work-proj/ai-work-mini/miniprogram', icons);
```

### search_icons(query, size=81, platform='fluent', amount=1)

Search for icons from Icons8 API.

**Parameters:**
- `query`: Search term for the icon
- `size`: Size of the icon in pixels (default: 81)
- `platform`: Icon platform/style (default: 'fluent')
- `amount`: Number of results to return (default: 1)

**Returns:**
Array of icon objects with URL and metadata.

**Example:**
```javascript
const icons = await search_icons('settings', 81, 'fluent', 3);
console.log(icons);
```

### download_icon(url, output_path)

Download a single icon from URL to specified path.

**Parameters:**
- `url`: URL of the icon
- `output_path`: Output file path

**Example:**
```javascript
const iconUrl = 'https://img.icons8.com/ios/100/8C8C8C/settings.png';
await download_icon(iconUrl, 'path/to/icons/settings.png');
```

---

## Installation

This skill uses curl for downloading files. Ensure curl is available in your environment.

```bash
# Install dependencies if needed
pip install requests
```

---

## Usage Examples

### Download TabBar icons for a mini program

```javascript
const { download_icons } = require('@codebuddy/skills/miniprogram-icon-downloader');

const tabs = [
  { name: 'ai', text: 'AI创作', search_query: 'ai brain artificial intelligence' },
  { name: 'dev', text: '开发工具', search_query: 'code programming developer' },
  { name: 'text', text: '文本工具', search_query: 'text document editing' },
  { name: 'material', text: '素材库', search_query: 'library collection folder' }
];

await download_icons('path/to/your/mini-program', tabs);
```

### Download custom icons with different sizes

```javascript
const { download_icons } = require('@codebuddy/skills/miniprogram-icon-downloader');

const customIcons = [
  { name: 'home', search_query: 'home house', size: 64 },
  { name: 'profile', search_query: 'user profile', size: 64 },
  { name: 'settings', search_query: 'settings gear', size: 64 }
];

await download_icons('path/to/your/mini-program', customIcons, {
  icon_dir: 'assets/icons',
  states: ['normal']
});
```

### Search and download icons manually

```javascript
const { search_icons, download_icon } = require('@codebuddy/skills/miniprogram-icon-downloader');

// Search for icons
const icons = await search_icons('camera', 81, 'fluent', 5);
if (icons.length > 0) {
  // Download first result
  await download_icon(icons[0].url, 'path/to/icons/camera.png');
}
```

---

## Icon Size Specifications

For WeChat Mini Program:

- **TabBar icons**: 81x81 pixels (recommended)
- **Navigation icons**: 24x24 to 32x32 pixels
- **Action icons**: 48x48 pixels
- **Large icons**: 128x128 pixels

---

## Search Tips

Use these general approaches for better icon search results:
- Use simple, descriptive terms (e.g., "home", "user", "settings")
- Try action words for functions (e.g., "search", "download", "edit")
- Use object names for items (e.g., "phone", "computer", "car")
- Consider synonyms if first search doesn't work
- Think about what the icon represents conceptually
- Use single words or short phrases for best results

---

## Error Handling

The skill handles common errors:
- Icon not found in search results
- Download failures
- File system errors

If an icon cannot be downloaded, the skill will skip it and continue with others.

---

## Dependencies

- **curl**: Must be available in the system
- **Node.js**: v14 or higher
- **Icons8 API access**: Through MCP server
- **child_process**: For executing curl
- **fs**: For file system operations
- **path**: For path manipulation

---

## Notes

- All icons are downloaded to `project_path/{icon_dir}/` directory
- Icon filenames follow the pattern: `{name}-{state}.png`
- The skill automatically handles both normal and active state icons
- For TabBar, ensure icons are placed in the correct directory structure
- Supports custom icon sizes and platforms

---

## Best Practices

1. **Consistent naming**: Use clear, descriptive icon names
2. **Standard sizes**: Use 81x81 for TabBar, 24x24 for navigation
3. **Color consistency**: Choose icons that match your design system
4. **Error handling**: Implement proper error handling in production
5. **Caching**: Consider caching downloaded icons for repeated use

---