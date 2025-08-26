import os, re, json, time, difflib, subprocess, shlex, glob, threading, queue, sys, argparse, traceback, platform, wave
from typing import Dict, Optional, Tuple, List, Any
from pathlib import Path

# --------- args / debug ----------
ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--debug", action="store_true")
args, _ = ap.parse_known_args()
DEBUG = bool(args.debug)

def dbg(msg: str):
    if DEBUG:
        print(f"[debug] {msg}")

def log_ex(e: BaseException):
    if DEBUG: traceback.print_exc()
    else: print(f"[neuroos] {e.__class__.__name__}: {e}")

# --------- dirs / env ----------
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
HOME = str(Path.home())
DATA_DIR = os.path.join(HOME, "NeuroOS")
NOTES_DIR = os.path.join(DATA_DIR, "Notes")
os.makedirs(NOTES_DIR, exist_ok=True)
WORKSPACES_FILE = os.path.join(DATA_DIR, "workspaces.json")
SYS = platform.system().lower()

# --------- misc helpers ----------
ANSI_ESC = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

def normalize_text(raw: str) -> str:
    s = ANSI_ESC.sub("", raw)
    s = re.sub(r"(.)\1{2,}", r"\1", s)
    s = s.replace("_"," ").replace("-"," ")
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s).lower()
    for a,b in {
        "opennn":"open","oppen":"open","openn":"open",
        "reming":"remind","remeinder":"reminder",
        "coede":"code","codee":"code","codde":"code",
        "visualstudio":"visual studio","vs  code":"vs code",
        "skleep":"sleep"
    }.items():
        s = s.replace(a,b)
    return re.sub(r"\s+"," ", s).strip()

def detect_url(s: str) -> Optional[str]:
    m = re.search(r"\b(https?://[^\s]+)\b", s, re.I)
    return m.group(1) if m else None

# --------- notifications & TTS ----------
def notify(title: str, message: str):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=5)
    except Exception as e:
        dbg(f"notify failed: {e}")

def esc_as(s: str) -> str:  # AppleScript
    return s.replace("\\", "\\\\").replace('"', '\\"')

def ps_escape(s: str) -> str:  # PowerShell
    return s.replace('"', '""')

def speak(msg: str):
    if os.environ.get("NEUROOS_TTS") != "1":
        return
    try:
        sysname = platform.system().lower()
        if "darwin" in sysname or "mac" in sysname:
            subprocess.Popen(["say", msg])
        elif "linux" in sysname:
            for cmd in (["spd-say", msg], ["espeak", msg]):
                try:
                    subprocess.Popen(cmd); break
                except Exception:
                    continue
        elif "windows" in sysname:
            safe = ps_escape(msg)
            psc = 'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{}")'.format(safe)
            subprocess.Popen(["powershell", "-NoProfile", "-Command", psc])
    except Exception:
        pass

# --------- clipboard / selection ----------
def osa(script: str) -> None:
    try: subprocess.run(["osascript", "-e", script], check=False)
    except Exception as e: log_ex(e)

def copy_selection():
    try:
        sysname = platform.system().lower()
        if "darwin" in sysname:
            osa('tell application "System Events" to keystroke "c" using {command down}')
            time.sleep(0.15)
        else:
            import pyautogui
            pyautogui.hotkey('ctrl','c')
            time.sleep(0.15)
        import pyperclip
        return pyperclip.paste() or ""
    except Exception as e:
        dbg(f"copy_selection failed: {e}")
        try:
            import pyperclip
            return pyperclip.paste() or ""
        except Exception:
            return ""

# --------- OS adapters (mac / linux / win) ----------
class OSAdapter:
    def open_app(self, user_name:str)->bool: raise NotImplementedError
    def open_url(self, url:str)->None: raise NotImplementedError
    def simple_text_doc(self, text:str)->None: raise NotImplementedError
    def notes_append(self, title:str, body:str)->None: raise NotImplementedError
    def mail_draft(self, to_addr:Optional[str], subject:str, body:str)->None: raise NotImplementedError
    def music_play(self)->None: pass
    def music_pause(self)->None: pass

