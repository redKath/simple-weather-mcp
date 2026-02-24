# A Simple MCP Weather Server written in Python

# Claude Desktop - Config (WSL)
```json
{
  "mcpServers": {
    "weather": {
      "command": "wsl.exe",
      "args": [
        "-e",
        "/home/kchan/.local/bin/uv",
        "--directory",
        "/home/kchan/Tutorials/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

# Screenshots - Local Test
<img width="1920" height="1020" alt="Screenshot 2026-02-24 184106" src="https://github.com/user-attachments/assets/9a3a155a-0ce6-4f40-9fe3-d9d16c0e6b85" />

<img width="1920" height="1020" alt="Screenshot 2026-02-24 184116" src="https://github.com/user-attachments/assets/26022496-3066-4a10-9a01-7f6ebccce1c5" />


Reference: [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server)
