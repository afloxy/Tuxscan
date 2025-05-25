# 🔍 TuxScan - Internal Security Scanner

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-orange)](https://pypi.org/project/tuxscan/)

TuxScan is a powerful yet lightweight security scanner designed to help developers and security professionals identify potential sensitive information in their codebase. It recursively scans directories and files to detect various types of sensitive data, helping maintain security best practices and prevent accidental exposure of confidential information.

## ⚠️ Important Disclaimer

**ETHICAL USE ONLY**

This tool is provided for educational and ethical security testing purposes only. By using this tool, you agree to:

1. Use it only on systems and codebases you own or have explicit permission to test
2. Not use it for any malicious or unauthorized security testing
3. Not use it to violate any laws or regulations
4. Not use it to compromise or damage any systems

**The author(s) of this tool are not responsible for any misuse or damage caused by this tool. Users are solely responsible for ensuring they have proper authorization before using this tool on any system.**

## ✨ Features

- 🔑 **Credential Detection**
  - Hardcoded passwords and usernames
  - API keys and secrets
  - Authentication tokens
  - Common default credentials

- 🌐 **Network Information**
  - IP addresses
  - URLs and endpoints
  - API endpoints

- 👤 **PII Detection**
  - Email addresses
  - Aadhaar numbers
  - PAN numbers
  - Other sensitive personal information

- 📊 **Reporting**
  - Beautiful HTML reports
  - Detailed findings with line numbers
  - Scan summary and statistics
  - Organized reports directory

- ⚙️ **Customization**
  - Configurable ignore patterns
  - Custom output file naming
  - Extensible pattern matching

## 🚀 Quick Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tuxscan.git
cd tuxscan
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

That's it! TuxScan is now installed and ready to use from anywhere in your system.

## 💻 Usage

### Basic Scan
```bash
tuxscan /path/to/scan
```

### Scan with Ignore Patterns
```bash
tuxscan /path/to/scan --ignore "*.git/*" "venv/*" "node_modules/*"
```

### Custom Report Name
```bash
tuxscan /path/to/scan --output custom_report.html
```

## 📝 Report Generation

TuxScan generates detailed HTML reports in the following locations:

1. **Default Location**: 
   - Reports are stored in the `reports` directory
   - Each report is named with timestamp: `report_YYYY-MM-DD_HH-MM-SS.html`

2. **Custom Location**:
   - Use `--output` flag to specify custom report name and location
   - Example: `tuxscan /path/to/scan --output /custom/path/report.html`

### Report Contents
Each report includes:
- Scan timestamp and duration
- Total number of findings
- Patterns checked
- Detailed findings with:
  - File paths
  - Line numbers
  - Matched content
  - Pattern type
  - Severity level

## 🔧 Configuration

### Ignore Patterns
You can specify patterns to ignore during scanning:
- File patterns: `*.log`, `*.tmp`
- Directory patterns: `venv/*`, `node_modules/*`
- Specific files: `config.json`

### Output Options
- Default: Generates timestamped reports in `reports` directory
- Custom: Specify custom output filename with `--output` option

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Inspired by various security scanning tools and best practices
- Built with Python's powerful regex and file handling capabilities 
