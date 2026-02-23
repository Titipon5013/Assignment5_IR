import os
import json
import math
import time
from pathlib import Path
from collections import defaultdict, Counter
from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)

es_client = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "6zoRJw9FqjrVa2hO=PP_"),
    ca_certs="http_ca.crt",
    verify_certs=False
)

crawled_folder = Path(os.path.abspath('')) / 'crawled/'

documents = {}
inverted_index = defaultdict(list)
doc_lengths = {}
pagerank_scores = {}

try:
    res = es_client.search(index="simple", size=10000, _source=['url', 'pagerank'], query={"match_all": {}})
    for hit in res['hits']['hits']:
        src = hit['_source']
        if 'url' in src and 'pagerank' in src:
            pagerank_scores[src['url']] = src['pagerank']

    total_docs = 0
    for file in os.listdir(crawled_folder):
        if file.endswith(".txt"):
            j = json.load(open(os.path.join(crawled_folder, file), encoding='utf-8'))
            url = j['url']
            text = j['text']

            documents[url] = {
                "title": j.get('title', 'No Title'),
                "snippet": text[:150] + "..."
            }

            terms = text.lower().split()
            doc_lengths[url] = len(terms)

            term_counts = Counter(terms)
            for term, count in term_counts.items():
                inverted_index[term].append((url, count))
            total_docs += 1

    idf_scores = {}
    for term, postings in inverted_index.items():
        df = len(postings)
        idf_scores[term] = math.log10(total_docs / float(df))

    print(f" Load Manual Index Completed ({total_docs} documents)")
except Exception as e:
    print(f"⚠ Can't create Manual Index : {e}")


@app.route('/api/search_es', methods=['GET'])
def search_es():
    query_text = request.args.get('q', '')
    start_time = time.time()

    body = {
        "query": {
            "function_score": {
                "query": {
                    "match": {
                        "text": query_text
                    }
                },
                "script_score": {
                    "script": {
                        "source": "_score * doc['pagerank'].value"
                    }
                }
            }
        },
        "size": 10
    }

    try:
        res = es_client.search(index='simple', body=body, source_excludes=['url_lists'])
        exec_time = time.time() - start_time

        results = []
        for hit in res['hits']['hits']:
            results.append({
                "title": hit['_source'].get('title', 'No Title'),
                "url": hit['_source'].get('url', '#'),
                "snippet": hit['_source'].get('text', '')[:150] + '...',
                "score": hit['_score']
            })

        return jsonify({
            "total_results": res['hits']['total']['value'],
            "execution_time": round(exec_time, 4),
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/search_manual', methods=['GET'])
def search_manual():
    query_text = request.args.get('q', '').lower()
    start_time = time.time()

    query_terms = query_text.split()
    doc_scores = defaultdict(float)

    for term in query_terms:
        if term in inverted_index:
            term_idf = idf_scores[term]

            for url, count in inverted_index[term]:
                tf = count / float(doc_lengths[url]) if doc_lengths[url] > 0 else 0
                doc_scores[url] += (tf * term_idf)

    results = []
    for url, tfidf_score in doc_scores.items():
        # ดึงคะแนน PageRank ที่แอบโหลดมาจาก ES เข้ามาคูณ
        pr_score = pagerank_scores.get(url, 0.0001)
        final_score = tfidf_score * pr_score

        results.append({
            "title": documents[url]['title'],
            "url": url,
            "snippet": documents[url]['snippet'],
            "score": final_score
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    top_10_results = results[:10]
    exec_time = time.time() - start_time

    return jsonify({
        "total_results": len(doc_scores),
        "execution_time": round(exec_time, 4),
        "results": top_10_results
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)