from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts')
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400
    
    if POSTS:
        new_id = POSTS[-1]["id"] + 1
    else:
        new_id = 1

    new_post = {"id": new_id, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_posts(id):
    post_to_delete = next((post for post in POSTS if post['id'] == id), None)

    if post_to_delete is None:
        return jsonify({"error": "Post not found."}), 404
    
    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post_to_update = next((post for post in POSTS if post['id'] == id), None)
    
    if post_to_update is None:
        return jsonify({"error": "Post not found."}), 404

    data = request.get_json()
    print(data)
    title = data.get('title')
    content = data.get('content')

    if title:
        post_to_update['title'] = title
    if content:
        post_to_update['content'] = content

    return jsonify(post_to_update), 200


@app.route('/api/posts/search')
def search_post():
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    results = POSTS

    if title_query:
        results = [post for post in results if title_query.lower() in post['title'].lower()]
    
    if content_query:
        results = [post for post in results if content_query.lower() in post['content'].lower()]
    
    return jsonify(results), 200
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