class MacAdapter(OSAdapter):
    APP_CANONICALS = {
        "safari": "Safari", "chrome": "Google Chrome", "google chrome": "Google Chrome",
        "notes": "Notes", "music": "Music", "vscode": "Visual Studio Code",
        "code": "Visual Studio Code", "terminal": "Terminal", "iterm":"iTerm",
        "reminders":"Reminders", "preview":"Preview", "textedit":"TextEdit",
        "mail":"Mail", "finder":"Finder",
    }
    BUNDLE_IDS = {
        "Safari":"com.apple.Safari", "Google Chrome":"com.google.Chrome", "Notes":"com.apple.Notes",
        "Music":"com.apple.Music", "Visual Studio Code":"com.microsoft.VSCode",
        "Terminal":"com.apple.Terminal", "iTerm":"com.googlecode.iterm2",
        "Reminders":"com.apple.reminders", "Preview":"com.apple.Preview",
        "TextEdit":"com.apple.TextEdit", "Mail":"com.apple.mail", "Finder":"com.apple.finder",
    }
    _APP_CACHE = None
    def _list_apps(self)->List[str]:
        if MacAdapter._APP_CACHE is not None: return MacAdapter._APP_CACHE
        paths = ["/Applications/*.app","/Applications/*/*.app","/System/Applications/*.app", os.path.join(HOME,"Applications","*.app")]
        names, seen = [], set()
        for pat in paths:
            for ap in glob.glob(pat):
                name = os.path.splitext(os.path.basename(ap))[0]
                if name not in seen: names.append(name); seen.add(name)
        MacAdapter._APP_CACHE = names
        return names
    def _resolve(self, user_name:str)->Optional[str]:
        s = (user_name or "").strip().lower()
        if s in self.APP_CANONICALS: return self.APP_CANONICALS[s]
        for n in self._list_apps():
            if n.lower()==s: return n
        best = difflib.get_close_matches(s,[n.lower() for n in self._list_apps()],n=1,cutoff=0.72)
        if best:
            for n in self._list_apps():
                if n.lower()==best[0]: return n
        return None
    def open_app(self, user_name:str)->bool:
        name = self._resolve(user_name) or user_name
        try:
            r = subprocess.run(["open","-a",name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if r.returncode==0: return True
            bid = self.BUNDLE_IDS.get(name)
            if bid:
                r = subprocess.run(["open","-b",bid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if r.returncode==0: return True
            osa('tell application "{}" to activate'.format(esc_as(name)))
            return True
        except Exception:
            return False
    def open_url(self, url:str)->None:
        try: osa('tell application "System Events" to open location "{}"'.format(esc_as(url)))
        except Exception: subprocess.Popen(["open",url])
    def simple_text_doc(self, text:str)->None:
        try:
            safe = esc_as(text)
            osa('''tell application "TextEdit"
                     activate
                     make new document with properties {text:"%s"}
                   end tell''' % safe)
        except Exception:
            path = os.path.join(HOME,"Desktop",f"neuroos_{int(time.time())}.txt")
            with open(path,"w") as f: f.write(text)
            subprocess.Popen(["open",path])
    def notes_append(self, title:str, body:str)->None:
        try:
            title_e, body_e = esc_as(title), esc_as(body)
            osa('''
            tell application "Notes"
              activate
              set theAccount to default account
              try
                set theFolder to folder "Notes" of theAccount
              on error
                set theFolder to make new folder at theAccount with properties {name:"Notes"}
              end try
              set theNotes to notes of theFolder whose name is "%s"
              if (count of theNotes)=0 then
                make new note at end of theFolder with properties {name:"%s", body:"%s"}
              else
                set existingNote to item 1 of theNotes
                set body of existingNote to (body of existingNote) & "<br/><div>%s</div>"
              end if
            end tell
            ''' % (title_e, title_e, body_e, body_e))
        except Exception as e:
            dbg("notes_append fallback: {}".format(e))
            path = os.path.join(NOTES_DIR, f"{title}.md")
            with open(path,"a") as f:
                f.write(f"\n\n---\n{time.ctime()}\n{body}\n")
            subprocess.Popen(["open",path])
    def mail_draft(self, to_addr:Optional[str], subject:str, body:str)->None:
        try:
            subj, bod, addr = esc_as(subject), esc_as(body), esc_as(to_addr or "")
            osa('''
            tell application "Mail"
              activate
              set newMessage to make new outgoing message with properties {subject:"%s", content:"%s" & return}
              if "%s" is not "" then
                tell newMessage to make new to recipient at end of to recipients with properties {address:"%s"}
              end if
            end tell
            ''' % (subj, bod, addr, addr))
        except Exception:
            from urllib.parse import quote
            url = f"mailto:{to_addr or ''}?subject={quote(subject)}&body={quote(body)}"
            self.open_url(url)
    def music_play(self)->None: osa('tell application "Music" to play')
    def music_pause(self)->None: osa('tell application "Music" to pause')

class LinuxAdapter(OSAdapter):
    APP_ALTS = {
        "chrome": ["google-chrome","google-chrome-stable","chromium","chromium-browser"],
        "google chrome": ["google-chrome","google-chrome-stable","chromium","chromium-browser"],
        "safari": [], "vscode": ["code","code-insiders"], "code":["code","code-insiders"],
        "terminal": ["gnome-terminal","konsole","xterm","xfce4-terminal","tilix","alacritty"],
        "notes": ["gedit","xed","kate","mousepad","leafpad"], "textedit": ["gedit","xed","kate","mousepad","leafpad"],
        "mail": ["thunderbird","evolution"], "music": ["vlc","rhythmbox","spotify"],
    }
    def _which(self, cmd:str)->Optional[str]:
        from shutil import which
        return which(cmd)
    def open_app(self, user_name:str)->bool:
        s = (user_name or "").strip().lower()
        alts = self.APP_ALTS.get(s) or [s]
        for c in alts:
            exe = self._which(c)
            if exe:
                try: subprocess.Popen([exe]); return True
                except Exception: continue
        return False
    def open_url(self, url:str)->None:
        try: subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e: dbg(f"xdg-open fail: {e}")
    def simple_text_doc(self, text:str)->None:
        path = os.path.join(HOME,"Desktop",f"neuroos_{int(time.time())}.txt")
        with open(path,"w") as f: f.write(text)
        self.open_url(path)
    def notes_append(self, title:str, body:str)->None:
        path = os.path.join(NOTES_DIR, f"{title}.md")
        with open(path,"a") as f: f.write(f"\n\n---\n{time.ctime()}\n{body}\n")
        self.open_url(path)
    def mail_draft(self, to_addr:Optional[str], subject:str, body:str)->None:
        from urllib.parse import quote
        url = f"mailto:{to_addr or ''}?subject={quote(subject)}&body={quote(body)}"
        self.open_url(url)

class WindowsAdapter(OSAdapter):
    APP_ALTS = {
        "chrome": ["chrome.exe","chrome"], "google chrome": ["chrome.exe","chrome"],
        "edge": ["msedge.exe","msedge"], "vscode": ["Code.exe","code"], "code": ["Code.exe","code"],
        "terminal": ["wt.exe","powershell.exe","cmd.exe"], "notes": ["notepad.exe"],
        "textedit": ["notepad.exe"], "mail": ["outlook.exe"], "music": ["spotify.exe","groove.exe"], "safari": [],
    }
    def _start(self, target:str)->bool:
        try:
            subprocess.Popen('start "" "{}"'.format(target), shell=True)
            return True
        except Exception:
            return False
    def open_app(self, user_name:str)->bool:
        s = (user_name or "").strip().lower()
        alts = self.APP_ALTS.get(s) or [s]
        for c in alts:
            if self._start(c): return True
        return False
    def open_url(self, url:str)->None: self._start(url)
    def simple_text_doc(self, text:str)->None:
        path = os.path.join(str(Path.home()), "Desktop", f"neuroos_{int(time.time())}.txt")
        with open(path,"w",encoding="utf-8") as f: f.write(text)
        self.open_url(path)
    def notes_append(self, title:str, body:str)->None:
        path = os.path.join(NOTES_DIR, f"{title}.md")
        with open(path,"a",encoding="utf-8") as f: f.write(f"\n\n---\n{time.ctime()}\n{body}\n")
        self.open_url(path)
    def mail_draft(self, to_addr:Optional[str], subject:str, body:str)->None:
        from urllib.parse import quote
        url = f"mailto:{to_addr or ''}?subject={quote(subject)}&body={quote(body)}"
        self.open_url(url)

if "darwin" in SYS or "mac" in SYS: ADAPT: OSAdapter = MacAdapter()
elif "windows" in SYS: ADAPT = WindowsAdapter()
else: ADAPT = LinuxAdapter()

# --------- Notes / reminders / mail wrappers ----------
def notes_create_or_append(title: str, body: str):
    ADAPT.notes_append(title, body); notify("NeuroOS", f"Added to '{title}'"); speak("Added to notes.")

_timers: List[threading.Timer] = []
def _fire_local_reminder(msg:str):
    notify("NeuroOS Reminder", msg); speak(msg)

def reminders_add(message: str, at_hhmm: Optional[Tuple[int,int]] = None, delta_rel: Optional[Tuple[str,int]] = None):
    when_sec = None
    if at_hhmm:
        h, m = at_hhmm
        now = time.localtime()
        target = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, h, m, 0, now.tm_wday, now.tm_yday, now.tm_isdst))
        if target <= time.time(): target += 86400
        when_sec = max(0, target - time.time())
    elif delta_rel:
        unit, n = delta_rel; n = int(n)
        when_sec = n * 3600 if unit=="hours" else n * 60 if unit=="minutes" else n
    if when_sec is None:
        notify("NeuroOS Reminder", message); speak("Reminder added."); return
    t = threading.Timer(when_sec, _fire_local_reminder, args=(message,))
    t.daemon = True; t.start(); _timers.append(t)
    print(f"[neuroos] Reminder in {int(when_sec)} sec: {message}" if when_sec<60 else f"[neuroos] Reminder in ~{int(when_sec//60)} min: {message}")
    speak("Reminder set.")

def mail_draft(to_addr: Optional[str], subject: str, body: str):
    ADAPT.mail_draft(to_addr, subject, body); speak("Draft ready.")

def open_url(url:str): ADAPT.open_url(url)
def textedit_new_with(text:str): ADAPT.simple_text_doc(text)
def music_play(): ADAPT.music_play()
def music_pause(): ADAPT.music_pause()

# --------- app name resolution ----------
APP_CANONICALS = {
    "safari":"safari","chrome":"chrome","google chrome":"chrome","edge":"edge",
    "notes":"notes","music":"music","vscode":"vscode","code":"vscode",
    "terminal":"terminal","reminders":"reminders","preview":"preview","textedit":"textedit","mail":"mail",
}
APP_SYNONYMS = {
    "browser": "chrome" if not ("darwin" in SYS or "mac" in SYS) else "safari",
    "google": "chrome", "apple music":"music", "vs code":"vscode",
    "v s code":"vscode", "visual studio code":"vscode", "visualstudio code":"vscode",
    "visualstudio":"vscode", "finder":"terminal" if not ("darwin" in SYS or "mac" in SYS) else "finder",
}
def resolve_app_name(user_name: str) -> Optional[str]:
    s = (user_name or "").strip().lower()
    if s in APP_SYNONYMS: s = APP_SYNONYMS[s]
    if s in APP_CANONICALS: return APP_CANONICALS[s]
    candidates = list(APP_SYNONYMS.keys()) + list(APP_CANONICALS.keys())
    best = difflib.get_close_matches(s, candidates, n=1, cutoff=0.72)
    return APP_CANONICALS.get(best[0], best[0]) if best else s
def open_app(user_name: str) -> bool:
    canonical = resolve_app_name(user_name)
    ok = ADAPT.open_app(canonical)
    if ok: print(f"[neuroos] Opening {canonical}"); speak(f"Opening {canonical}")
    else:  print("[neuroos] I couldn't recognize that app."); speak("Sorry, I couldn't recognize that app.")
    return ok
def search_web(query: str):
    q = shlex.quote(query); open_url(f"https://duckduckgo.com/?q={q}")

# --------- context ----------
class Context:
    def __init__(self) -> None:
        self.last_intent: Optional[str] = None
        self.last_slots: Dict[str, Any] = {}
        self.last_selection: str = ""
        self.last_workspace: Optional[str] = None
        self.last_opened_apps: List[str] = []
CTX = Context()

# --------- time parsing ----------
def parse_time_relative(text: str) -> Optional[Tuple[str,int]]:
    m = re.search(r"\b(in|after|for)\s+(\d{1,4})\s*(seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h)\b", text, re.I)
    if not m: return None
    n = int(m.group(2)); unit = m.group(3).lower()
    if unit.startswith(("hour","hr","h")): return ("hours", n)
    if unit.startswith(("sec","s")): return ("seconds", n)
    return ("minutes", n)
def extract_message_after_relative(text: str) -> Optional[str]:
    m = re.search(r"(?:in|after|for)\s+\d{1,4}\s*(?:seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h)\s*(?:to|for)\s+(.+)$", text, re.I)
    return m.group(1).strip() if m else None
def parse_time_at(text: str) -> Optional[Tuple[int,int]]:
    t = text.lower().strip()
    m = re.search(r"\b(at\s*)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", t)
    if not m: return None
    hour = int(m.group(2)); minute = int(m.group(3) or 0); ampm = m.group(4)
    if ampm == "pm" and hour < 12: hour += 12
    if ampm == "am" and hour == 12: hour = 0
    return (hour, minute)
def extract_message_after_at(text: str) -> Optional[str]:
    m = re.search(r"\bat\b.*?(?:to|for)\s+(.+)$", text, re.I)
    return m.group(1).strip() if m else None

# --------- tiny rule-answers + LLM ----------
CAPITALS = {"india":"New Delhi","usa":"Washington, D.C.","united states":"Washington, D.C.","uk":"London",
            "united kingdom":"London","france":"Paris","germany":"Berlin","italy":"Rome","spain":"Madrid",
            "japan":"Tokyo","china":"Beijing","canada":"Ottawa","australia":"Canberra"}
def qa_rule_answer(q: str) -> Optional[str]:
    t = normalize_text(q)
    m = re.search(r"(?:what\s+is|what's|whats)?\s*the\s+capital\s+of\s+([a-z .]+)\??$", t)
    if m: return CAPITALS.get(m.group(1).strip())
    if re.search(r"\bwhat\s+is\s+a?\s*mutex\??$|\bdefine\s+mutex\b", t):
        return ("A mutex (mutual exclusion lock) lets only one thread enter a critical section at a time. "
                "Threads must acquire it before touching shared state and release it after, preventing race conditions.")
    return None

class LLMEngine:
    def __init__(self):
        self._ready=False; self._err=None; self._pipe=None; self._task=None; self._is_encdec=False
        self._model_id = os.environ.get("NEUROOS_HF_PATH") or os.environ.get("NEUROOS_HF_MODEL","Qwen/Qwen2.5-0.5B-Instruct")
        self._lock = threading.Lock()
    def _lazy_load(self):
        with self._lock:
            if self._ready or self._err: return
            try:
                from transformers import AutoConfig, pipeline
                cfg = AutoConfig.from_pretrained(self._model_id, trust_remote_code=True)
                self._is_encdec = bool(getattr(cfg,"is_encoder_decoder",False))
                self._task = "text2text-generation" if self._is_encdec else "text-generation"
                self._pipe = pipeline(self._task, model=self._model_id, device_map="cpu", trust_remote_code=True)
                self._ready=True; dbg(f"LLM loaded: {self._model_id} encdec={self._is_encdec}")
            except Exception as e:
                self._err=str(e); log_ex(e)
    def available(self)->bool:
        if not self._ready and not self._err: self._lazy_load()
        return self._ready
    def status(self)->str:
        if self._ready: return f"[llm] ready ({self._model_id})"
        if self._err: return f"[llm] error: {self._err}"
        return "[llm] loading…"
    def _build_prompt(self, q:str, ctx:Optional[str])->str:
        if self._is_encdec:
            return ("Use the context to answer concisely.\nContext:\n{}\n\nQuestion: {}\nAnswer:"
                    .format(ctx, q)) if ctx else ("Answer concisely: {}".format(q))
        return ("You are factual and concise.\nContext:\n{}\n\nQ: {}\nA:".format(ctx,q)) if ctx else ("You are factual and concise.\nQ: {}\nA:".format(q))
    def answer(self, prompt:str, context:Optional[str]=None, max_new_tokens:int=128)->Optional[str]:
        ra = qa_rule_answer(prompt)
        if ra: return ra
        if not self.available(): return None
        try:
            q = self._build_prompt(prompt.strip(), context)
            if self._task=="text2text-generation":
                out = self._pipe(q, max_new_tokens=max_new_tokens, num_beams=4, do_sample=False)
                return (out[0].get("generated_text") or "").strip() or None
            out = self._pipe(q, max_new_tokens=max_new_tokens, do_sample=False, return_full_text=False)
            text = (out[0].get("generated_text") or "").strip()
            text = re.split(r"\nQ:\s*", text)[0].strip()
            return text or None
        except Exception as e:
            log_ex(e); return None

LLM = LLMEngine()

# --------- intents ----------
OPEN_VERBS  = r"(open|launch|start|run|load|i want|i wanna|please|pls)"
PLAY_VERBS  = r"(play|start)"
STOP_VERBS  = r"(stop|pause|halt)"
REMIND_WORD = r"(remind|reminder|remember)"
QUESTION_LIKE = re.compile(r"^\s*(who|what|when|where|why|how|which|whom)\b", re.I)
INTENT_PATTERNS = [
    ("open_workspace", re.compile(rf"\b{OPEN_VERBS}\b.*\b(workspace)\b\s*(\w+)?|^open\s+workspace\s+(\w+)$", re.I)),
    ("save_workspace", re.compile(r"^save\s+workspace\s+([a-z0-9_-]+)$", re.I)),
    ("open_multi_apps", re.compile(rf"\b{OPEN_VERBS}\b\s+([a-z0-9 .]+?)(?:\s+and\s+([a-z0-9 .]+))+$", re.I)),
    ("open_app", re.compile(rf"\b{OPEN_VERBS}\b\s+([a-z0-9 .]+)$", re.I)),
    ("open_url", re.compile(r"\b(open|launch)\b\s+(https?://[^\s]+)", re.I)),
    ("search_web", re.compile(r"\b(search|google|look up|find)\b\s+(for\s+)?(.+)$", re.I)),
    ("note_text", re.compile(r"\b(take|make|create|add|append)\b.*\b(note|notes)\b.*?(?:about|that|:)?\s*(.+)$", re.I)),
    ("add_to_titled_note", re.compile(r"\badd\b\s+(.+?)\s+\bto\b\s+(?:note|notes)\s+(.+)$", re.I)),
    ("send_selection_to", re.compile(rf"\b(send|save|add|append)\b\s+(?:from\s+([a-z0-9 .]+)\s+)?(this|selection|selected text|it)?\s*\b(to|into|in)\b\s+(notes?|reminders?|textedit|mail|file)\b", re.I)),
    ("search_with_selection", re.compile(r"\b(search|google|look up|find)\b\s+(this|selection|selected text|it)\b", re.I)),
    ("email_selection", re.compile(r"\b(email|mail)\b\s+(this|selection|selected text|it)\s+(?:to\s+([^\s]+))?(?:\s+subject\s+(.+))?$", re.I)),
    ("remind_for_rel", re.compile(rf"\b(remind|reminder)\b.*\b(for|in|after)\b.*\b(\d+)\s*(seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h)\b.*?(?:to|for)\s+(.+)$", re.I)),
    ("remind_in", re.compile(rf"\b{REMIND_WORD}\b.*\b(in|after|for)\b", re.I)),
    ("remind_at", re.compile(rf"\b{REMIND_WORD}\b.*\bat\b", re.I)),
    ("play_music", re.compile(rf"\b{PLAY_VERBS}\b.*\b(music|song|playlist)\b", re.I)),
    ("stop_music", re.compile(rf"\b{STOP_VERBS}\b.*\b(music|song|playlist)\b", re.I)),
    ("open_file_direct", re.compile(r"\b(open|view|show)\b\s+([~/][^\s]+|[^ ]+\.[a-z0-9]{1,6})$", re.I)),
    ("ask_llm", re.compile(r"^(ask|question)\s+(.+)$", re.I)),
    ("explain_selection", re.compile(r"^(explain|what does this mean)\s+(this|selection|selected text|it)?$", re.I)),
    ("summarize_selection", re.compile(r"^(summarize|tl;dr)\s+(this|selection|selected text|it)?$", re.I)),
    ("voice_start", re.compile(r"^voice (on|start)(?:\s+(.+))?$", re.I)),
    ("voice_stop", re.compile(r"^voice (off|stop)$", re.I)),
    ("voice_status", re.compile(r"^voice status$", re.I)),
    ("voice_devices", re.compile(r"^voice devices$", re.I)),
    ("voice_test", re.compile(r"^voice test$", re.I)),
    ("llm_status", re.compile(r"^llm status$", re.I)),
    ("do_again", re.compile(r"\b(do it again|again|same again|repeat that)\b", re.I)),
]

def fuzzy_match_any_appphrase(text: str) -> Optional[str]:
    hay = text.replace("visualstudio", "visual studio")
    candidates = list(APP_SYNONYMS.keys()) + list(APP_CANONICALS.keys())
    best, score = None, 0.0
    for c in candidates:
        if c in hay: return c
        r = difflib.SequenceMatcher(None, hay, c).ratio()
        if r > score: best, score = c, r
    return best if score >= 0.70 else None

def parse_intent(raw_text: str):
    t = normalize_text(raw_text)
    if not t: return None, {}, 0.0
    url = detect_url(t)
    if url: return "open_url", {"url": url}, 0.98
    for name, rx in INTENT_PATTERNS:
        m = rx.search(t)
        if not m: continue
        if name == "open_workspace":
            ws = (m.group(2) or m.group(3) or "").strip().lower() or (CTX.last_workspace or "coding")
            return "open_workspace", {"workspace": ws}, 0.9
        if name == "save_workspace": return "save_workspace", {"name": m.group(1).lower()}, 0.95
        if name == "open_multi_apps":
            verb_match = re.search(OPEN_VERBS, t); start = verb_match.end() if verb_match else 0
            seg = t[start:].strip()
            apps = re.split(r"\s+and\s+|, ", seg, flags=re.I)
            wanted = []
            for a in apps:
                a = re.sub(rf"^{OPEN_VERBS}\s+", "", a, flags=re.I).strip()
                if a: wanted.append(a)
            return "open_multi_apps", {"apps_raw": wanted}, 0.88
        if name == "open_app":   return "open_app", {"app_raw": m.group(1).strip()}, 0.86
        if name == "open_url":   return "open_url", {"url": m.group(2)}, 0.98
        if name == "search_web": return "search_web", {"query": m.group(3).strip()}, 0.9
        if name == "note_text":  return "note_text", {"title":"Quick Notes","body": m.group(3).strip()}, 0.9
        if name == "add_to_titled_note": return "add_to_titled_note", {"title": m.group(2).strip(), "body": m.group(1).strip()}, 0.9
        if name == "send_selection_to":
            src = (m.group(2) or "").strip(); dest = m.group(5).lower()
            return "send_selection_to", {"source_app": src or None, "dest": dest}, 0.92
        if name == "search_with_selection": return "search_with_selection", {}, 0.9
        if name == "email_selection":
            to_addr = (m.group(3) or "").strip() or None; subject = (m.group(4) or "Note").strip()
            return "email_selection", {"to": to_addr, "subject": subject}, 0.92
        if name == "remind_for_rel":
            n = int(m.group(3)); unit = m.group(4); msg = m.group(5).strip()
            unit_norm = "hours" if unit.lower().startswith(("hour","hr","h")) else "seconds" if unit.lower().startswith(("sec","s")) else "minutes"
            return "remind", {"message": msg, "rel": (unit_norm, n)}, 0.9
        if name == "remind_in":
            msg = extract_message_after_relative(t) or re.sub(rf"\b{REMIND_WORD}\b.*?(in|after|for)\b.*", "", t, flags=re.I).strip() or "Reminder"
            return "remind", {"message": msg, "rel": parse_time_relative(t)}, 0.88
        if name == "remind_at":
            msg = extract_message_after_at(t) or "Reminder"
            return "remind", {"message": msg, "at": parse_time_at(t)}, 0.88
        if name == "play_music":  return "play_music", {}, 0.9
        if name == "stop_music":  return "stop_music", {}, 0.9
        if name == "open_file_direct":
            return "open_url" if m.group(2).startswith("http") else ("open_file", {"target": m.group(2).strip()}, 0.9)
        if name == "ask_llm":            return "ask_llm", {"query": m.group(2).strip()}, 0.95
        if name == "explain_selection":  return "explain_selection", {}, 0.95
        if name == "summarize_selection":return "summarize_selection", {}, 0.95
        if name == "voice_start": return "voice_start", {"target": (m.group(2) or "").strip()}, 1.0
        if name == "voice_stop":  return "voice_stop", {}, 1.0
        if name == "voice_status": return "voice_status", {}, 1.0
        if name == "voice_devices": return "voice_devices", {}, 1.0
        if name == "voice_test": return "voice_test", {}, 1.0
        if name == "llm_status":   return "llm_status", {}, 1.0
        if name == "do_again":
            if CTX.last_intent: return CTX.last_intent, CTX.last_slots, 0.88
            return None, {}, 0.0
    cand = fuzzy_match_any_appphrase(t)
    if cand: return "open_app", {"app_raw": cand}, 0.72
    if t.endswith("?") or QUESTION_LIKE.search(t): return "ask_llm", {"query": raw_text.strip()}, 0.75
    m3 = re.search(r"\b(search|find|google)\b\s+(.+)$", t, re.I)
    if m3: return "search_web", {"query": m3.group(2).strip()}, 0.65
    return None, {}, 0.0

# --------- workspaces / exec ----------
DEFAULT_WORKSPACES = {
    "coding": [
        {"action":"open_app","app":"vscode"},
        {"action":"open_app","app":"terminal"},
        {"action":"open_url","url":"https://github.com/"},
        {"action":"open_app","app":"notes"},
    ],
    "study": [
        {"action":"open_app","app":"chrome" if "darwin" not in SYS and "mac" not in SYS else "safari"},
        {"action":"open_url","url":"https://scholar.google.com/"},
        {"action":"open_app","app":"notes"},
    ],
}
def load_workspaces() -> Dict[str, List[Dict[str, Any]]]:
    ws = dict(DEFAULT_WORKSPACES)
    if os.path.exists(WORKSPACES_FILE):
        try:
            with open(WORKSPACES_FILE,"r") as f: ws.update(json.load(f) or {})
        except Exception: pass
    return ws
def save_workspace(name: str, app_list: Optional[List[str]] = None):
    if app_list is None: app_list = CTX.last_opened_apps[-6:] or ["vscode","terminal"]
    ws = load_workspaces(); ws[name] = [{"action":"open_app","app":a} for a in app_list]
    try:
        with open(WORKSPACES_FILE,"w") as f:
            custom = {k:v for k,v in ws.items() if k not in DEFAULT_WORKSPACES or v != DEFAULT_WORKSPACES[k]}
            json.dump(custom, f, indent=2)
        print(f"[neuroos] Saved workspace '{name}' with apps: {', '.join(app_list)}"); speak(f"Saved workspace {name}.")
    except Exception as e:
        log_ex(e)

def exec_action(intent: str, slots: Dict):
    try:
        if intent == "open_workspace":
            ws_all = load_workspaces()
            ws = (slots.get("workspace") or CTX.last_workspace or "coding").lower()
            plan = ws_all.get(ws)
            if not plan: print(f"[neuroos] Unknown workspace: {ws}"); speak("Unknown workspace."); return
            print(f"[neuroos] Opening workspace: {ws}"); speak(f"Opening workspace {ws}"); CTX.last_workspace = ws
            for step in plan:
                if step["action"] == "open_app":
                    if open_app(step["app"]): CTX.last_opened_apps.append(step["app"])
                elif step["action"] == "open_url":
                    open_url(step["url"]); 
            return
        if intent == "save_workspace":
            save_workspace(slots.get("name") or f"ws_{int(time.time())}"); return
        if intent == "open_multi_apps":
            for raw in slots.get("apps_raw", []):
                if raw and open_app(raw): CTX.last_opened_apps.append(raw)
            return
        if intent == "open_app":
            target = slots.get("app_raw","")
            if open_app(target): CTX.last_opened_apps.append(target)
            return
        if intent == "open_url":
            print(f"[neuroos] Opening URL: {slots['url']}"); open_url(slots["url"]); return
        if intent == "search_web":
            q = slots["query"]; print(f"[neuroos] Searching: {q}"); search_web(q); return
        if intent == "note_text":
            body = slots.get("body","") or CTX.last_selection
            if not body: print("[neuroos] Nothing to add."); speak("Nothing to add."); return
            notes_create_or_append(slots.get("title","Quick Notes"), body); return
        if intent == "add_to_titled_note":
            body = slots.get("body","") or CTX.last_selection
            if not body: print("[neuroos] Nothing to add."); speak("Nothing to add."); return
            notes_create_or_append(slots.get("title","Quick Notes"), body); return
        if intent == "send_selection_to":
            dest = slots.get("dest","notes")
            sel = copy_selection(); CTX.last_selection = sel
            if not sel.strip(): print("[neuroos] No selection captured."); speak("No selection captured."); return
            if dest.startswith("note"): notes_create_or_append("Quick Notes", sel)
            elif dest.startswith("remind"): reminders_add(sel)
            elif dest == "textedit": textedit_new_with(sel)
            elif dest == "mail": mail_draft(None,"Note",sel)
            elif dest == "file":
                path = os.path.join(HOME, "Desktop", f"neuroos_{int(time.time())}.txt")
                with open(path,"w",encoding="utf-8") as f: f.write(sel)
                print(f"[neuroos] Wrote selection to file: {path}"); speak("Saved to file.")
            else: print(f"[neuroos] Unknown destination: {dest}"); speak("Unknown destination.")
            return
        if intent == "search_with_selection":
            sel = copy_selection(); CTX.last_selection = sel
            if not sel.strip(): print("[neuroos] No selection captured."); speak("No selection captured."); return
            print(f"[neuroos] Searching selection: {sel[:60]}{'...' if len(sel)>60 else ''}")
            search_web(sel); return
        if intent == "email_selection":
            sel = copy_selection() or CTX.last_selection
            if not sel.strip(): print("[neuroos] No selection captured."); speak("No selection captured."); return
            mail_draft(slots.get("to"), slots.get("subject","Note"), sel); return
        if intent == "remind":
            msg = slots.get("message","Reminder")
            if slots.get("at"): print(f"[neuroos] Reminder at {slots['at']}: {msg}"); reminders_add(msg, at_hhmm=slots["at"])
            elif slots.get("rel"):
                unit, n = slots["rel"]; print(f"[neuroos] Reminder in {n} {unit}: {msg}"); reminders_add(msg, delta_rel=slots["rel"])
            else: print("[neuroos] Reminder (no time)"); reminders_add(msg)
            return
        if intent == "play_music":  print("[neuroos] Play (best effort)"); music_play(); return
        if intent == "stop_music":  print("[neuroos] Pause (best effort)"); music_pause(); return
        if intent == "open_file":
            target = slots.get("target","")
            if target.startswith("http"): open_url(target); return
            try:
                if "darwin" in SYS or "mac" in SYS: subprocess.Popen(["open", target])
                elif "windows" in SYS: subprocess.Popen('start "" "{}"'.format(target), shell=True)
                else: subprocess.Popen(["xdg-open", target])
                print(f"[neuroos] Opening file: {target}")
            except Exception as e:
                log_ex(e)
            return
        if intent == "ask_llm":
            q = slots.get("query","").strip()
            if not q: print("[neuroos] Empty question."); return
            ans = LLM.answer(q)
            if ans: print(f"[llm] {ans}"); speak("Answered.")
            else:   print("[llm] Unavailable (install transformers+torch or set NEUROOS_HF_MODEL)."); speak("LLM unavailable.")
            return
        if intent == "explain_selection":
            sel = copy_selection() or CTX.last_selection
            if not sel.strip(): print("[neuroos] No selection captured."); speak("No selection captured."); return
            ans = LLM.answer("Explain in simple terms.", context=sel, max_new_tokens=200)
            if ans: print(f"[llm] {ans}"); return
            print("[llm] Unavailable."); return
        if intent == "summarize_selection":
            sel = copy_selection() or CTX.last_selection
            if not sel.strip(): print("[neuroos] No selection captured."); speak("No selection captured."); return
            ans = LLM.answer("Summarize the context in 3 bullet points.", context=sel, max_new_tokens=160)
            if ans: print(f"[llm] {ans}"); return
            print("[llm] Unavailable."); return
        if intent == "voice_devices": VOICE.list_devices(); return
        if intent == "voice_test": VOICE.test_record(); return
        if intent == "voice_start": VOICE.start(slots.get("target")); return
        if intent == "voice_stop":  VOICE.stop(); return
        if intent == "voice_status": print(VOICE.status()); return
        if intent == "llm_status": print(LLM.status()); return
        print("[neuroos] I don't know how to do that yet."); speak("I don't know how to do that yet.")
    except Exception as e:
        log_ex(e); print("[neuroos] (handled error)")

# --------- Voice engine (improved) ----------
class VoiceEngine:
    def __init__(self):
        self.running = False
        self.rec_thread: Optional[threading.Thread] = None
        self.dec_thread: Optional[threading.Thread] = None
        self.consume_thread: Optional[threading.Thread] = None
        self.seg_q: "queue.Queue[Tuple[bytes,int]]" = queue.Queue()  # (pcm16, sr)
        self.txt_q: "queue.Queue[str]" = queue.Queue()
        self.err: Optional[str] = None
        self.model = None
        self.input_device_index: Optional[int] = None
        self.input_device_name: Optional[str] = None
        self.stream_sr: int = 16000  # will adapt if needed

    def status(self) -> str:
        return "[voice] running={} device={} sr={} seg_q={} txt_q={} error={}".format(
            self.running, self.input_device_name or self.input_device_index, self.stream_sr,
            self.seg_q.qsize(), self.txt_q.qsize(), self.err or "none"
        )

    # ---- utilities ----
    def _find_device(self, target: Optional[str]) -> Tuple[Optional[int], Optional[str]]:
        import sounddevice as sd
        devices = sd.query_devices()
        default_idx = None
        try:
            default_pair = sd.default.device or (None, None)
            default_idx = default_pair[0]
        except Exception:
            default_idx = None

        # by env
        env_t = os.environ.get("NEUROOS_INPUT_DEVICE")
        target = target or env_t or ""

        # target numeric?
        if target:
            try:
                idx = int(target)
                if 0 <= idx < len(devices) and devices[idx]["max_input_channels"] > 0:
                    return idx, devices[idx]["name"]
            except Exception:
                pass
            # match by name fragment
            t = target.lower()
            for i, d in enumerate(devices):
                if d["max_input_channels"] > 0 and t in (d["name"] or "").lower():
                    return i, d["name"]

        # default input if valid
        if default_idx is not None:
            try:
                d = devices[default_idx]
                if d["max_input_channels"] > 0:
                    return default_idx, d["name"]
            except Exception:
                pass

        # first with input
        for i, d in enumerate(devices):
            if d["max_input_channels"] > 0:
                return i, d["name"]

        return None, None

    def list_devices(self):
        try:
            import sounddevice as sd
            devs = sd.query_devices()
            print("Input devices:")
            for i, d in enumerate(devs):
                if d["max_input_channels"] > 0:
                    print("  [{}] {}  (in={}, out={}, default_sr={})".format(
                        i, d["name"], d["max_input_channels"], d["max_output_channels"], int(d.get("default_samplerate") or 0)
                    ))
        except Exception as e:
            print("[voice] Could not list devices:", e)

    def test_record(self, seconds: int = 4):
        try:
            import sounddevice as sd, numpy as np
            idx, name = self._find_device(None)
            if idx is None:
                print("[voice] No input device with a microphone was found."); return
            sr_try = [16000, 48000, 44100]
            stream_sr = None
            for sr in sr_try:
                try:
                    with sd.InputStream(device=idx, samplerate=sr, channels=1, dtype="int16"): stream_sr = sr; break
                except Exception:
                    continue
            if stream_sr is None:
                print("[voice] Could not open stream at 16k/48k/44.1k. Check mic permissions."); return
            print(f"[voice] Recording {seconds}s from '{name}' at {stream_sr} Hz …")
            data = sd.rec(int(seconds*stream_sr), samplerate=stream_sr, channels=1, dtype="int16", device=idx)
            sd.wait()
            path = os.path.join(DATA_DIR, "voice_test.wav")
            Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
            with wave.open(path, "wb") as wf:
                wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(stream_sr)
                wf.writeframes(data.tobytes())
            print(f"[voice] Wrote {path}. Play it to confirm the mic works.")
        except Exception as e:
            print("[voice] test_record error:", e)
            if DEBUG: traceback.print_exc()

    # ---- resample to 16k for Whisper ----
    def _resample_to_16k(self, pcm_i16: bytes, sr_in: int) -> bytes:
        import numpy as np
        if sr_in == 16000:
            return pcm_i16
        arr = np.frombuffer(pcm_i16, dtype=np.int16).astype(np.float32)
        x = np.arange(len(arr))
        duration = len(arr) / sr_in
        n_out = int(duration * 16000)
        if n_out <= 0: return pcm_i16
        x_out = np.linspace(0, len(arr)-1, n_out)
        y = np.interp(x_out, x, arr)
        y16 = np.clip(y, -32768, 32767).astype(np.int16)
        return y16.tobytes()

    def start(self, target: Optional[str] = None):
        if self.running:
            print("[voice] already running."); return
        try:
            import sounddevice as sd  # noqa
            import numpy as np        # noqa
        except Exception:
            print("[voice] Missing modules. Install: pip install sounddevice numpy"); return
        try:
            from faster_whisper import WhisperModel  # noqa
        except Exception:
            print("[voice] Missing faster-whisper. Install: pip install faster-whisper"); return

        # load model
        model_size = os.environ.get("NEUROOS_WHISPER_PATH") or os.environ.get("NEUROOS_WHISPER_SIZE", "small.en")
        compute = os.environ.get("NEUROOS_WHISPER_COMPUTE", "int8")
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(model_size, device="cpu", compute_type=compute)
        except Exception as e:
            self.err = "whisper load failed: {}".format(e); log_ex(e)
            print("[voice] Could not load Whisper. Try: export NEUROOS_WHISPER_SIZE=tiny.en"); return

        # pick input device
        idx, name = self._find_device(target)
        if idx is None:
            print("[voice] No input device found. Run: voice devices  (and ensure mic permissions)"); return
        self.input_device_index, self.input_device_name = idx, name

        # pick sample rate: 16k then 48k then 44.1k
        import sounddevice as sd
        sr_try = [16000, 48000, 44100]
        chosen_sr = None
        for sr in sr_try:
            try:
                with sd.InputStream(device=idx, samplerate=sr, channels=1, dtype="int16"):
                    chosen_sr = sr; break
            except Exception as e:
                dbg("stream open failed at {} Hz: {}".format(sr, e))
                continue
        if chosen_sr is None:
            print("[voice] Could not open microphone stream at 16k/48k/44.1k. Check permissions in OS settings.")
            return
        self.stream_sr = chosen_sr
        print("[voice] using device '{}' (index {}) at {} Hz".format(name, idx, chosen_sr))

        # threads
        self.running = True; self.err = None
        self.rec_thread = threading.Thread(target=self._recorder, daemon=True)
        self.dec_thread = threading.Thread(target=self._decoder, daemon=True)
        self.consume_thread = threading.Thread(target=self._consumer, daemon=True)
        self.rec_thread.start(); self.dec_thread.start(); self.consume_thread.start()
        print("[voice] started."); speak("Voice started.")

    def stop(self):
        if not self.running:
            print("[voice] already stopped."); return
        self.running = False
        print("[voice] stopping…"); speak("Voice stopped.")

    def _recorder(self):
        try:
            import sounddevice as sd, numpy as np
            # VAD
            vad = None; use_vad = False
            try:
                import webrtcvad
                # VAD supports 8000/16000/32000/48000
                if self.stream_sr in (8000,16000,32000,48000):
                    vad = webrtcvad.Vad(2); use_vad = True; dbg("using webrtcvad at {} Hz".format(self.stream_sr))
                else:
                    dbg("VAD disabled (sr={} not supported)".format(self.stream_sr))
            except Exception:
                dbg("webrtcvad unavailable; using RMS threshold")

            block_ms = 20
            block_size = int(self.stream_sr * block_ms / 1000)

            def is_speech(frame_i16: bytes) -> bool:
                if use_vad:
                    try: return vad.is_speech(frame_i16, self.stream_sr)
                    except Exception: return False
                arr = np.frombuffer(frame_i16, dtype=np.int16)
                rms = float(np.sqrt(np.mean(arr.astype(np.float32)**2)) + 1e-8)
                return rms > 200  # lowered threshold

            max_segment_ms = 12000
            silence_end_ms = 700

            with sd.RawInputStream(samplerate=self.stream_sr, blocksize=block_size, dtype='int16', channels=1, device=self.input_device_index) as istream:
                print("[voice] Listening… (say: 'open chrome', 'what is a mutex?')")
                collecting = False
                seg = bytearray(); speech_ms=0; silence_ms=0

                while self.running:
                    data, overflowed = istream.read(block_size)
                    if overflowed and DEBUG: dbg("input overflow")
                    if not data: continue

                    if is_speech(data):
                        seg.extend(data); speech_ms += block_ms; silence_ms = 0; collecting = True
                    else:
                        if collecting:
                            silence_ms += block_ms; seg.extend(data)

                    if collecting and (silence_ms >= silence_end_ms or speech_ms >= max_segment_ms):
                        if len(seg) > block_size * 5:
                            # enqueue (pcm, sr)
                            self.seg_q.put((bytes(seg), self.stream_sr))
                            dbg("segment queued (~{:.2f}s)".format(len(seg)/2/self.stream_sr))
                        seg = bytearray(); collecting=False; speech_ms=0; silence_ms=0
        except Exception as e:
            self.err = str(e); log_ex(e)
            print("[voice] recorder error:", e)

    def _decoder(self):
        try:
            import numpy as np
            from faster_whisper import WhisperModel
            model: WhisperModel = self.model  # type: ignore
            while self.running:
                try:
                    pcm, sr_in = self.seg_q.get(timeout=0.25)
                except queue.Empty:
                    continue
                try:
                    # resample to 16k if needed
                    if sr_in != 16000:
                        pcm = self._resample_to_16k(pcm, sr_in)
                        sr_in = 16000
                    arr = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)/32768.0
                    segments, info = model.transcribe(arr, language="en", task="transcribe", beam_size=1, vad_filter=False)
                    text = "".join(seg.text for seg in segments).strip()
                    if text:
                        self.txt_q.put(text); dbg("decoded: {}".format(text))
                except Exception as e:
                    dbg("decode err: {}".format(e))
        except Exception as e:
            self.err = str(e); log_ex(e)

    def _consumer(self):
        while self.running:
            try:
                text = self.txt_q.get(timeout=0.25)
            except queue.Empty:
                continue
            try:
                print(f"\n🎤 {text}")
                process_line(text)
            except Exception as e:
                log_ex(e)

VOICE = VoiceEngine()

# --------- CLI ----------
CHAIN_SEPS = re.compile(r"\s*(?:;|&&| and then | then | \| )\s*", re.I)
def split_commands(raw: str) -> List[str]:
    return [p.strip() for p in CHAIN_SEPS.split(raw.strip()) if p.strip()]

BANNER = """NeuroOS — Cross-Platform (Text + offline voice + local LLM)
Examples:
  voice devices | voice start | voice start 2 | voice start macbook microphone
  voice test | voice status | voice stop
  open chrome | open vscode | open vscode and terminal and notes
  open workspace coding | save workspace myfocus | open workspace myfocus
  send selection to notes | email selection to you@example.com subject Research
  search this (select text first)
  take note: meeting at 6 | add fix login bug to note TODOs
  remind me in 20 seconds to stretch | remind me at 8:30 pm to practice
  ask what is a mutex? | what is the capital of India?
Type 'exit' to quit.
"""

def process_line(raw: str):
    commands = split_commands(raw)
    for cmd in commands:
        try:
            intent, slots, _ = parse_intent(cmd)
            if not intent:
                target = fuzzy_match_any_appphrase(normalize_text(cmd))
                if target:
                    exec_action("open_app", {"app_raw": target})
                    CTX.last_intent, CTX.last_slots = "open_app", {"app_raw": target}
                else:
                    print("[neuroos] Sorry, I didn't get that."); speak("Sorry, I didn't get that.")
                continue
            exec_action(intent, slots)
            CTX.last_intent, CTX.last_slots = intent, slots
        except Exception as e:
            log_ex(e); print("[neuroos] (handled error)")

def main():
    print(BANNER)
    sysname = platform.system()
    print("[neuroos] OS: {} | Voice model: {} | compute: {}".format(
        sysname, os.environ.get('NEUROOS_WHISPER_PATH') or os.environ.get('NEUROOS_WHISPER_SIZE','small.en'),
        os.environ.get('NEUROOS_WHISPER_COMPUTE','int8')
    ))
    print(LLM.status())
    while True:
        try:
            raw = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nbye."); VOICE.stop(); return
        except Exception as e:
            log_ex(e); continue
        if not raw: continue
        if raw.strip().lower() in ("exit","quit"):
            VOICE.stop(); print("bye."); return
        process_line(raw)

if __name__ == "__main__":
    main()
