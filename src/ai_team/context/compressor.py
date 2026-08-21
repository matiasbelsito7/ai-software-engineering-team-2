"""
Context compressor.
"""

from __future__ import annotations

from ai_team.context.exceptions import ContextCompressionError
from ai_team.context.models import ContextSelection


class ContextCompressor:
    """
    Compresses the selected context so that it fits
    within the target context window.
    """

    def __init__(
        self,
        *,
        max_messages: int = 15,
        max_memories: int = 8,
        max_documents: int = 8,
    ) -> None:

        self._max_messages = max_messages

        self._max_memories = max_memories

        self._max_documents = max_documents

    async def compress(
        self,
        selection: ContextSelection,
    ) -> ContextSelection:
        """
        Compress the context.

        Truncates each section to the configured limits and records
        compression statistics in metadata.
        """

        try:
            conv_before = len(selection.conversation)
            mem_before = len(selection.memories)
            doc_before = len(selection.documents)

            compressed_conv = selection.conversation[-self._max_messages :]
            compressed_mem = selection.memories[: self._max_memories]
            compressed_doc = selection.documents[: self._max_documents]

            total_before = conv_before + mem_before + doc_before
            total_after = len(compressed_conv) + len(compressed_mem) + len(compressed_doc)

            metadata = {
                **selection.metadata,
                "compression": {
                    "conversation_before": conv_before,
                    "conversation_after": len(compressed_conv),
                    "memories_before": mem_before,
                    "memories_after": len(compressed_mem),
                    "documents_before": doc_before,
                    "documents_after": len(compressed_doc),
                    "total_before": total_before,
                    "total_after": total_after,
                    "ratio": total_after / total_before if total_before > 0 else 1.0,
                },
            }

            return ContextSelection(
                conversation=compressed_conv,
                memories=compressed_mem,
                documents=compressed_doc,
                metadata=metadata,
            )
        except Exception as exc:
            raise ContextCompressionError(
                f"Failed to compress context: {exc}",
            ) from exc
