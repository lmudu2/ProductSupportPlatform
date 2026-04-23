# How to Run the Product Support & Service Intelligence Platform

The fastest way to launch the dashboard is to use the Google Colab notebook. This allows any collaborator to run the platform in a fully pre-configured cloud environment—no local installations required.

## Step 1 — Open the Notebook in Colab
Click the link below to open the demo environment directly in your browser:

🚀 **[Open in Colab](https://colab.research.google.com/github/lmudu2/ProductSupportPlatform/blob/main/Product_Support_Intelligence_Demo.ipynb)**

> [!NOTE]
> You will need to be signed into a Google account to run the cells and save your configuration.

## Step 2 — Configure the Groq API Key
This platform uses the Llama-3 reasoning engine via Groq. To keep your API key secure in the cloud, follow these steps:

1. Click the **Keys (🔑)** icon in the left sidebar of your Google Colab window.
2. Click **Add new secret**.
3. Set the Name to exactly: `GROQ_API_KEY`
4. Paste your Groq API key into the Value field.
5. Toggle the switch to grant **"Notebook access"** to this secret.

> [!IMPORTANT]
> The `GROQ_API_KEY` is mandatory for the diagnostic narrative and strategic arbitration features to function.

## Step 3 — Run All Cells
Once your API key is configured:
1. Go to the top menu and select **Runtime → Run all** (or press `Cmd + F9` / `Ctrl + F9`).

The notebook will automatically:
- Clone the repository from GitHub.
- Install all Python dependencies (`Streamlit`, `Groq`, `XGBoost`, `Pandas`).
- Sync your `GROQ_API_KEY` to the local environment.
- Launch the Streamlit server and create a secure public tunnel.

## Step 4 — Access the Live Dashboard
Scroll to the very bottom of the notebook. The final cell will output a secure tunnel URL once the server has booted:

```text
🔗 CLICK THE LINK BELOW TO OPEN YOUR DASHBOARD:
https://some-random-words.loca.lt
```

Click that URL to open the live **Product Support & Service Intelligence Platform** in a new browser tab.

## Step 5 — Run Your First Diagnostic Workflow
1. **Multi-Modal Ingest**: Upload a hardware image (industrial gear, mobile device, etc.) or use the default telemetry.
2. **Review ML Inference**: View the confidence score and cost estimation for the predicted hardware fault.
3. **Analyze Strategy**: Check the **AI Strategy** section to see if the engine recommends "Repair" or "Upgrade" based on the sector's economic mandate.

---

## Technical Resources

| Resource | Link |
| :--- | :--- |
| **GitHub Repository** | [lmudu2/ProductSupportPlatform](https://github.com/lmudu2/ProductSupportPlatform) |
| **Project Whitepaper** | [Whitepaper.md](./Product_Support_Intelligence_Whitepaper.md) |
| **Technical README** | [README.md](./README.md) |

---

## Troubleshooting

| Issue | Solution |
| :--- | :--- |
| `GROQ_API_KEY not found` | Confirm the secret is named exactly `GROQ_API_KEY` and "Notebook access" is ON. |
| Dashboard is a blank white screen | Wait 5–10 seconds for the tunnel to initialize, then hard-refresh (`Cmd + Shift + R`). |
| Colab disconnects | Free Colab tiers timeout after inactivity. Re-run all cells to reboot. |
| Tunnel URL is slow | If `localtunnel` is slow, you can manually restart the final cell to generate a new URL. |
| Hardware sector not identified | Ensure the uploaded image is clear and the component is centered for the Vision AI. |
