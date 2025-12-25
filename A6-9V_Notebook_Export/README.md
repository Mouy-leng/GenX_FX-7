A6-9V NotebookLM Export Helper

This folder contains helper files to export a Google NotebookLM notebook (saved link) to local files.

Note: NotebookLM requires a signed-in Google Account to access private notebooks. The repository cannot fetch the notebook content without authentication.

Files included:
- README.md - this document
- export_notebooklm_playwright/ - a small Playwright script template (Node.js) that automates sign-in using a browser profile and saves the page HTML.
- run_export.ps1 - PowerShell helper that installs dependencies and runs the exporter using your profile (Windows PowerShell / pwsh).

Quick instructions
1. Open PowerShell (pwsh) as the intended user (so it uses your Chrome/Edge profile path).
2. Edit the Playwright script's NOTEBOOK_URL constant to the NotebookLM link: https://notebooklm.google.com/notebook/4824ad0b-4f53-4b06-a641-cb8f3bd90622
3. Optional: update BROWSER_USER_DATA_DIR in run_export.ps1 to point to your Chrome/Edge profile that is signed into the Google account which has access.
4. Run the helper (from this folder):

    pwsh.exe -File .\run_export.ps1

If you prefer manual export, open the NotebookLM link in your signed-in browser, then save the page (Ctrl+S) or copy the content into a local file.

Security notes
- Do not commit browser profiles containing secrets.
- The Playwright script uses your browser user-data directory to reuse an existing signed-in session. This is safer than scripting credentials directly.

If you want, I can tailor the Playwright script to your browser (Chrome or Edge), or add Puppeteer or Selenium variants.