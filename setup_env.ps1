Write-Host "Creating Python virtual environment..."
python -m venv venv

Write-Host "Activating virtual environment and installing requirements..."
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Write-Host ""
Write-Host "Environment setup is complete!"
Write-Host "To activate the environment manually in the future, run:"
Write-Host ".\venv\Scripts\Activate.ps1"
