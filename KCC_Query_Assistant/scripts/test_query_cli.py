from rag_pipeline import handle_query

print("\n💬 Welcome to KCC Query Assistant (CLI Test Mode)")
print("Type 'exit' to quit.\n")

while True:
    query = input("Ask your question: ").strip()
    if query.lower() in ["exit", "quit"]:
        break

    result = handle_query(query)

    print("\n🔍 SOURCE:", result["source"])
    print("\n📚 CONTEXT USED:\n")
    for i, chunk in enumerate(result["context"], 1):
        print(f"[{i}] {chunk}\n")

    print("🧠 RESPONSE:\n", result["answer"])
    print("="*80 + "\n")
