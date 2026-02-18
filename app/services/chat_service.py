"""Simple chat service for compound Q&A - MVP version"""
from app.services.groq_client import get_groq_client


def chat_about_compound(compound_data: dict, analysis: dict, question: str) -> str:
    """
    Answer questions about a compound using LLM

    Args:
        compound_data: Dict with 'name' and 'ingredients' list
        analysis: Analysis result dict with top/heart/base notes
        question: User's question

    Returns:
        LLM response as string
    """
    # Build context from compound and analysis
    ingredients_str = ', '.join([
        f"{i['name']} ({i['percentage']}%)"
        for i in compound_data['ingredients']
    ])

    top_notes_str = ', '.join([n['name'] for n in analysis.get('top_notes', [])])
    heart_notes_str = ', '.join([n['name'] for n in analysis.get('heart_notes', [])])
    base_notes_str = ', '.join([n['name'] for n in analysis.get('base_notes', [])])

    context = f"""You are a perfume expert. Answer the user's question about this compound concisely and helpfully.

Compound: {compound_data['name']}
Ingredients: {ingredients_str}

Analysis Results:
- Top Notes: {top_notes_str or 'None'}
- Heart Notes: {heart_notes_str or 'None'}
- Base Notes: {base_notes_str or 'None'}
- Olfactive Family: {analysis.get('olfactive_family', 'Unknown')}
- Projection: {analysis.get('projection', 'Unknown')}
- Longevity: {analysis.get('longevity_hours', 0)} hours

User Question: {question}

Provide a clear, concise answer based on the compound's composition and analysis."""

    # Call LLM
    client = get_groq_client()
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": context}],
        temperature=0.3
    )

    return completion.choices[0].message.content
