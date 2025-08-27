# NeuroOS — Human-First, Offline OS Agent (NeuroKernels)

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

(Architecture diagram image placeholder — insert your own diagram here)

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
