"""
RAG System Evaluation Script
Tests retrieval quality, embedding performance, and system metrics
"""

import time
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

from src.embeddings_hf import EmbeddingGenerator
from src.vector_store import VectorStore
from test_cases import create_test_cases


class RAGEvaluator:
    """Evaluate RAG system retrieval performance"""
    
    def __init__(self, vector_store_path: str = "vector_store"):
        """Initialize evaluator with vector store"""
        print("=" * 70)
        print("RAG SYSTEM EVALUATION")
        print("=" * 70)
        
        # Load components
        print("\n📥 Loading vector store...")
        self.vector_store = VectorStore(dimension=1024)
        self.vector_store.load(vector_store_path)
        
        print("📥 Loading embedding model...")
        self.embedder = EmbeddingGenerator(model_name="intfloat/multilingual-e5-large")
        
        print("\n✅ System loaded successfully")
        print(f"   Documents in store: {len(self.vector_store.texts)}")
        print(f"   Embedding dimension: {self.embedder.dimension}")
    
        
    def calculate_precision_at_k(self, results: List[Dict], expected_source: str, k: int = 5) -> float:
        """Calculate Precision@K"""
        if expected_source is None:
            return None  # Can't calculate without ground truth
        
        relevant_count = 0
        for result in results[:k]:
            if expected_source in result['metadata'].get('source_file', ''):
                relevant_count += 1
        
        return relevant_count / k
    
    def calculate_mrr(self, results: List[Dict], expected_source: str) -> float:
        """Calculate Mean Reciprocal Rank"""
        if expected_source is None:
            return None
        
        for rank, result in enumerate(results, 1):
            if expected_source in result['metadata'].get('source_file', ''):
                return 1.0 / rank
        
        return 0.0  # Not found
    
    def test_retrieval_quality(self, test_cases: List[Dict], k: int = 3) -> Dict:
        """Test retrieval performance"""
        print("\n" + "=" * 70)
        print("TEST 1: RETRIEVAL QUALITY")
        print("=" * 70)
        
        results = {
            'precision_scores': [],
            'mrr_scores': [],
            'distances': [],
            'response_times': []
        }
        
        for i, test_case in enumerate(test_cases, 1):
            query = test_case['query']
            expected_source = test_case['expected_source']
            
            print(f"\n[{i}/{len(test_cases)}] Testing: {query[:50]}...")
            
            # Measure retrieval time
            start_time = time.time()
            query_embedding = self.embedder.generate_embedding(query)
            retrieved = self.vector_store.search(query_embedding, k=k)
            elapsed = time.time() - start_time
            
            results['response_times'].append(elapsed)
            
            # Calculate metrics
            if expected_source:
                precision = self.calculate_precision_at_k(retrieved, expected_source, k)
                mrr = self.calculate_mrr(retrieved, expected_source)
                
                if precision is not None:
                    results['precision_scores'].append(precision)
                if mrr is not None:
                    results['mrr_scores'].append(mrr)
            
            # Store best distance
            if retrieved:
                best_distance = retrieved[0]['distance']
                results['distances'].append(best_distance)
                
                print(f"   Best distance: {best_distance:.4f}")
                print(f"   Top source: {retrieved[0]['metadata'].get('source_file', 'Unknown')}")
                if expected_source:
                    print(f"   Precision@{k}: {precision:.2f}")
                    print(f"   MRR: {mrr:.2f}")
        
        # Calculate averages
        avg_precision = np.mean(results['precision_scores']) if results['precision_scores'] else 0
        avg_mrr = np.mean(results['mrr_scores']) if results['mrr_scores'] else 0
        avg_distance = np.mean(results['distances'])
        avg_time = np.mean(results['response_times'])
        
        print("\n" + "-" * 70)
        print("RETRIEVAL QUALITY SUMMARY:")
        print("-" * 70)
        print(f"Average Precision@{k}: {avg_precision:.3f} ({avg_precision*100:.1f}%)")
        print(f"Average MRR: {avg_mrr:.3f}")
        print(f"Average Best Distance: {avg_distance:.4f}")
        print(f"Average Response Time: {avg_time:.3f}s")
        
        return results
    
    def test_threshold_accuracy(self, test_cases: List[Dict], threshold: float = 0.6) -> Dict:
        """Test no-info detection threshold"""
        print("\n" + "=" * 70)
        print("TEST 2: THRESHOLD ACCURACY (No-Info Detection)")
        print("=" * 70)
        print(f"Threshold: {threshold}")
        
        answerable_queries = [tc for tc in test_cases if tc['answerable']]
        unanswerable_queries = [tc for tc in test_cases if not tc['answerable']]
        
        true_positives = 0  # Answerable and passes threshold
        false_negatives = 0  # Answerable but fails threshold
        true_negatives = 0  # Unanswerable and fails threshold
        false_positives = 0  # Unanswerable but passes threshold
        
        print(f"\nTesting {len(answerable_queries)} answerable queries...")
        for test_case in answerable_queries:
            query_embedding = self.embedder.generate_embedding(test_case['query'])
            results = self.vector_store.search(query_embedding, k=1)
            
            if results:
                distance = results[0]['distance']
                if distance < threshold:
                    true_positives += 1
                else:
                    false_negatives += 1
                    print(f"   ❌ False Negative: '{test_case['query'][:40]}...' (distance: {distance:.4f})")
        
        print(f"\nTesting {len(unanswerable_queries)} unanswerable queries...")
        for test_case in unanswerable_queries:
            query_embedding = self.embedder.generate_embedding(test_case['query'])
            results = self.vector_store.search(query_embedding, k=1)
            
            if results:
                distance = results[0]['distance']
                if distance >= threshold:
                    true_negatives += 1
                else:
                    false_positives += 1
                    print(f"   ⚠️  False Positive: '{test_case['query'][:40]}...' (distance: {distance:.4f})")
        
        # Calculate metrics
        total = len(test_cases)
        accuracy = (true_positives + true_negatives) / total
        
        if (true_positives + false_negatives) > 0:
            recall = true_positives / (true_positives + false_negatives)
        else:
            recall = 0
        
        if (true_positives + false_positives) > 0:
            precision = true_positives / (true_positives + false_positives)
        else:
            precision = 0
        
        print("\n" + "-" * 70)
        print("THRESHOLD ACCURACY SUMMARY:")
        print("-" * 70)
        print(f"True Positives (Correct Accept): {true_positives}/{len(answerable_queries)}")
        print(f"False Negatives (Incorrect Reject): {false_negatives}/{len(answerable_queries)}")
        print(f"True Negatives (Correct Reject): {true_negatives}/{len(unanswerable_queries)}")
        print(f"False Positives (Incorrect Accept): {false_positives}/{len(unanswerable_queries)}")
        print(f"\nOverall Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        print(f"Precision: {precision:.3f} ({precision*100:.1f}%)")
        print(f"Recall: {recall:.3f} ({recall*100:.1f}%)")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'tp': true_positives,
            'fp': false_positives,
            'tn': true_negatives,
            'fn': false_negatives
        }
    
    def test_cross_lingual_performance(self, test_cases: List[Dict]) -> Dict:
        """Test cross-lingual retrieval"""
        print("\n" + "=" * 70)
        print("TEST 3: CROSS-LINGUAL PERFORMANCE")
        print("=" * 70)
        
        # Group by language combination
        same_language = []
        cross_language = []
        
        for test_case in test_cases:
            if test_case['type'] == 'cross-lingual':
                cross_language.append(test_case)
            elif test_case['answerable']:
                same_language.append(test_case)
        
        print(f"\nSame-language queries: {len(same_language)}")
        print(f"Cross-lingual queries: {len(cross_language)}")
        
        # Test same-language
        same_lang_distances = []
        for test_case in same_language:
            query_embedding = self.embedder.generate_embedding(test_case['query'])
            results = self.vector_store.search(query_embedding, k=3)
            if results:
                same_lang_distances.append(results[0]['distance'])
        
        # Test cross-lingual
        cross_lang_distances = []
        for test_case in cross_language:
            query_embedding = self.embedder.generate_embedding(test_case['query'])
            results = self.vector_store.search(query_embedding, k=3)
            if results:
                cross_lang_distances.append(results[0]['distance'])
                print(f"\n   Query: {test_case['query'][:50]}...")
                print(f"   Best match: {results[0]['metadata'].get('source_file', 'Unknown')}")
                print(f"   Distance: {results[0]['distance']:.4f}")
        
        avg_same = np.mean(same_lang_distances) if same_lang_distances else 0
        avg_cross = np.mean(cross_lang_distances) if cross_lang_distances else 0
        
        print("\n" + "-" * 70)
        print("CROSS-LINGUAL SUMMARY:")
        print("-" * 70)
        print(f"Same-language avg distance: {avg_same:.4f}")
        print(f"Cross-lingual avg distance: {avg_cross:.4f}")
        print(f"Performance gap: {((avg_cross - avg_same) / avg_same * 100):.1f}% worse")
        
        return {
            'same_language_distance': avg_same,
            'cross_language_distance': avg_cross,
            'performance_gap': avg_cross - avg_same
        }
    
    def test_embedding_speed(self, num_texts: int = 100) -> Dict:
        """Test embedding generation speed"""
        print("\n" + "=" * 70)
        print("TEST 4: EMBEDDING PERFORMANCE")
        print("=" * 70)
        
        # Sample texts from vector store
        sample_texts = self.vector_store.texts[:num_texts]
        
        print(f"\nGenerating embeddings for {num_texts} texts...")
        
        # Single embedding
        start = time.time()
        self.embedder.generate_embedding(sample_texts[0])
        single_time = time.time() - start
        
        # Batch embedding
        start = time.time()
        self.embedder.generate_embeddings_batch(sample_texts)
        batch_time = time.time() - start
        
        time_per_text_single = single_time
        time_per_text_batch = batch_time / num_texts
        speedup = time_per_text_single / time_per_text_batch
        
        print("\n" + "-" * 70)
        print("EMBEDDING PERFORMANCE SUMMARY:")
        print("-" * 70)
        print(f"Single embedding: {single_time:.4f}s")
        print(f"Batch ({num_texts} texts): {batch_time:.4f}s")
        print(f"Time per text (single): {time_per_text_single:.4f}s")
        print(f"Time per text (batch): {time_per_text_batch:.4f}s")
        print(f"Batch speedup: {speedup:.1f}x faster")
        
        return {
            'single_time': single_time,
            'batch_time': batch_time,
            'speedup': speedup
        }
    
    def run_all_tests(self):
        """Run complete evaluation suite"""
        print("\n🧪 Starting RAG System Evaluation")
        print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Create test cases
        test_cases = create_test_cases()
        print(f"✅ Created {len(test_cases)} test cases")
        
        # Run tests
        retrieval_results = self.test_retrieval_quality(test_cases, k=6)
        threshold_results = self.test_threshold_accuracy(test_cases, threshold=0.6)
        crosslingual_results = self.test_cross_lingual_performance(test_cases)
        embedding_results = self.test_embedding_speed(num_texts=100)
        
        # Final summary
        print("\n" + "=" * 70)
        print("FINAL EVALUATION SUMMARY")
        print("=" * 70)
        print("\n📊 Key Metrics:")
        print(f"   Retrieval Precision@3: {np.mean(retrieval_results['precision_scores']):.3f}")
        print(f"   Retrieval MRR: {np.mean(retrieval_results['mrr_scores']):.3f}")
        print(f"   Threshold Accuracy: {threshold_results['accuracy']:.3f}")
        print(f"   Cross-lingual Gap: {crosslingual_results['performance_gap']:.4f}")
        print(f"   Avg Response Time: {np.mean(retrieval_results['response_times']):.3f}s")
        print(f"   Batch Speedup: {embedding_results['speedup']:.1f}x")
        
        print("\n✅ Evaluation complete!")


if __name__ == "__main__":
    # Run evaluation
    evaluator = RAGEvaluator(vector_store_path="vector_store")
    evaluator.run_all_tests()