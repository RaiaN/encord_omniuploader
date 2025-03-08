** HOW TO UPLOAD LABELS **

1. Create and activate venv
2. Install dependendices `pip install -r requirements.txt`
3. Set up Encoder public API key
- Create Encord public API key
- Download generated private ssh key
- Rename it as `ssh-private-key.ed25519`
4. Open `upload.py` and set `PROJECT_HASH` to your project hash value
5. Run `python upload.py` to upload labels