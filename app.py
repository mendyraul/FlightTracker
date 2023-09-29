from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', profiles=profiles)

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    # Find the profile with the given ID
    profile = next((p for p in profiles if p['id'] == profile_id), None)
    if profile:
        return render_template('profile.html', profile=profile)
    else:
        return "Profile not found", 404

if __name__ == '__main__':
    app.run(debug=True)
 