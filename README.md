## RedTool: Redteam Framework

This repository contains a small command-and-control client and payload used for security research and penetration testing labs.

### Project Structure

```
project-skeleton
├── client
│   ├── app.py
│   └── cybersploit_client
│       ├── commands
│       └── util
├── payload
│   └── server.py
```

The `client` directory contains the operator tooling that initiates connections and issues commands.

The `payload` directory contains the code that runs on a target host.

### Configuration

Copy `client/cybersploit_client/util/config.py.example` to `client/cybersploit_client/util/config.py` and update:

- `DEFAULT_IP` to the target listener IP (`TARGET_IP`)
- `DEFAULT_PORT` if you are not using the default port
- SMTP settings if you intend to use the phishing email module

### Dependencies

If you want to use the client's screenshot command, you'll need to install Pillow:

```bash
pip install Pillow
```

### Security Disclaimer

This framework is provided **solely for educational purposes and authorized security testing**.  
You must **only** deploy and run this code on systems for which you have **explicit written permission** from the owner.  
The authors and maintainers accept **no responsibility or liability** for any misuse, damage, or legal issues arising from the use of this software.

© 2026 Lyric Hagen, Nessa Lee, Kelvin Xu, Sanya Badhe. All rights reserved. This project was created by Lyric Hagen, Nessa Lee, Kelvin Xu, and Sanya Badhe. Do not present or distribute as your own work.
