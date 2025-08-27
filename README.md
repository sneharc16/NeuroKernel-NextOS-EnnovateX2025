### **Important Instructions**:  
- Click on *"Use this template"* button and *"Create a new repository"* in your github account for submission.
<img width="1262" height="93" alt="Screenshot 2025-08-15 at 5 59 49 AM" src="https://github.com/user-attachments/assets/b72d5afd-ba07-4da1-ac05-a373b3168b6a" />

- Add one of the following open source licenses - [MIT](https://opensource.org/licenses/MIT), [Apache 2.0](https://opensource.org/licenses/Apache-2.0) or [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause) to your submission repository. 
- Once your repository is ready for **evaluation** send an email to ennovatex.io@samsung.com with the subject - "AI Challenge Submission - Team name" and the body of the email must contain only the Team Name, Team Leader Name & your GitHub project repository link.
- All submission project materials outlined below must be added to the github repository and nothing should be attached in the submission email.
- In case of any query, please feel free to reach out to us at ennovatex.io@samsung.com

#### Evaluation Criteria

| Project Aspect | % |
| --- | --- |
| Novelty of Approach | 25% |
| Technical implementation & Documentation | 25% |
| UI/UX Design or User Interaction Design | 15% |
| Ethical Considerations & Scalability | 10% |
| Demo Video (10 mins max) | 25% |

**-------------------------- Your Project README.md should start from here -----------------------------**

# Samsung EnnovateX 2025 AI Challenge Submission

* **Problem Statement** - Building the Next OS-Level AI Experience - A single, powerful multimodal foundation model can serve as an unchangeable firmware within edge/mobile operating system, enabling applications to use compact "adapters" (for varied downstream tasks – text, image, audio, video) instead of bundling several large models. Some of the architectural innovations that can be included are - firmware backbone and task-specific adapters, multi-path execution to route tasks efficiently based on complexity, demonstrating system benefits through metrics like latency and battery performance.

* **Team name** - NeuroKernels

* **Team members (Names)** - Dhruv Dawar [(@dhruv-developer)](https://github.com/dhruv-developer), Sneha Roychowdhury [(@sneharc16)](https://github.com/sneharc16), and Shivya Khandpur [(@Shivya0410)](https://github.com/Shivya0410))

* **Demo Video Link** - https://www.youtube.com/watch?v=ziajMIa0Iyc

## Project Artefacts

* **Technical Documentation** - [Docs](./docs/) *(All technical details including architecture, setup, usage, compliance, models/datasets, testing, FAQs, and changelog written in markdown files inside the docs folder)*

* **Source Code** - [Source](./src/) *(Cross-platform text-only MVP (macOS + Linux + Windows terminal). Each script installs and runs consistently on the intended platforms.)*

* **Models Used** - Optional offline: GGUF or local Hugging Face model folder. 

* **Models Published** - N/A (no custom model trained).

* **Datasets Used** - N/A (no external datasets required).

* **Datasets Published** - N/A

## Attribution

This project is built from scratch as an original OS-level AI experience. No existing open source projects were used as a base.

---

# NeuroOS — Human-First OS-Level AI (Text-Only MVP)

## Setup & Installation

### Linux (Debian/Ubuntu)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
sudo apt-get update
sudo apt-get install -y xclip wl-clipboard libnotify-bin playerctl ffmpeg xdg-utils || true
sudo apt-get install -y mpv vlc || true
python src/neuroos_linux_nollm.py
```

### macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python src/neuroos_macos.py
```

### Compliance Mode (no network helpers)
```bash
export NEUROOS_OFFLINE=1
```
This disables web helpers (RSS, weather, translate) and guarantees fully local execution.  


## Usage

**Run:**
- Linux: `python src/neuroos_linux_nollm.py`
- macOS: `python src/neuroos_macos.py`

**Example commands** (chainable with `;`, `then`, `and then`):
- `open chrome`
- `open firefox and code and terminal`
- `open workspace coding`
- `save workspace myfocus` → `open workspace myfocus`
- `send selection to notes`
- `email selection to you@example.com subject Research`
- `search this` (copy text first)
- `take note: meeting at 6`
- `remind me in 20 seconds to stretch`
- `open file report.pdf`
- `play file ~/Music/song.mp3`


## Offline / Compliance Mode

**Challenge rule recap:**
- **Allowed:** open-source libraries, open data
- **Disallowed:** third-party APIs, proprietary data

Compliance mode is enabled by setting `NEUROOS_OFFLINE=1`.  


## Models

- MVP uses no LLM (rule-compliant).
- Optional: local GGUF or Hugging Face models (TinyLlama, Qwen).
- No internet calls; models load only from local files.


## Datasets

- None required for MVP (rule-based).
- Optionally, a small synthetic dataset of command → intent/slots pairs can be published on Hugging Face.


## Security & Privacy

- Offline by default, strict compliance mode
- Local storage only for notes, reminders, and workspaces
- No telemetry, no cloud accounts
- Minimal OS-level privileges
- Full transparency; users can inspect all files



## Testing & Validation

- **Automated:** smoke tests, intent parsing, file opening
- **Manual:** scripted demo sequence covering app launch, workspaces, reminders, file/music control
- **Metrics:** command latency < 1s; ≥90% accuracy on demo intent set; full sequence completion rate



## FAQ

- Uses no third-party APIs in Compliance Mode
- Optional offline LLMs supported but disabled for submission
- Architecture is Raspberry Pi-ready
- Default workspaces are user-editable JSON



## Changelog

- **2025-MM-DD:** Created Linux terminal MVP (no LLM), compliance mode added
- **2025-MM-DD:** Added macOS text-only script with Apple Notes/Reminders integration
- **2025-MM-DD:** Implemented workspaces, chaining, selection routing
- **2025-MM-DD:** Added reminders, fuzzy file open, media controls, local audio
- **2025-MM-DD:** Wrote full docs and test plan



## License

LICENSE (MIT)
MIT License

Copyright (c) 2025 NeuroKernels

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction...
