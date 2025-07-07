#!/usr/bin/env python
"""Development server runner"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "sentinel.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
    )