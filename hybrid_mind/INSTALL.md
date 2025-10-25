# Installation Guide

## Overview

Hybrid Mind requires **Ollama** running locally with the **llama3:8b** model. This guide covers setup for all platforms.

---

## Step 1: Install Ollama

### Mac
```bash
curl https://ollama.ai/install.sh | sh
```

### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

### Windows
1. Download installer from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Follow the installation wizard

---

## Step 2: Download the Model

Once Ollama is installed, download the required model:

```bash
ollama pull llama3:8b
```

**Note:** This downloads approximately **4.7GB**. Depending on your internet connection, this may take several minutes.

---

## Step 3: Start Ollama Server

In a terminal window, start the Ollama server:

```bash
ollama serve
```

**Keep this terminal window open** while using Hybrid Mind. The server must be running for the system to work.

---

## Step 4: Verify Installation

Open a **new terminal window** (keep the server running in the first one) and verify:

```bash
ollama list
```

You should see `llama3:8b` in the output. Example:
```
NAME            ID              SIZE    MODIFIED
llama3:8b       a6990ed6be41    4.7 GB  2 minutes ago
```

---

## Step 5: Test Connection

Run a quick test to ensure Ollama is responding:

```bash
ollama run llama3:8b "Hello, are you working?"
```

If you get a response, you're ready to use Hybrid Mind!

---

## Step 6: Run Hybrid Mind

Navigate to the `hybrid_mind` directory and start with observation:

```bash
cd hybrid_mind
python mind_observer.py
```

You should see the system:
1. Creating antifragile base glyphs
2. Spawning test glyphs
3. Analyzing system state
4. Generating observations

Output will be saved to the `observations/` folder.

---

## Quick Start Workflow

Once installed, here's the recommended first-time flow:

```bash
# 1. Let it observe itself
python mind_observer.py

# 2. Chat about what it found
python mind_chat.py
# Type: "What did you observe?"
# Type: "exit" when done

# 3. See what code it proposes
python mind_coder.py

# 4. Run the full autonomous loop (interactive mode)
python mind_loop.py 1 interactive
```

---

## Troubleshooting

### "Connection refused" or "Cannot connect to Ollama"

**Problem:** Ollama server isn't running

**Solution:**
```bash
ollama serve
```
Keep this running in a separate terminal

---

### "Model 'llama3:8b' not found"

**Problem:** Model hasn't been downloaded

**Solution:**
```bash
ollama pull llama3:8b
```
Wait for the download to complete (4.7GB)

---

### "Module not found" errors when running Python

**Problem:** You're not in the right directory or dependencies are missing

**Solution:**
```bash
# Make sure you're in the hybrid_mind directory
cd hybrid_mind

# Verify Python version (need 3.8+)
python --version

# If using virtual environment (optional):
python -m venv env
source env/bin/activate  # Mac/Linux
# OR
env\Scripts\activate  # Windows
```

---

### "Permission denied" (Mac/Linux)

**Problem:** Ollama installation needs elevated privileges

**Solution:**
```bash
# Try with sudo
curl https://ollama.ai/install.sh | sudo sh

# Or install to user directory
curl https://ollama.ai/install.sh | sh --prefix=$HOME/.local
```

---

### Port 11434 already in use

**Problem:** Another process is using Ollama's default port

**Solution:**
```bash
# Find what's using the port (Mac/Linux)
lsof -i :11434

# Kill the process or use a different port
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

---

### Slow responses or timeouts

**Problem:** System doesn't have enough resources

**Solution:**
- Close other applications
- Ensure you have at least 8GB RAM available
- Consider using a smaller model if performance is poor:
  ```bash
  ollama pull llama3:8b-q4_0  # Smaller quantized version
  ```

---

### Python version too old

**Problem:** Need Python 3.8 or higher

**Solution:**
```bash
# Check version
python --version

# If too old, install newer Python:
# Mac: brew install python@3.11
# Linux: sudo apt install python3.11
# Windows: Download from python.org
```

---

## System Requirements

### Minimum Requirements
- **CPU:** Modern multi-core processor
- **RAM:** 8GB (system needs ~4GB for llama3:8b)
- **Disk:** 10GB free space (5GB for model + workspace)
- **OS:** macOS 10.15+, Ubuntu 20.04+, Windows 10+
- **Python:** 3.8 or higher

### Recommended Requirements
- **RAM:** 16GB or more
- **Disk:** SSD for better model loading performance
- **CPU:** 8+ cores for faster inference

---

## Alternative: Use Custom GPT

If you don't want to install anything locally, you can try the **Custom GPT version** which doesn't require any setup:

[Link to Glyphwheel Mind v22 Custom GPT - to be added]

The Custom GPT has limited capabilities compared to the full Hybrid Mind system, but it's perfect for quick experimentation.

---

## Next Steps

Once everything is installed and working:

1. Read the [README.md](README.md) for full documentation
2. Start with `mind_observer.py` to see the system in action
3. Explore the other phases: chat, coder, and loop
4. Check the `observations/` and `proposals/` folders to see what the mind produces

---

## Getting Help

If you run into issues not covered here:

1. **Check Ollama docs:** [ollama.ai/docs](https://ollama.ai)
2. **Open an issue** on GitHub with:
   - Your OS and Python version
   - Error messages
   - What you were trying to do
3. **Review the logs** in the `observations/` folder for clues

---

## Uninstallation

If you want to remove Ollama:

### Mac/Linux
```bash
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf ~/.ollama
```

### Windows
Use "Add or Remove Programs" to uninstall Ollama

The model data is stored in:
- Mac/Linux: `~/.ollama/models`
- Windows: `%USERPROFILE%\.ollama\models`

Delete this folder to free up the ~5GB of disk space.

---

## Support

- **Ollama Support:** [ollama.ai](https://ollama.ai)
- **Python Support:** [python.org](https://python.org)
- **Hybrid Mind Issues:** [GitHub Issues]

---

*Happy experimenting! 🧠⚡*

---

**Installation complete?** → Continue to [README.md](README.md) for usage instructions
