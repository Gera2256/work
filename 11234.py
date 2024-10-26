import psycopg2
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify

app = Flask(__name__)
es = Elasticsearch(['http://localhost:9200'])
conn = psycopg2.connect(
    dbname='yourdbname',
    user='youruser',
    password='yourpassword',
    host='localhost',
    port='5432'
)

@app.route('/document', methods=['POST'])
def save_document():
    data = request.json.get('document', {})

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO documents (title, content) VALUES (%s, %s) RETURNING id;", (title, content))
            document_id = cur.fetchone()[0]
            conn.commit()
            es.index(index='documents', id=document_id, body=data)

        return jsonify({
            "document": {
                "id": document_id,
                "title": title,
                "content": content
            }
        }), 201  # Статус 201 для успешного создания
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['GET'])
def search_documents():
    query_string = request.args.get('querystring', '')

    try:
        response = es.search(index='documents', body={
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": ["title", "content"],
                    "type": "best_fields"
                }
            }
        })

        documents = []
        for hit in response['hits']['hits']:
            documents.append({
                "id": hit['_id'],
                "fieldName": "title" if 'title' in hit['_source'] else "content",
                "fieldContent": hit['_source'].get('title', hit['_source'].get('content'))
            })

        return jsonify({"documents": documents})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/document/<int:document_id>', methods=['PATCH'])
def update_document(document_id):
    updated_data = request.json.get('document', {})

    if not updated_data.get('title') or not updated_data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE documents SET title = %s, content = %s WHERE id = %s;",
                        (updated_data['title'], updated_data['content'], document_id))
            conn.commit()
            es.update(index='documents', id=document_id, body={"doc": updated_data})

        return jsonify({
            "document": {
                "id": document_id,
                "title": updated_data["title"],
                "content": updated_data["content"]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_connection():
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
