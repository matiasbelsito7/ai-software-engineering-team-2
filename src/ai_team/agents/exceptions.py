class AgentError(Exception):
    """Base exception for all agent errors."""


class AgentExecutionError(AgentError):
    """Raised when an agent execution fails."""


class AgentValidationError(AgentError):
    """Raised when an invalid request is received."""


class AgentConfigurationError(AgentError):
    """Raised when an agent is misconfigured."""


class AgentRegistrationError(AgentError):
    """Raised when an agent cannot be registered."""


class AgentNotFoundError(AgentError):
    """Raised when an agent cannot be found."""


class AgentCapabilityError(AgentError):
    """Raised when an agent does not support a capability."""


class ToolExecutionError(AgentError):
    """Raised when a tool invocation fails."""
