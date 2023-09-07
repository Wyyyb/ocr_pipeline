# PDF 转文本信息 Pipeline

这个项目提供了一个将PDF文件转换为文本信息的pipeline。

## 运行

要启动pipeline，请运行以下命令：
\`\`\`bash
python trans_pdf_to_txt.py
\`\`\`

## 贡献

我们目前需要完成文本的后处理部分，以使OCR的文本结果更加干净。主要任务是实现`postprocess/post_process_api.py`中的`process`函数。

### 任务描述

- **输入**：一段OCR结果文本。
- **输出**：这段文本的清洗结果，类型也是一段文本。

如果你有兴趣帮助我们实现这部分功能，欢迎提交pull request！

## 测试

`post_process_api.py`中已经包含了单元测试，你可以通过以下命令直接运行单元测试：

\`\`\`bash
python postprocess/post_process_api.py
\`\`\`

同时，你也可以运行以下命令进行系统测试：

\`\`\`bash
python trans_pdf_to_txt.py
\`\`\`
