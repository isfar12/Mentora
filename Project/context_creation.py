#This part was done to test context upload and retrieve in chat

context='''
### About GreenGrow Innovations

**GreenGrow Innovations** is a forward-thinking AI company founded by **Zubayer Ishfar Zeem**. Committed to driving sustainability through cutting-edge technology, GreenGrow leverages artificial intelligence to develop innovative solutions that address some of the world's most pressing environmental challenges.

Since its inception, the company has been dedicated to fostering a more sustainable future by using AI to optimize resource use, reduce waste, and promote greener practices across industries. GreenGrow's solutions are designed to empower businesses, governments, and individuals to make smarter, more sustainable choices.

In a significant milestone, GreenGrow Innovations has recently secured **\$1 million** in funding, with a valuation of **\$200 million**, underscoring the growing demand for its groundbreaking technologies. With a vision to create impactful change, GreenGrow continues to pave the way toward a more sustainable and AI-driven world.

At GreenGrow, we believe that the future of sustainability is intertwined with the power of artificial intelligence, and we are committed to being at the forefront of this transformation.
'''

import uuid
from rag_loaders import text_splitter
from vector_store import load_vector_store
session_id = str(uuid.uuid4())
splitted_text=text_splitter(context)
vector_store = load_vector_store(session_id)
vector_store.add_texts(texts=splitted_text,metadatas=[{"source": "context_creation.py"}])
print(session_id)