from flask import Flask, request, jsonify
import psycopg2
import json

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.gxnnoohfqoppozdbzviu',
        password='AN3CnLKgbWgzYKBO',
        host='aws-0-eu-west-2.pooler.supabase.com',
        port='6543'
    )
    return conn

@app.route('/search', methods=['GET'])
def search():
    # Ensure request content type is JSON
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    # Get data from request
    data = request.json
    query_text = data.get('query')
    query_vector = data.get('vector')

    if not query_text and not query_vector:
        return jsonify({"error": "Bad Request, missing query or vector"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Perform keyword search
    if query_text:
        cur.execute("""
            SELECT id, title, author, publication_date, category
            FROM magazine_information
            WHERE title ILIKE %s OR author ILIKE %s
        """, (f'%{query_text}%', f'%{query_text}%'))
        keyword_results = cur.fetchall()

    # Perform vector search
    if query_vector:
        cur.execute("""
            SELECT id, title, author, publication_date, category, content
            FROM magazine_content
            ORDER BY vector_representation <=> %s
            LIMIT 10
        """, (query_vector,))
        vector_results = cur.fetchall()

    cur.close()
    conn.close()

    # Combine results
    combined_results = {
        "keyword_results": keyword_results,
        "vector_results": vector_results
    }

    return jsonify(combined_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6543, debug=True)
