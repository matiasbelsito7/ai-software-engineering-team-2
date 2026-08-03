```python
"""
Shared public API.

This package contains the common building blocks shared across the entire
application:

- Type aliases
- Enumerations
- Protocols
- Constants

Only stable, reusable definitions should be re-exported here.
"""

from ai_team.shared.constants import *
from ai_team.shared.protocols import *
from ai_team.shared.types import *

__all__ = [
    # Intentionally populated by the imported modules.
]
```
