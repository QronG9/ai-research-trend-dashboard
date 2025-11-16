"""
Frontend and Cloud Function share the same list of AI sub-directions.
Copy of src/config/directions.py for Cloud Function packaging.
"""
from __future__ import annotations

DIRECTIONS = [
    {
        "name": "Natural Language Processing",
        "concept_id": "https://openalex.org/C154945302",
        "keywords": ["natural language processing", "nlp"],
    },
    {
        "name": "Large Language Models (LLM)",
        "concept_id": None,
        "keywords": ["large language model", "LLM"],
    },
    {
        "name": "Vision-Language Models (VLM)",
        "concept_id": None,
        "keywords": ["vision-language", "VLM", "vision language model"],
    },
    {
        "name": "Video LLM",
        "concept_id": None,
        "keywords": ["video LLM", "video-language model", "video language model"],
    },
    {
        "name": "Retrieval-Augmented Generation (RAG)",
        "concept_id": None,
        "keywords": ["retrieval augmented generation", "RAG"],
    },
    {
        "name": "Graph Neural Networks (GNN)",
        "concept_id": None,
        "keywords": ["graph neural network", "GNN"],
    },
    {
        "name": "Graph Representation Learning",
        "concept_id": None,
        "keywords": ["graph representation learning"],
    },
    {
        "name": "Causal Machine Learning",
        "concept_id": None,
        "keywords": ["causal machine learning", "causal ML"],
    },
    {
        "name": "Causal Inference",
        "concept_id": None,
        "keywords": ["causal inference"],
    },
    {
        "name": "Reinforcement Learning",
        "concept_id": "https://openalex.org/C127413603",
        "keywords": ["reinforcement learning"],
    },
    {
        "name": "Deep Reinforcement Learning",
        "concept_id": None,
        "keywords": ["deep reinforcement learning"],
    },
    {
        "name": "Prompt Engineering",
        "concept_id": None,
        "keywords": ["prompt engineering"],
    },
    {
        "name": "Instruction Tuning",
        "concept_id": None,
        "keywords": ["instruction tuning", "instruction fine-tuning"],
    },
    {
        "name": "AI Alignment",
        "concept_id": None,
        "keywords": ["AI alignment"],
    },
    {
        "name": "RLHF",
        "concept_id": None,
        "keywords": ["RLHF", "reinforcement learning from human feedback"],
    },
    {
        "name": "Multimodal Learning",
        "concept_id": None,
        "keywords": ["multimodal learning", "multi-modal"],
    },
    {
        "name": "Few-shot Learning",
        "concept_id": None,
        "keywords": ["few-shot learning", "few shot"],
    },
    {
        "name": "Self-supervised Learning",
        "concept_id": None,
        "keywords": ["self-supervised learning", "self supervised"],
    },
    {
        "name": "Contrastive Learning",
        "concept_id": None,
        "keywords": ["contrastive learning"],
    },
    {
        "name": "Federated Learning",
        "concept_id": None,
        "keywords": ["federated learning"],
    },
    {
        "name": "Differential Privacy in ML",
        "concept_id": None,
        "keywords": ["differential privacy machine learning", "dp ml"],
    },
    {
        "name": "Knowledge Graphs",
        "concept_id": None,
        "keywords": ["knowledge graph", "knowledge graphs"],
    },
    {
        "name": "Graph Machine Learning",
        "concept_id": None,
        "keywords": ["graph machine learning"],
    },
    {
        "name": "Automatic Speech Recognition",
        "concept_id": None,
        "keywords": ["automatic speech recognition", "ASR"],
    },
    {
        "name": "Machine Translation",
        "concept_id": None,
        "keywords": ["machine translation", "neural machine translation", "NMT"],
    },
    {
        "name": "Question Answering",
        "concept_id": None,
        "keywords": ["question answering", "QA"],
    },
    {
        "name": "Information Retrieval",
        "concept_id": None,
        "keywords": ["information retrieval", "IR"],
    },
    {
        "name": "Named Entity Recognition",
        "concept_id": None,
        "keywords": ["named entity recognition", "NER"],
    },
    {
        "name": "Summarization",
        "concept_id": None,
        "keywords": ["text summarization", "summarization"],
    },
    {
        "name": "Data Augmentation",
        "concept_id": None,
        "keywords": ["data augmentation"],
    },
    {
        "name": "Domain Adaptation",
        "concept_id": None,
        "keywords": ["domain adaptation"],
    },
    {
        "name": "Computer Vision",
        "concept_id": "https://openalex.org/C41008148",
        "keywords": ["computer vision", "object detection", "image classification"],
    },
    {
        "name": "Multimodal (General)",
        "concept_id": None,
        "keywords": ["multimodal learning", "multimodal AI", "vision language", "audio-text", "cross-modal"],
    },
]
