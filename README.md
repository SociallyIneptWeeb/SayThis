# SayThis
A simple Python GUI App that generates audio from text using online TTS services.

![SayThis TTS Tab](docs/tts_tab.png)

## Setup

### Step 1: Download the Application

1. Go to the [Releases page](https://github.com/SociallyIneptWeeb/SayThis/releases) of this repository
2. Download the latest release ZIP file for your operating system:
   - **Windows**: `saythis-Windows.zip`
   - **macOS**: `saythis-macOS.zip`
   - **Linux**: `saythis-Linux.zip`

**WARNING**: MacOS release executable has performance issues and is not functioning as expected.

### Step 2: Extract and Run

1. Extract the downloaded ZIP file to a folder of your choice
2. Navigate into the extracted folder
3. Double-click on `SayThis.exe` to run the application

## Configure TTS Service

SayThis currently supports two text-to-speech services: ElevenLabs and Google Cloud TTS. Choose one of the following setup methods:

### Option 1: ElevenLabs TTS

#### Obtain ElevenLabs API Key

1. Navigate to https://elevenlabs.io/app/home and login/signup
2. Click on profile pic on bottom left and then click **API Keys**
3. Click **Create API Key** and enter a name
4. Copy the API key shown and save it in a file as this is the only time the key is viewable
5. If the API key is lost, simply follow the steps again to create a new one

#### Add API Key to SayThis App

1. Open the SayThis application
2. Click on the **Settings** tab
3. Select **ElevenLabs** from the service dropdown if it is not already selected
4. Paste your copied ElevenLabs API Key into the API Key input field
5. Click the **Save Settings** button

### Option 2: Google Cloud TTS

#### Obtain Service Account JSON

1. Create new project in Google Cloud Console if not created yet
2. Enable Cloud Text-to-Speech API. Enable billing on account (free trial) if needed
3. Navigate to **IAM & Admin** on Sidebar, then **Service Accounts** on Sidebar
4. Click **Create Service Account** and enter Name
5. Once created, click into the service account and click on the **Keys** tab
6. Click **Add Key** → **Create New Key** → **JSON**. This will download a JSON file to your computer

#### Add Service Account to SayThis App

1. Open the SayThis application
2. Click on the **Settings** tab
3. Select **Google Cloud** from the service dropdown if it is not already selected
4. Click on the **Browse** button which will open up file explorer
5. Select the downloaded service account JSON file
6. Click the **Save Settings** button

---

You're now ready to use SayThis! Simply switch back to the TTS tab, enter your text and generate high-quality audio using your chosen text-to-speech service.
