"""Build and save vector database from your PDFs"""

import warnings
warnings.filterwarnings('ignore')

from src.document_processor import DocumentProcessor
from src.embeddings_hf import EmbeddingGenerator
from src.vector_store import VectorStore

print("=" * 60)
print("🏗️  Building Vector Database")
print("=" * 60)

# Step 1: Load documents
print("\n📚 STEP 1: Loading PDFs")
print("-" * 60)

processor = DocumentProcessor()
file_paths = [
    "sample_docs/RAND_RR487z1_english.pdf",
    "sample_docs/RAND_RR1562z1.arabic.pdf",
    "sample_docs/RAND_RR1681z1.arabic.pdf",
    "sample_docs/RAND_RRA3540-1_english.pdf",
    
]

chunks = processor.load_documents(file_paths)
print(f"✅ Loaded {len(chunks)} chunks")

# Step 2: Generate embeddings
print("\n🧮 STEP 2: Generating Embeddings")
print("-" * 60)

embedder = EmbeddingGenerator()
texts, embeddings, metadatas = embedder.embed_documents(chunks)
print(f"✅ Generated {len(embeddings)} embeddings")

# Step 3: Build vector store
print("\n💾 STEP 3: Building Vector Store")
print("-" * 60)

vector_store = VectorStore(dimension=1024)
vector_store.add_documents(texts, embeddings, metadatas)

# Step 4: Save to disk
print("\n💿 STEP 4: Saving to Disk")
print("-" * 60)

save_path = "vector_store"
vector_store.save(save_path)

print("\n" + "=" * 60)
print("✅ Vector Database Built & Saved!")
print("=" * 60)
print(f"📂 Location: {save_path}/")
print(f"📊 Total documents: {len(chunks)}")
print(f"📐 Dimension: 384")
print(f"💾 Files created:")
print(f"   - {save_path}/index.faiss")
print(f"   - {save_path}/data.pkl")
print("=" * 60)