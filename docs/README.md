# NeuroOS - Human-First, Offline OS Agent

**Samsung EnnovateX 2025 AI Challenge Submission by Team NeuroKernels**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Cross Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()
[![Offline First](https://img.shields.io/badge/offline-first-green.svg)]()
[![Open Source](https://img.shields.io/badge/license-MIT-blue.svg)]()

## Overview

NeuroOS is an OS-native agent designed to provide seamless voice and text control over desktop environments. Unlike traditional chatbot overlays, NeuroOS integrates directly with operating system primitives to offer genuine system-level automation while maintaining complete offline functionality and user privacy.

## Table of Contents

- [Approach & Uniqueness](#approach--uniqueness)
- [Technical Stack](#technical-stack)
- [Technical Architecture](#technical-architecture)
- [Implementation Details](#implementation-details)
- [Installation Instructions](#installation-instructions)
- [User Guide](#user-guide)
- [Salient Features](#salient-features)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Approach & Uniqueness

### Problem Statement

Current AI assistants suffer from several critical limitations:

- **Cloud Dependency**: Require constant internet connectivity for processing
- **Limited System Integration**: Cannot deeply interact with operating system components
- **Privacy Concerns**: Transmit sensitive voice and usage data to external servers
- **High Latency**: Network round-trips introduce delays in command execution
- **Platform Inconsistency**: Different behavior and capabilities across operating systems
- **Resource Intensity**: Heavy cloud infrastructure requirements

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

**Cross-Platform Consistency**
- Unified command interface abstracting platform differences
- Native capability utilization while maintaining compatibility
- Automatic adaptation to system-specific features

### Unique Differentiators

1. **True Offline Operation**: Complete functionality without internet connectivity after initial setup
2. **System-Level Integration**: Direct OS primitive access rather than application-level automation
3. **Privacy by Design**: Zero data transmission to external services
4. **Resource Efficiency**: Optimized for low-power devices including Raspberry Pi 5
5. **Developer-Friendly**: Single-file deployment with extensive customization options
6. **Enterprise Ready**: Professional workflow automation capabilities

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
- **[SentencePiece](https://github.com/google/sentencepiece)** - Tokenization library for language model processing

### System Integration
- **macOS**: `osascript` (AppleScript execution), `open` (application launching)
- **Linux**: `xdg-open` (standard application launching), `notify-send` (desktop notifications), `wmctrl` (window management)
- **Windows**: `start` (application launching), PowerShell (system automation), Windows API integration

### Development Tools
- **[pytest](https://pytest.org/)** - Testing framework for unit and integration tests
- **[black](https://black.readthedocs.io/)** - Code formatting and style enforcement
- **[flake8](https://flake8.pycqa.org/)** - Code quality and style checking
- **[mypy](https://mypy.readthedocs.io/)** - Static type checking for Python

## Technical Architecture

![en2](https://github.com/user-attachments/assets/cba394bf-51b1-43bc-9204-f342fc9ac1c0)
![en1](https://github.com/user-attachments/assets/7d3e1c64-157b-4ce8-9133-52dcdd3d4a46)


### System Overview

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
├─────────────────────┬─────────────────────┬───────────────────────┤
│   Regex Patterns    │   Fuzzy Matching    │   LLM Fallback       │
│   (Exact matches)   │   (Typo tolerance)  │   (Complex queries)   │
└─────────────────────┴─────────────────────┴───────────────────────┘
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
├─────────────────────┬─────────────────────┬───────────────────────┤
│   File Operations   │   Context Storage   │   Inter-app Comm     │
│   (Path resolution) │   (Session state)   │   (Data routing)      │
└─────────────────────┴─────────────────────┴───────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  OS Adapter Layer                               │
├─────────────────────┬─────────────────────┬───────────────────────┤
│   macOS Adapter     │   Linux Adapter     │   Windows Adapter     │
│   (AppleScript)     │   (xdg-open)        │   (PowerShell)        │
└─────────────────────┴─────────────────────┴───────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   System Execution Layer                        │
├─────────────────────┬─────────────────────┬───────────────────────┤
│   Applications      │   File System       │   System Services     │
│   (Launch/Control)  │   (CRUD operations) │   (Notifications)     │
└─────────────────────┴─────────────────────┴───────────────────────┘
```

### Component Details

#### Voice Engine Architecture
```
Audio Input → VAD → Segmentation → Preprocessing → Whisper → Text Output
     ↑         ↑         ↑             ↑            ↑          ↑
sounddevice webrtcvad  Silence    16kHz Resample  Model    Confidence
                       Detection                  Inference  Scoring
```

**Components:**
- **Audio Capture**: Continuous monitoring with configurable sample rates
- **Voice Activity Detection**: Real-time speech/non-speech classification
- **Audio Segmentation**: Automatic silence-based utterance boundary detection
- **Preprocessing**: Noise reduction, normalization, and format conversion
- **Speech Recognition**: Local Whisper model inference with beam search
- **Post-processing**: Confidence scoring and transcript validation

#### Intent Processing Pipeline
```
Raw Text → Normalization → Pattern Matching → Fuzzy Matching → LLM Fallback → Intent
    ↑           ↑              ↑                 ↑                ↑           ↑
Input Text   Lowercase,     Regex Patterns   Levenshtein      Language     Structured
             Punctuation   (High confidence) Distance        Model        Command
```

**Processing Stages:**
1. **Text Normalization**: Case normalization, punctuation handling, whitespace cleanup
2. **Pattern Matching**: Exact regex matches for common command structures
3. **Fuzzy Matching**: Typo-tolerant matching using edit distance algorithms
4. **Context Integration**: Previous command history and application state
5. **LLM Fallback**: Natural language processing for complex queries
6. **Intent Validation**: Semantic validation and parameter extraction

#### OS Adapter Pattern
```
┌─────────────────────────────────────────────────────────────────┐
│                    Abstract OSAdapter                           │
├─────────────────────────────────────────────────────────────────┤
│  + launch_app(name: str) -> bool                                │
│  + open_url(url: str) -> bool                                   │
│  + send_notification(title: str, message: str) -> bool          │
│  + get_active_window() -> Optional[str]                         │
│  + set_clipboard(text: str) -> bool                             │
│  + execute_command(cmd: str) -> CommandResult                   │
└─────────────────────────────────────────────────────────────────┘
                                    ▲
                    ┌───────────────┼───────────────┐
                    │               │               │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   MacAdapter    │ │  LinuxAdapter   │ │ WindowsAdapter  │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ + AppleScript   │ │ + xdg-open      │ │ + PowerShell    │
│ + open cmd      │ │ + notify-send   │ │ + start cmd     │
│ + osascript     │ │ + wmctrl        │ │ + Windows API   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Implementation Details

### Core File Structure
```
multi.py                           # Main implementation file (single-file architecture)
├── Configuration Classes
│   ├── NeuroOSConfig             # System configuration management
│   └── Intent                    # Command representation structure
├── Core Engine Classes
│   ├── VoiceEngine               # Audio processing and speech recognition
│   ├── LLMEngine                 # Optional language model integration
│   └── WorkspaceManager          # Multi-application orchestration
├── Processing Classes
│   ├── IntentParser              # Command interpretation and parsing
│   └── ActionPlanner             # Task sequencing and execution planning
├── Platform Adapters
│   ├── OSAdapter (Abstract)      # Cross-platform interface definition
│   ├── MacAdapter               # macOS-specific implementation
│   ├── LinuxAdapter             # Linux-specific implementation
│   └── WindowsAdapter           # Windows-specific implementation
└── Main Orchestrator
    └── NeuroOS                  # Primary system coordinator
```

### Supported Intent Categories

#### Application Control
```python
Intent(action="open_app", target="chrome", parameters={})
Intent(action="open_workspace", target="development", parameters={"layout": "tiled"})
Intent(action="close_app", target="spotify", parameters={})
Intent(action="focus_app", target="vscode", parameters={})
```

#### Content Management
```python
Intent(action="send_selection", target="notes", parameters={"content": "clipboard_text"})
Intent(action="take_note", target="default", parameters={"text": "Meeting notes"})
Intent(action="add_to_note", target="TODO", parameters={"item": "Review PR #123"})
Intent(action="save_file", target="document.txt", parameters={"path": "/home/user/docs"})
```

#### Time Management
```python
Intent(action="remind_in", target="5 minutes", parameters={"message": "Take break"})
Intent(action="remind_at", target="15:30", parameters={"message": "Team meeting"})
Intent(action="schedule_task", target="tomorrow", parameters={"task": "Code review"})
```

#### System Operations
```python
Intent(action="open_url", target="https://github.com", parameters={})
Intent(action="search_web", target="python asyncio tutorial", parameters={})
Intent(action="lock_screen", target=None, parameters={})
Intent(action="show_desktop", target=None, parameters={})
```

#### AI Processing
```python
Intent(action="ask_llm", target="explain mutex vs semaphore", parameters={"context": ""})
Intent(action="explain_selection", target="selected_code", parameters={"language": "python"})
Intent(action="summarize_selection", target="article_text", parameters={"max_length": 200})
```

### Voice Processing Implementation

#### Audio Capture Loop
```python
def audio_capture_loop(self):
    """Continuous audio capture with VAD-based segmentation"""
    with sd.InputStream(
        samplerate=self.sample_rate,
        channels=1,
        dtype=np.float32,
        callback=self.audio_callback
    ) as stream:
        while self.is_recording:
            # Process audio buffer
            audio_data = self.audio_buffer.get()
            
            # Apply VAD
            if self.vad.is_speech(audio_data):
                self.speech_buffer.append(audio_data)
                self.silence_start = None
            else:
                if self.silence_start is None:
                    self.silence_start = time.time()
                elif time.time() - self.silence_start > self.silence_duration:
                    # Process accumulated speech
                    self.process_speech_segment()
```

#### Speech Recognition Pipeline
```python
def process_speech_segment(self):
    """Process accumulated audio segment through Whisper"""
    if len(self.speech_buffer) < self.min_speech_length:
        return
        
    # Concatenate audio segments
    audio_array = np.concatenate(self.speech_buffer)
    
    # Normalize audio
    audio_array = self.normalize_audio(audio_array)
    
    # Run Whisper inference
    segments, info = self.whisper_model.transcribe(
        audio_array,
        beam_size=5,
        language="en",
        condition_on_previous_text=False
    )
    
    # Extract transcript with confidence
    transcript = ""
    avg_confidence = 0.0
    for segment in segments:
        transcript += segment.text
        avg_confidence += segment.avg_logprob
        
    if avg_confidence / len(segments) > self.confidence_threshold:
        self.on_speech_recognized(transcript.strip())
```

### Command Processing Architecture

#### Multi-Stage Intent Resolution
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
    
    # Stage 4: LLM fallback for natural language
    if self.llm_engine.is_available():
        intent = self.llm_engine.parse_intent(text)
        if intent and intent.confidence > 0.5:
            return intent
    
    return None
```

## Installation Instructions

### System Requirements

#### Minimum Requirements
- **Operating System**: macOS 10.14+, Ubuntu 18.04+, Windows 10+
- **Python**: Version 3.9 or higher
- **Memory**: 4 GB RAM
- **Storage**: 1 GB available space
- **Audio**: Microphone input capability
- **Processor**: 2 GHz dual-core CPU

#### Recommended Requirements
- **Operating System**: Latest stable version
- **Python**: Version 3.10 or higher
- **Memory**: 8 GB RAM
- **Storage**: 2 GB available space (SSD preferred)
- **Audio**: Noise-canceling microphone
- **Processor**: 3 GHz quad-core CPU or Apple M1/M2

### Installation Process

#### Step 1: Python Environment Setup
```bash
# Verify Python version (must be 3.9+)
python --version

# Create isolated virtual environment
python -m venv neuroos-env

# Activate virtual environment
# macOS/Linux:
source neuroos-env/bin/activate
# Windows:
neuroos-env\Scripts\activate

# Upgrade pip to latest version
pip install --upgrade pip
```

#### Step 2: Core Dependencies Installation
```bash
# Install core audio processing dependencies
pip install faster-whisper==0.10.0
pip install sounddevice==0.4.6
pip install numpy==1.24.3
pip install webrtcvad==2.0.10

# Install desktop integration dependencies
pip install pyautogui==0.9.54
pip install pyperclip==1.8.2
pip install plyer==2.1.0

# Install optional AI dependencies
pip install transformers==4.35.2
pip install torch==2.1.0
pip install sentencepiece==0.1.99
```

#### Step 3: Platform-Specific Configuration

**macOS Setup**
```bash
# Install system dependencies (if needed)
brew install portaudio

# Grant microphone permissions
echo "Please grant microphone access in:"
echo "System Settings → Privacy & Security → Microphone → Terminal/iTerm"

# Install additional utilities (optional)
brew install cliclick  # Enhanced automation capabilities
```

**Linux Setup (Ubuntu/Debian)**
```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-dev portaudio19-dev libasound2-dev

# Install desktop integration tools
sudo apt install -y xdg-utils wmctrl notify-send

# Install additional audio tools (optional)
sudo apt install -y pulseaudio-utils alsa-utils
```

**Windows Setup**
```powershell
# No additional system dependencies required
# Ensure Windows Defender allows microphone access:
# Settings → Privacy → Microphone → Allow desktop apps

# Optional: Install Windows Terminal for better CLI experience
# From Microsoft Store or: winget install Microsoft.WindowsTerminal
```

#### Step 4: NeuroOS Installation
```bash
# Download NeuroOS main file
curl -O https://raw.githubusercontent.com/neurokernels/neuroos/main/multi.py

# Or clone full repository
git clone https://github.com/neurokernels/neuroos.git
cd neuroos
```

#### Step 5: Environment Configuration
```bash
# Create configuration directory
mkdir -p ~/.neuroos

# Set environment variables (optional)
export NEUROOS_WHISPER_SIZE=tiny.en        # Model size: tiny.en, small.en
export NEUROOS_WHISPER_COMPUTE=int8        # Precision: int8, float16, float32
export NEUROOS_TTS=1                       # Enable spoken feedback
export NEUROOS_HF_MODEL="Qwen/Qwen2.5-0.5B-Instruct"  # LLM model
export TOKENIZERS_PARALLELISM=false        # Disable tokenizer warnings

# Make configuration persistent (optional)
echo 'export NEUROOS_WHISPER_SIZE=tiny.en' >> ~/.bashrc
echo 'export NEUROOS_TTS=1' >> ~/.bashrc
```

#### Step 6: Installation Verification
```bash
# Test basic functionality
python multi.py --test

# Test audio input
python multi.py --test-audio

# Start interactive mode
python multi.py --debug
```

### First-Time Setup

#### Initial Configuration
```bash
# Start NeuroOS
python multi.py

# List available microphones
> voice devices

# Expected output:
# Available audio devices:
# 0: Built-in Microphone (2 channels)
# 1: USB Headset (1 channel)
# 2: AirPods Pro (2 channels)

# Start voice recognition with device 0
> voice start 0

# Verify voice is working
> voice status
# Expected output: Voice recognition active on device 0

# Test voice recognition
> voice test
# Speak a command and verify transcript appears
```

#### Basic Functionality Test
```bash
# Test application launching
> open calculator

# Test note taking
> take note: NeuroOS setup completed successfully

# Test web search
> search web for weather today

# Test workspace (create simple workspace first)
> open calculator and notes
> save workspace basic
> close all
> open workspace basic
```

## User Guide

### Getting Started

#### Voice Setup and Configuration

**Device Selection**
```bash
# List all available audio input devices
python multi.py
> voice devices

# Sample output:
# Available audio devices:
# 0: Built-in Microphone (macOS) - 2 channels, 44100 Hz
# 1: USB Headset Microphone - 1 channel, 48000 Hz  
# 2: AirPods Pro Microphone - 1 channel, 24000 Hz

# Select device by index
> voice start 0

# Or select by name (partial matching supported)
> voice start "USB Headset"
> voice start airpods
```

**Voice Recognition Testing**
```bash
# Check current voice status
> voice status
# Output: Voice recognition active on device 0 (Built-in Microphone)

# Test voice recognition pipeline
> voice test
# Speak clearly: "This is a test"
# Output: Recognized: "This is a test" (confidence: 0.89)

# Stop voice recognition
> voice stop
```

**Audio Quality Optimization**
```bash
# Adjust VAD sensitivity (0=least sensitive, 3=most sensitive)
> config set vad_mode 2

# Set custom silence duration (seconds)
> config set silence_duration 1.5

# Configure maximum recording time
> config set max_recording_time 20.0
```

### Core Command Categories

#### Application Control

**Basic Application Management**
```bash
# Launch single application
> open chrome
> open vscode
> open "Visual Studio Code"  # Full name matching
> open spotify

# Launch with specific parameters
> open chrome --incognito
> open vscode ~/projects/neuroos
> open "Google Chrome" --new-window

# Multiple application launch
> open chrome and terminal and notes
> open vscode and chrome and spotify

# Application control
> close chrome
> close all chrome windows
> switch to vscode
> focus spotify
> minimize all windows
> show desktop
```

**Advanced Application Management**
```bash
# Application information
> list running apps
> show active window
> get app info chrome

# Window management
> move chrome to desktop 2
> resize vscode to 1200x800
> maximize current window
> tile windows left and right
```

#### Workspace Management

**Creating and Managing Workspaces**
```bash
# Create workspace by launching applications
> open vscode and terminal and chrome --new-window github.com
> save workspace development

# Create workspace with specific layout
> open notes and calculator and safari
> arrange windows grid
> save workspace research

# Load existing workspace
> open workspace development
> load workspace research

# Workspace information
> list workspaces
> show workspace development
> delete workspace old_project
```

**Advanced Workspace Features**
```bash
# Workspace with custom positioning
> create workspace design
> open figma at position 0,0 size 800x600
> open chrome at position 800,0 size 800x600
> open notes at position 0,600 size 1600x400
> save workspace design

# Conditional workspace loading
> open workspace development if not running
> restore workspace after system restart
```

#### Content Capture and Routing

**Selection-Based Operations**
```bash
# First, select text in any application, then:

# Route to applications
> send selection to notes
> send selection to reminders
> add selection to note "Meeting Notes"
> append selection to file ~/documents/research.txt

# Communication
> email selection to john@example.com subject "Research Data"
> email selection to team@company.com subject "Weekly Update" body "See attached findings:"

# Web operations
> search this
> search selection on google
> search "selected text" on stackoverflow
> open selection as url
```

**Clipboard Management**
```bash
# Direct clipboard operations
> copy "Hello World" to clipboard
> get clipboard content
> clear clipboard

# Clipboard history (if enabled)
> show clipboard history
> paste from history 3
> save clipboard to file
```

#### Note Taking and Task Management

**Note Creation and Management**
```bash
# Create new notes
> take note: Team meeting scheduled for tomorrow at 3 PM
> note: Remember to review the pull request #456
> quick note: Buy groceries after work

# Append to existing notes
> add "Review deployment checklist" to note TODO
> add "Call client about project status" to note "Work Tasks"
> append "Meeting outcome: Approved budget increase" to note "Project Alpha"

# Note organization
> create note category "Personal"
> move note "Grocery List" to category "Personal"
> list all notes
> search notes for "meeting"
```

**Reminder System**
```bash
# Relative time reminders
> remind me in 5 minutes to take a break
> remind me in 1 hour to call mom
> remind me in 30 seconds to check the oven
> remind me in 2 hours and 15 minutes to attend the meeting

# Absolute time reminders
> remind me at 3:30 PM to review the document
> remind me at 9:00 AM tomorrow to submit the report
> remind me at 8:00 PM to watch the webinar

# Recurring reminders
> remind me every day at 9 AM to check emails
> remind me every Monday at 10 AM for team standup
> remind me every Friday at 5 PM to submit timesheet

# Reminder management
> list all reminders
> cancel reminder about "team meeting"
> snooze current reminder for 10 minutes
```

#### System and Web Operations

**Web Navigation and Search**
```bash
# Direct URL opening
> open https://github.com/neurokernels/neuroos
> open google.com
> browse to stackoverflow.com
> go to https://docs.python.org

# Web search
> search web for "machine learning tutorials"
> google "python async programming"
> search "best practices for code review"
> look up "macOS terminal shortcuts"

# Search with selected text
# (First select text, then:)
> search this
> google selection
> look this up on wikipedia
```

**System Control**
```bash
# Screen and session management
> lock screen
> log out
> restart system
> shut down computer
> sleep system

# Display management
> show desktop
> hide all windows
> change to desktop 2
> create new desktop
> arrange displays

# System information
> show system info
> check battery status
> display storage usage
> show running processes
```

#### AI-Powered Operations

**Question Answering**
```bash
# General knowledge questions
> ask what is the difference between a process and a thread?
> ask how does HTTP authentication work?
> ask explain the SOLID principles in programming
> ask what are the benefits of using Docker?

# Technical explanations
> ask how to optimize database queries?
> ask what is the best way to handle errors in Python?
> ask explain RESTful API design principles
```

**Text Processing with AI**
```bash
# First select text in any application, then:

# Text explanation
> explain selection
> explain this code
> what does this function do?
> break down this paragraph

# Text summarization  
> summarize selection
> give me key points from this
> create brief summary
> extract main ideas

# Code analysis
> review this code
> find potential bugs in selection
> suggest improvements for this function
> explain the algorithm
```

### Advanced Usage Patterns

#### Workflow Automation

**Multi-Step Operations**
```bash
# Development workflow
> start development session
  # This could execute: open vscode, start dev server, open browser, open terminal

# Research workflow  
> begin research on "machine learning"
  # This could execute: open browser, search topic, open notes, create research note

# Presentation workflow
> prepare presentation mode
  # This could execute: close distractions, open slides, enable do not disturb
```

**Conditional Commands**
```bash
# Execute based on system state
> open vscode if not running
> start music if no audio playing
> save workspace if changes detected
> backup files if Friday

# Time-based conditions
> remind me to leave if after 5 PM
> start focus mode if working hours
> enable night mode if after sunset
```

#### Custom Command Creation

**Personal Shortcuts**
```bash
# Create custom aliases
> alias "start coding" to "open workspace development"
> alias "break time" to "lock screen and remind me in 15 minutes to return"
> alias "end day" to "save all and close apps and shutdown"

# Complex macro commands
> create command "weekly review"
> step 1: open note "Weekly Goals"
> step 2: search email for "completed tasks"  
> step 3: create note "Week Summary"
> save command
```

### Configuration and Customization

#### Voice Recognition Settings

**Model Configuration**
```bash
# Switch Whisper model size
> config set whisper_model small.en  # Options: tiny.en, small.en, medium.en
> config set whisper_compute float16  # Options: int8, float16, float32

# Audio processing settings
> config set sample_rate 16000# NeuroOS — Human-First, Offline OS Agent (NeuroKernels)

Single-file, cross-platform OS-level agent that turns natural language into actions across apps — offline, privacy-first, and accessible. Runs on macOS, Linux, and Windows; Raspberry Pi 5 ready.

---

## Samsung EnnovateX 2025 — Submission Header

**Problem Statement :**  
[“Building the Next OS-Level AI Experience”]

**Team name:** NeuroKernels  

**Team members:** Dhruv, Shivya, Sneha  

**Demo video:** [[YouTube link](https://www.youtube.com/watch?v=ziajMIa0Iyc)]  

**Source code:** `multi.py` (single file)  

**Models used (open-weights):**
- **Speech-to-text:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper) models (e.g., tiny.en / small.en)  
- **Local LLM (optional):** [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) or [FLAN-T5-Base](https://huggingface.co/google/flan-t5-base)  

**Datasets used:** None (runtime only)  

**Open Source Rules & Disclosure:**  
No third-party/commercial APIs or SDKs; only OSS libraries & local resources.  

---

## 1) Approach & What’s Unique

- **OS-native agent layer:** not a “bot in a tab.” We drive system events & app inter-communication with native primitives per OS.  
- **Offline-first:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for voice, small open-weight LLM for NLU/QA. No cloud calls → privacy + low latency.  
- **Accessibility-first:** one-shot tasks (“send selection to notes”, “remind me in 20 seconds”), voice or text.  
- **Workspaces:** declare workflows like “coding” → VS Code + Terminal + GitHub + Notes in one go.  
- **Single-file:** easy install/run, consistent on macOS/Linux/Windows (& Pi).  

---

## 2) Technical Stack (OSS)

- **Python:** [3.9+](https://www.python.org/)  
- **STT:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper)  
- **LLM (optional):** [Transformers](https://huggingface.co/docs/transformers/index) + [PyTorch](https://pytorch.org/)  
- **Models:** [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) / [FLAN-T5-Base](https://huggingface.co/google/flan-t5-base)  
- **Audio I/O & VAD:** [sounddevice](https://python-sounddevice.readthedocs.io/), [webrtcvad](https://github.com/wiseman/py-webrtcvad)  
- **Desktop glue:** [pyautogui](https://pyautogui.readthedocs.io/en/latest/), [pyperclip](https://pyperclip.readthedocs.io/en/latest/), [plyer](https://github.com/kivy/plyer)  
- **OS primitives:**  
  - macOS → AppleScript / `open`  
  - Linux → `xdg-open`  
  - Windows → `start` / PowerShell  

---

## 3) Architecture (brief)

<img width="3840" height="2401" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183643" src="https://github.com/user-attachments/assets/3bceb4b4-8a3f-437a-8b60-699335a7c471" />
<img width="2709" height="3840" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183615" src="https://github.com/user-attachments/assets/85569663-c231-449b-aee4-eb26c8a1a271" />
<img width="3840" height="292" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183535" src="https://github.com/user-attachments/assets/59288b96-7750-49e1-9efe-6f566c1cfb94" />
<img width="3840" height="1812" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183506" src="https://github.com/user-attachments/assets/01d0be4c-99ce-4f46-bc4c-73af33cfd175" />
<img width="2111" height="3840" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183428" src="https://github.com/user-attachments/assets/50a9146c-ebc1-40fd-90c7-cc7a921ebf89" />
<img width="3840" height="456" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183241" src="https://github.com/user-attachments/assets/b7576c24-6bf8-43fd-8ed5-784a11cedf40" />
<img width="3840" height="3511" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-26-183100" src="https://github.com/user-attachments/assets/b1d99dd9-b1af-45b1-8cbe-dc09df266936" />


**Highlights:**
- Intent-first (regex + typo/fuzzy), LLM fallback for Q&A and explain/summarize selection.  
- Adapters abstract per-OS differences.  
- Context remembers last selection, recent apps, last workspace, etc.  

---

## 4) Implementation Details

**File:** `multi.py`  

**Key modules inside:**  
- **OSAdapter** (MacAdapter, LinuxAdapter, WindowsAdapter)  
- **VoiceEngine** (device listing, test record, VAD, resample → 16k, robust segmenting)  
- **LLMEngine** (lazy-load HF model; encoder-decoder or decoder-only)  
- **Intents:**  
  - open_app  
  - open_workspace / save_workspace  
  - send selection to {notes|reminders|file|mail}  
  - remind {in|at}  
  - open_url, search_web  
  - ask_llm, explain/summarize selection  
  - voice {devices|start|status|stop}  

---

## 5) Installation (Single Place)

```bash
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install faster-whisper sounddevice numpy webrtcvad transformers torch sentencepiece pyautogui pyperclip plyer


# Optional tuning:
export NEUROOS_WHISPER_SIZE=tiny.en        # or small.en
export NEUROOS_WHISPER_COMPUTE=int8        # CPU-friendly
export NEUROOS_TTS=1                       # spoken confirmations
export NEUROOS_HF_MODEL="Qwen/Qwen2.5-0.5B-Instruct"
export TOKENIZERS_PARALLELISM=false

# Run:
python multi.py --debug
