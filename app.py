from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


def load_blog_posts():
    """
        Load blog posts from a JSON file.
        Returns A list of blog posts if the file is found and valid; otherwise, an empty list.
    """
    try:
        with open('blog_posts.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: blog_posts.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: blog_posts.json file is not valid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


@app.route('/')
def index():
    """
        index page showing all blog posts.
        Returns rendered HTML for the index page.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
        Handle adding a new blog post.
        Returns rendered HTML for the add page or a redirect to the index on POST.
    """
    if request.method == 'POST':

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_blog_posts()

        new_id = len(blog_posts) + 1

        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)

        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


def save_blog_posts(blog_posts):
    """
        Save the list of blog posts to a JSON file.
    """
    with open('blog_posts.json', 'w') as f:
        json.dump(blog_posts, f, indent=4)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
        Handle deleting a blog post by its ID.
    """
    blog_posts = load_blog_posts()

    updated_posts = [post for post in blog_posts if post['id'] != post_id]

    with open('blog_posts.json', 'w') as f:
        json.dump(updated_posts, f, indent=4)

    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    """
        Find a blog post by its ID.
    """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
        Handle updating an existing blog post.
    """

    blog_posts = load_blog_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':

        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated blog posts back to the JSON file
        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Enable debug mode for detailed error messages
