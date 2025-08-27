# NeuroOS - Human-First, Offline OS Agent

**Samsung EnnovateX 2025 AI Challenge Submission by Team NeuroKernels**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Cross Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()
[![Offline First](https://img.shields.io/badge/offline-first-green.svg)]()
[![Open Source](https://img.shields.io/badge/license-MIT-blue.svg)]()

## Overview

NeuroOS is an OS-native agent designed to provide seamless voice and text control over desktop environments. Unlike traditional chatbot overlays, NeuroOS integrates directly with operating system primitives to offer genuine system-level automation while maintaining complete offline functionality and user privacy.

---

## Table of Contents

- [Approach & Uniqueness](#approach--uniqueness)
- [Technical Stack](#technical-stack)
- [Architecture Overview](#architecture-overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Advanced Configuration](#advanced-configuration)
- [Technical Implementation](#technical-implementation)
- [Performance Metrics](#performance-metrics)
- [Contributing](#contributing)

---

## Approach & Uniqueness

### Problem Statement

Current AI assistants suffer from several critical limitations:

- **Cloud Dependency**: Require constant internet connectivity for processing
- **Limited System Integration**: Cannot deeply interact with operating system components
- **Privacy Concerns**: Transmit sensitive voice and usage data to external servers
- **High Latency**: Network round-trips introduce delays in command execution
- **Platform Inconsistency**: Different behavior and capabilities across operating systems

### Solution Architecture

NeuroOS addresses these challenges through a fundamentally different approach:

**OS-Native Integration**
- Direct interface with operating system primitives across macOS, Linux, and Windows
- Platform-specific adapters utilizing AppleScript, xdg-open, and PowerShell
- Deep system integration enabling control of applications, files, notifications, and system settings

**Single-File Architecture**
- Entire system contained in `multi.py` for simplified deployment
- Self-contained dependencies management
- Consistent behavior across platforms with minimal configuration

**Offline-First Design**
- All processing including speech-to-text, natural language understanding, and orchestration occurs locally
- No external API calls or cloud dependencies
- Immediate response times with zero network latency

**Multi-Modal Interface**
- Voice and text input with equal feature parity
- Accessibility-first design principles
- Support for users with varying interaction preferences

**Workspace Orchestration**
- Multi-application workflow automation through declarative configurations
- State management across application sessions
- Complex task automation through simple voice commands

### Key Differentiators

1. **True Offline Operation**: Complete functionality without internet connectivity after initial setup
2. **System-Level Integration**: Direct OS primitive access rather than application-level automation
3. **Privacy by Design**: Zero data transmission to external services
4. **Resource Efficiency**: Optimized for low-power devices including Raspberry Pi 5
5. **Developer-Friendly**: Single-file deployment with extensive customization options
6. **Enterprise Ready**: Professional workflow automation capabilities

---

## Technical Stack

### Core Runtime
- **[Python 3.9+](https://www.python.org/)** - Primary implementation language with cross-platform compatibility
- **[faster-whisper](https://github.com/SYSTRAN/faster-whisper)** - Optimized local speech-to-text processing using OpenAI Whisper models
- **[sounddevice](https://python-sounddevice.readthedocs.io/)** - Cross-platform audio input/output with low-latency streaming
- **[webrtcvad](https://github.com/wiseman/py-webrtcvad)** - Voice activity detection using Google WebRTC algorithms
- **[NumPy](https://numpy.org/)** - Numerical computing for audio processing and signal analysis

### Desktop Integration
- **[pyautogui](https://pyautogui.readthedocs.io/)** - Cross-platform GUI automation and screen interaction
- **[pyperclip](https://pypi.org/project/pyperclip/)** - Clipboard management for text capture and routing
- **[plyer](https://github.com/kivy/plyer)** - Cross-platform access to native APIs for notifications and system features

### Language Models (Optional)
- **[Transformers](https://github.com/huggingface/transformers)** - State-of-the-art language model inference framework
- **[PyTorch](https://pytorch.org/)** - Deep learning framework for model execution
- **[Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)** - Lightweight instruction-following model for Q&A
- **[FLAN-T5-Base](https://huggingface.co/google/flan-t5-base)** - Text-to-text generation model for summarization

### System Integration
- **macOS**: `osascript` (AppleScript execution), `open` (application launching)
- **Linux**: `xdg-open` (standard application launching), `notify-send` (desktop notifications), `wmctrl` (window management)
- **Windows**: `start` (application launching), PowerShell (system automation), Windows API integration

---

## Architecture Overview

### System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                     │
├─────────────────────┬───────────────────────────────────────────┤
│   Voice Input       │              Text Input                   │
│   (Microphone)      │              (CLI/GUI)                    │
└─────────────────────┴───────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Input Processing Layer                       │
├─────────────────────┬───────────────────────────────────────────┤
│  Speech-to-Text     │         Text Preprocessing                │
│  (faster-whisper)   │         (Normalization)                   │
└─────────────────────┴───────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Intent Parser Layer                          │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   Regex Patterns    │   Fuzzy Matching    │   LLM Fallback      │
│   (Exact matches)   │   (Typo tolerance)  │   (Complex queries) │
└─────────────────────┴─────────────────────┴─────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Planning Layer                              │
├─────────────────────┬───────────────────────────────────────────┤
│  Action Sequencing  │         Context Management                │
│  (Step generation)  │         (State tracking)                  │
└─────────────────────┴───────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Middleware Layer                              │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   File Operations   │   Context Storage   │   Inter-app Comm    │
│   (Path resolution) │   (Session state)   │   (Data routing)    │
└─────────────────────┴─────────────────────┴─────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  OS Adapter Layer                               │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   macOS Adapter     │   Linux Adapter     │   Windows Adapter   │
│   (AppleScript)     │   (xdg-open)        │   (PowerShell)      │
└─────────────────────┴─────────────────────┴─────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   System Execution Layer                        │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   Applications      │   File System       │   System Services   │
│   (Launch/Control)  │   (CRUD operations) │   (Notifications)   │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

### Voice Processing Pipeline

```
Audio Input → VAD → Segmentation → Preprocessing → Whisper → Text Output
     ↑         ↑         ↑             ↑            ↑          ↑
sounddevice webrtcvad  Silence    16kHz Resample  Model    Confidence
                       Detection                  Inference  Scoring
```

### Intent Resolution Workflow

```
Raw Text → Normalization → Pattern Matching → Fuzzy Matching → LLM Fallback → Intent
    ↑           ↑              ↑                 ↑                ↑           ↑
Input Text   Lowercase,     Regex Patterns   Levenshtein      Language     Structured
             Punctuation   (High confidence) Distance        Model        Command
```

---

## Core Features

### Application Control

**Basic Operations**
- Launch single or multiple applications with voice commands
- Switch between running applications
- Close applications and manage windows
- Control application-specific functions

```bash
# Voice commands examples:
"open chrome"
"open vscode and terminal"
"switch to spotify" 
"close all chrome windows"
```

**Workspace Management**
- Create and save complex multi-application layouts
- Restore entire working environments with a single command
- Manage different workspaces for various tasks
- Automatic application positioning and sizing

```bash
# Create workspace
"open vscode and chrome and terminal"
"save workspace development"

# Restore workspace
"open workspace development"
```

### Content Routing and Capture

**Inter-Application Communication**
- Route selected text between applications
- Send content to notes, reminders, or email
- Search selected text on the web
- Copy and paste operations with context

```bash
# Select text in any application, then:
"send selection to notes"
"email selection to team@company.com"
"search this on stackoverflow"
```

**Smart Clipboard Management**
- Enhanced clipboard functionality with history
- Context-aware paste operations
- Cross-application data transfer

### Time Management and Productivity

**Note Taking System**
- Create quick notes with voice commands
- Append to existing notes by name
- Organize notes by categories
- Search and retrieve notes efficiently

```bash
"take note: Meeting with client at 3 PM"
"add review code to note TODO"
"show all notes containing project"
```

**Reminder System**
- Set reminders with relative or absolute timing
- Voice-activated reminder creation
- System notifications for scheduled tasks
- Recurring reminder support

```bash
"remind me in 20 minutes to take a break"
"remind me at 3:30 PM to call the client"
"remind me every day at 9 AM to check emails"
```

### AI-Powered Operations (Optional)

**Question Answering**
- Offline natural language question processing
- Technical explanations and documentation lookup
- Code analysis and explanation
- General knowledge queries

```bash
"ask what is the difference between a process and a thread"
"ask how does HTTP authentication work"
"explain this selected code"
```

**Text Processing**
- Summarize selected text or articles
- Explain complex technical content
- Analyze code for potential issues
- Generate documentation from code

```bash
# Select text, then:
"summarize selection"
"explain this function"
"find issues in this code"
```

---

## Installation

### Prerequisites

**System Requirements:**
- **Operating System**: macOS 10.14+, Ubuntu 18.04+, Windows 10+
- **Python**: Version 3.9 or higher
- **Memory**: 4 GB RAM (8 GB recommended)
- **Storage**: 1 GB available space
- **Audio**: Microphone input capability

### Installation Steps

```bash
# 1. Create and activate virtual environment
python -m venv neuroos-env
source neuroos-env/bin/activate  # Windows: neuroos-env\Scripts\activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install core dependencies
pip install faster-whisper==0.10.0
pip install sounddevice==0.4.6
pip install numpy==1.24.3
pip install webrtcvad==2.0.10

# 4. Install desktop integration
pip install pyautogui==0.9.54
pip install pyperclip==1.8.2
pip install plyer==2.1.0

# 5. Install optional AI dependencies
pip install transformers==4.35.2
pip install torch==2.1.0
pip install sentencepiece==0.1.99

# 6. Clone NeuroOS
git clone https://github.com/neurokernels/neuroos.git
cd neuroos

# 7. Configure environment (optional)
export NEUROOS_WHISPER_SIZE=tiny.en
export NEUROOS_WHISPER_COMPUTE=int8
export NEUROOS_TTS=1
export NEUROOS_HF_MODEL="Qwen/Qwen2.5-0.5B-Instruct"

# 8. Launch NeuroOS
python multi.py
```

### Platform-Specific Setup

**macOS Configuration**
```bash
# Install system dependencies
brew install portaudio

# Grant microphone permissions
# System Settings → Privacy & Security → Microphone → Terminal
```

**Linux Configuration**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3-dev portaudio19-dev libasound2-dev
sudo apt install -y xdg-utils wmctrl notify-send
```

**Windows Configuration**
```powershell
# Ensure microphone permissions are granted
# Settings → Privacy → Microphone → Allow desktop apps
```

### Verification

```bash
# Test basic functionality
python multi.py --test

# Test audio input
python multi.py --test-audio

# Start debug mode
python multi.py --debug
```

---

## Usage Examples

### Basic Voice Setup

```bash
# Launch NeuroOS
python multi.py

# List available microphones
> voice devices
# Output: Available audio devices:
# 0: Built-in Microphone (2 channels)
# 1: USB Headset (1 channel)

# Start voice recognition
> voice start 0

# Test voice recognition
> voice test
# Speak: "This is a test"
# Output: Recognized: "This is a test" (confidence: 0.89)
```

### Application Control Examples

```bash
# Single application launch
"open calculator"
"open google chrome"
"open visual studio code"

# Multiple application launch
"open chrome and terminal"
"open vscode and spotify and notes"

# Application management
"close chrome"
"switch to terminal"
"minimize all windows"
"show desktop"
```

### Workspace Orchestration

```bash
# Development workspace
"open vscode and terminal and chrome"
"arrange windows"
"save workspace coding"

# Research workspace  
"open safari and notes and calculator"
"save workspace research"

# Load existing workspace
"open workspace coding"
"load workspace research"
```

### Content Management

```bash
# Note-taking workflow
"take note: Team meeting scheduled for tomorrow"
"add fix login bug to note TODO"
"show all notes"
"search notes for meeting"

# Content routing
# First select text in any application:
"send selection to notes"
"add selection to note Project Ideas" 
"email selection to john@company.com subject Research Data"
```

### Time Management

```bash
# Reminder system
"remind me in 15 minutes to stretch"
"remind me at 2:30 PM to join the meeting"
"remind me every Monday at 10 AM for team standup"

# Task scheduling
"schedule review code for tomorrow"
"add call client to today's tasks"
```

### AI-Powered Analysis

```bash
# Question answering
"ask what is a mutex in programming"
"ask how does OAuth 2.0 work"
"ask explain the difference between git merge and rebase"

# Code analysis (select code first)
"explain this function"
"find potential issues in selection"
"suggest improvements for this code"

# Text processing (select text first)
"summarize selection"
"explain this paragraph in simple terms"
"translate selection to Spanish"
```

---

## Advanced Configuration

### Voice Recognition Tuning

```bash
# Model configuration
export NEUROOS_WHISPER_SIZE=small.en     # tiny.en, small.en, medium.en
export NEUROOS_WHISPER_COMPUTE=float16   # int8, float16, float32

# Audio processing
export NEUROOS_VAD_MODE=2                # 0-3, higher = more sensitive
export NEUROOS_SILENCE_DURATION=1.5      # seconds of silence before processing
export NEUROOS_MAX_RECORDING_TIME=30     # maximum recording duration
```

### Language Model Configuration

```bash
# Enable AI features
export NEUROOS_ENABLE_LLM=1
export NEUROOS_HF_MODEL="Qwen/Qwen2.5-0.5B-Instruct"

# Model performance
export NEUROOS_LLM_MAX_TOKENS=256
export NEUROOS_LLM_TEMPERATURE=0.7
export TOKENIZERS_PARALLELISM=false
```

### System Integration Settings

```bash
# Text-to-speech feedback
export NEUROOS_TTS=1
export NEUROOS_TTS_RATE=200              # words per minute

# Notification settings
export NEUROOS_NOTIFICATIONS=1
export NEUROOS_NOTIFICATION_TIMEOUT=5000 # milliseconds

# Debug and logging
export NEUROOS_DEBUG=1
export NEUROOS_LOG_LEVEL=INFO
```

### Custom Command Configuration

```python
# Add to multi.py configuration section
CUSTOM_INTENTS = {
    "start focus mode": [
        ("close_app", "slack"),
        ("close_app", "discord"), 
        ("enable_dnd", None),
        ("play_focus_music", None)
    ],
    "end work day": [
        ("save_all_documents", None),
        ("close_all_apps", None),
        ("system_sleep", None)
    ]
}

# Workspace templates
WORKSPACE_TEMPLATES = {
    "development": {
        "apps": ["code", "terminal", "chrome"],
        "urls": ["https://github.com", "https://stackoverflow.com"],
        "layout": "tiled"
    },
    "design": {
        "apps": ["figma", "photoshop", "chrome"],
        "layout": "custom",
        "positions": {"figma": (0, 0, 800, 600)}
    }
}
```

---

## Technical Implementation

### File Structure

```
multi.py                           # Main implementation file
├── Configuration Classes
│   ├── NeuroOSConfig             # System configuration
│   └── Intent                    # Command structure
├── Core Engine Classes  
│   ├── VoiceEngine               # Audio processing
│   ├── LLMEngine                 # Language models
│   └── WorkspaceManager          # Multi-app orchestration
├── Processing Classes
│   ├── IntentParser              # Command interpretation
│   └── ActionPlanner             # Task sequencing
├── Platform Adapters
│   ├── OSAdapter (Abstract)      # Cross-platform interface
│   ├── MacAdapter               # macOS implementation
│   ├── LinuxAdapter             # Linux implementation
│   └── WindowsAdapter           # Windows implementation
└── Main Orchestrator
    └── NeuroOS                  # Primary coordinator
```

### Supported Intent Categories

```python
# Application control
Intent(action="open_app", target="chrome", parameters={})
Intent(action="open_workspace", target="development", parameters={})
Intent(action="close_app", target="spotify", parameters={})

# Content management  
Intent(action="send_selection", target="notes", parameters={})
Intent(action="take_note", target="default", parameters={"text": "content"})
Intent(action="add_to_note", target="TODO", parameters={"item": "task"})

# Time management
Intent(action="remind_in", target="5 minutes", parameters={"message": "break"})
Intent(action="remind_at", target="15:30", parameters={"message": "meeting"})

# System operations
Intent(action="open_url", target="https://github.com", parameters={})
Intent(action="search_web", target="query", parameters={})
Intent(action="lock_screen", target=None, parameters={})

# AI processing
Intent(action="ask_llm", target="question", parameters={})
Intent(action="explain_selection", target="code", parameters={})
Intent(action="summarize_selection", target="text", parameters={})
```

### Voice Processing Architecture

```python
def process_speech_segment(self):
    """Process accumulated audio through Whisper"""
    # Concatenate and normalize audio
    audio_array = np.concatenate(self.speech_buffer)
    audio_array = self.normalize_audio(audio_array)
    
    # Run Whisper inference
    segments, info = self.whisper_model.transcribe(
        audio_array,
        beam_size=5,
        language="en",
        condition_on_previous_text=False
    )
    
    # Extract transcript with confidence scoring
    transcript = ""
    avg_confidence = 0.0
    for segment in segments:
        transcript += segment.text
        avg_confidence += segment.avg_logprob
        
    if avg_confidence / len(segments) > self.confidence_threshold:
        self.on_speech_recognized(transcript.strip())
```

### Intent Resolution Pipeline

```python
def parse_intent(self, text: str) -> Optional[Intent]:
    """Multi-stage intent parsing with fallback strategies"""
    
    # Stage 1: Exact pattern matching
    intent = self.pattern_matcher.match(text)
    if intent and intent.confidence > 0.9:
        return intent
    
    # Stage 2: Fuzzy matching for typos
    intent = self.fuzzy_matcher.match(text)
    if intent and intent.confidence > 0.7:
        return intent
    
    # Stage 3: Context-aware matching
    intent = self.context_matcher.match(text, self.current_context)
    if intent and intent.confidence > 0.6:
        return intent
    
    # Stage 4: LLM fallback
    if self.llm_engine.is_available():
        intent = self.llm_engine.parse_intent(text)
        if intent and intent.confidence > 0.5:
            return intent
    
    return None
```

---

## Performance Metrics

### Latency Benchmarks

| Operation | Time (ms) | Description |
|-----------|-----------|-------------|
| Voice Recognition | 150-300 | Speech-to-text processing |
| Intent Parsing | 10-50 | Command interpretation |
| App Launch | 500-2000 | Application startup |
| Context Switch | 100-200 | Window focus change |
| Note Creation | 50-100 | File system write |
| LLM Query | 1000-3000 | AI model inference |

### Resource Usage

| Component | Memory (MB) | CPU (%) | Description |
|-----------|-------------|---------|-------------|
| Base System | 200-400 | 1-3 | Core NeuroOS processes |
| Voice Engine | 300-500 | 5-15 | Audio processing active |
| Whisper tiny.en | 150-200 | 10-30 | Speech recognition |
| Whisper small.en | 300-400 | 15-40 | Enhanced accuracy |
| LLM (Optional) | 500-1000 | 20-60 | AI processing |

### Accuracy Metrics

| Feature | Accuracy | Notes |
|---------|----------|-------|
| Voice Recognition | 85-95% | Varies by accent/noise |
| Intent Parsing | 90-98% | High for trained commands |
| App Detection | 95-99% | Cross-platform consistency |
| Context Awareness | 80-90% | Improves with usage |

---

## Development and Testing

### Testing Framework

```bash
# Run full test suite
python -m pytest tests/

# Test specific components
python -m pytest tests/test_voice_engine.py
python -m pytest tests/test_intent_parser.py
python -m pytest tests/test_os_adapters.py

# Integration tests
python multi.py --test
python multi.py --test-voice
python multi.py --test-apps
```

### Code Quality

```bash
# Code formatting
black multi.py

# Type checking
mypy multi.py

# Linting
flake8 multi.py
```

### Custom Extensions

```python
class CustomAdapter(OSAdapter):
    """Example custom OS adapter"""
    
    def launch_app(self, name: str) -> bool:
        # Custom application launch logic
        pass
        
    def send_notification(self, title: str, message: str) -> bool:
        # Custom notification implementation
        pass

# Register custom adapter
neuroos.register_adapter("custom", CustomAdapter())
```

---

## Troubleshooting

### Common Issues

**Audio Input Problems**
```bash
# Check available devices
python multi.py --list-audio

# Test microphone access
python multi.py --test-audio

# Verify permissions (macOS)
# System Settings → Privacy & Security → Microphone
```

**Performance Issues**
```bash
# Reduce model size
export NEUROOS_WHISPER_SIZE=tiny.en

# Optimize compute type  
export NEUROOS_WHISPER_COMPUTE=int8

# Disable LLM features
export NEUROOS_ENABLE_LLM=0
```

**Platform-Specific Issues**

*macOS*: Ensure microphone permissions are granted and AppleScript execution is allowed.

*Linux*: Install required system packages: `sudo apt install xdg-utils wmctrl notify-send`

*Windows*: Run as administrator for system-level operations, ensure PowerShell execution policy allows scripts.

---

## Contributing

We welcome contributions to NeuroOS! Please see our contributing guidelines:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/neuroos.git
cd neuroos

# Create development environment
python -m venv dev-env
source dev-env/bin/activate

# Install development dependencies
pip install -e .
pip install -r requirements-dev.txt
```

### Contribution Areas

- **Platform Adapters**: Extend OS integration capabilities
- **Voice Recognition**: Improve audio processing and accuracy
- **Intent Parsing**: Add new command patterns and natural language support
- **UI/UX**: Enhance user interface and experience
- **Documentation**: Improve guides and examples
- **Testing**: Expand test coverage and automation

### Code Standards

- Follow PEP 8 style guidelines
- Include type hints for new functions
- Add comprehensive docstrings
- Write unit tests for new features
- Update documentation for API changes

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Team NeuroKernels

**Samsung EnnovateX 2025 AI Challenge Submission**

NeuroOS represents our vision for the future of human-computer interaction: intelligent, private, accessible, and truly integrated with the operating system. We believe that AI assistants should enhance productivity without compromising privacy or requiring constant internet connectivity.

Our mission is to democratize AI-powered computing through solutions that work offline, respect user privacy, and provide genuine utility through deep system integration.

---

*Built for a more intelligent, private, and accessible computing experience.*
