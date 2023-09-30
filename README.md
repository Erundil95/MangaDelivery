
MangaDelivery
MangaDelivery is a Python-based application that allows users to automatically download and save manga chapters from specific websites. The application is designed to run periodically on your pc and store the downloaded manga chapters in a local directory or a cloud storage system of the user's choice (only Gdrive is supported so far, can still just simply use the local directory for dropbox/onedrive/icloud for a simple cloud savefile).

Notes

If the refresh token is revoked/expired it will be automatically deleted and it'll prompt a new OAuth flow to create a new file with fresh access token and refresh token
