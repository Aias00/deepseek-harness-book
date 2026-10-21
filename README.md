# 从零认识 DeepSeek Harness

面向小白的中文工程导读，包含 12 章正文、术语表、资料索引和自检题，约 1 万汉字。介绍项目用途、任务流程、插件协作、工程目录和排错方法。

- [在线阅读](https://aias00.github.io/deepseek-harness-book/)
- [下载 EPUB](https://aias00.github.io/deepseek-harness-book/deepseek-harness-book.epub)
- [阅读书稿](DeepSeek-Harness-小白入门.txt)

在线版支持手机阅读、章节跳转、系统深色模式和浏览器页面查找，无外部脚本依赖。EPUB 可导入 Apple Books、Calibre 等阅读器。

## 内容与来源

本书依据 2026-10-20 的 DeepSeek Harness 工作区编写，所见根包版本为 `0.2.1-rc.2`，属于独立编写的非官方工程导读。

工程与参考资料来自 [DeepSeek-AI/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)。原工程版权与 MIT 许可见 [LICENSE](LICENSE)。本仓库新增书稿、页面与脚本同样采用 MIT 许可。

书中启动指引来自工程文档，本次编写未启动完整应用、未调用真实模型 API。工程处于开发者预览阶段，实际行为请以所使用版本的官方资料为准。

## 更新与生成

安装 Python 3 与 Pandoc 后，在本仓库根目录运行：

```sh
python3 build.py
python3 build_site.py
```

`build.py` 生成并检查 EPUB，`build_site.py` 生成 `docs/` 在线版及下载文件。书稿为 `DeepSeek-Harness-小白入门.txt`，采用 Markdown 内容格式；网页模板与样式分别为 `site-template.html` 和 `site.css`。

GitHub Pages 从 `main` 分支的 `/docs` 发布。修改书稿后重新执行上述生成命令，并将生成结果一起提交。

## 验证

EPUB 检查覆盖 ZIP、XML、资源声明、章节导航、阅读顺序、内部链接和封面。检查结果见 `validation.json`。最初编写环境未安装 Java，未执行 EPUBCheck。
