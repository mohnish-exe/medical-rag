import csv
import json

with open('../query_answers_with_contexts_final.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(list(reader)[:5], 1):
        data = json.loads(row['answer_with_context'])
        contexts = data.get('contexts', [])
        print(f"\n{i}. Type: {type(contexts)}")
        if contexts:
            print(f"   First context type: {type(contexts[0])}")
            print(f"   First context: {str(contexts[0])[:100]}")
