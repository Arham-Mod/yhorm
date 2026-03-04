from core.retrieval.retriever import Retriever
from core.retrieval.dependency_expander import DependencyExpander
from core.context_builder.build_context import ContextBuilder


class RepoIntelligencePipeline:
    """
    Orchestrates retrieval + context building.
    """

    def __init__(
        self,
        embedder,
        vector_store,
        metadata_store,
    ):
        # Build dependency expander
        self.dependency_expander = DependencyExpander(metadata_store)

        # Build retriever
        self.retriever = Retriever(
            embedder=embedder,
            vector_store=vector_store,
            metadata_store=metadata_store,
            dependency_expander=self.dependency_expander,
        )

        # Build context builder
        self.context_builder = ContextBuilder()

    def run(self, query: str):
        print("\n🔎 Running Query:", query)

        # 1. Retrieve chunks
        chunks = self.retriever.retrieve(query)

        print(f"\n📦 Retrieved {len(chunks)} chunks after expansion")

        # 2. Build structured context
        context = self.context_builder.build(chunks)

        return {
            "context": context,
            "chunks": chunks,
        }