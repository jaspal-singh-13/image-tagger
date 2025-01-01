# 🏷️ Image Tagger POC

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0089D6?logo=microsoft-azure)](https://azure.microsoft.com/products/cognitive-services/openai-service/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A powerful AI-driven image tagging solution powered by Azure OpenAI's vision capabilities, featuring a sleek Streamlit interface for effortless tag generation.

![Demo Screenshot](docs/demo-screenshot.png)

## ✨ Key Features

- 🤖 **AI-Powered Analysis**: Harnesses Azure OpenAI's advanced vision models
- 🎯 **Smart Tag Curation**: Customizable whitelist/blacklist system
- 🌐 **Modern Web Interface**: Built with Streamlit for seamless user experience
- 🔄 **Real-time Processing**: Instant tag generation and filtering
- 📋 **Tag Management**: Easy export of generated tags
- 🛡️ **Secure Handling**: Safe file processing and error management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API credentials
- Active Azure OpenAI deployment
- UV package manager (recommended)

### Setup

1. **Clone & Navigate**
```bash
git clone https://github.com/jaspal-singh-13/image-tagger.git
cd image-tagger
```

2. **Install Dependencies**

Using UV (Recommended):
```bash
uv sync
```

Using pip:
```bash
pip install -r requirements.txt
```

3. **Configure Environment**

Create a `.env` file:
```env
AZURE_ENDPOINT="your-azure-endpoint"
AZURE_API_KEY="your-api-key"
DEPLOYMENT_NAME="your-deployment-name"
API_VERSION="your-api-version"
```

4. **Launch Application**
```bash
streamlit run app.py
```

## 🎨 Usage Guide

1. Access the web interface at `http://localhost:8501`
2. Upload your image using the file picker
3. Adjust the temperature slider for tag generation control
4. Review generated tags
5. Download tags as needed

## 🗂️ Project Architecture

```
image-tagger/
├── script/
│   ├── 📱 app.py           # Streamlit interface
│   ├── 🎯 tagger.py        # Core tagging engine
│   ├── 💬 prompt.py        # AI prompts
│   ├── ⚙️ constants.py     # Configuration
│   └── 📋 tags_config.json # Tag definitions
├── 📝 requirements.txt     # Dependencies
├── 🔧 pyproject.toml      # Project metadata and dependencies
├── 🔒 uv.lock            # UV package lock file
├── 📖 README.md           # Documentation
└── 🔒 .env                # Credentials
```

## ⚙️ Advanced Configuration

### Tag Configuration

Customize `tags_config.json`:
```json
{
    "whitelist_tags": [
        "modern",
        "kitchen",
        "interior"
    ],
    "blacklist_tags": [
        "inappropriate",
        "offensive"
    ]
}
```

### Temperature Control

- **0.0**: Consistent, focused results
- **0.5**: Balanced creativity
- **1.0**: Maximum creativity

## 🔧 Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| API Connection Failed | Check Azure credentials in `.env` |
| No Tags Generated | Verify image format and size |
| Missing Dependencies | Run `uv sync` or check `requirements.txt` |

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🙋‍♂️ Support & Contact

- 📫 Report issues on our [Issue Tracker](https://github.com/jaspal-singh-13/image-tagger/issues)
- 📧 Email: work@four17.in

---
Made with ❤️ by the Team Oxima