import requests
import json
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig

def create_token_on_pumpfun(
    private_key: str,
    token_name: str,
    token_symbol: str,
    token_description: str,
    token_twitter: str,
    token_telegram: str,
    token_website: str,
    image_path: str,
    dev_buy_amount: float,
    rpc_endpoint: str,
    priority_fee: float = 0.0005,
    slippage: int = 10
):
    try:
        # Generate keypairs
        signer_keypair = Keypair.from_base58_string(private_key)
        mint_keypair = Keypair()

        print(f"Signer Public Key: {signer_keypair.pubkey()}")
        print(f"Mint Public Key: {mint_keypair.pubkey()}")

        # Define token metadata
        form_data = {
            "name": token_name,
            "symbol": token_symbol,
            "description": token_description,
            "twitter": token_twitter,
            "telegram": token_telegram,
            "website": token_website,
            "showName": "true",
        }

        # Read and attach the image
        with open(image_path, "rb") as f:
            file_content = f.read()

        files = {"file": (image_path, file_content, "image/jpg")}

        # Upload metadata to IPFS via Pump.fun API
        print("Uploading metadata to IPFS...")
        metadata_response = requests.post(
            "https://pump.fun/api/ipfs", data=form_data, files=files
        )
        print("Metadata Response Status Code:", metadata_response.status_code)
        print("Metadata Response Content:", metadata_response.content)

        metadata_response.raise_for_status()
        metadata_uri = metadata_response.json().get("metadataUri")

        if not metadata_uri:
            raise ValueError("Failed to upload metadata to IPFS")

        print(f"Metadata URI: {metadata_uri}")

        # Token metadata with URI
        token_metadata = {
            "name": form_data["name"],
            "symbol": form_data["symbol"],
            "uri": metadata_uri,
        }

        # Create transaction payload
        print("Creating token transaction...")
        response = requests.post(
            "https://pumpportal.fun/api/trade-local",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "publicKey": str(signer_keypair.pubkey()),
                    "action": "create",
                    "tokenMetadata": token_metadata,
                    "mint": str(mint_keypair.pubkey()),
                    "denominatedInSol": "true",
                    "amount": dev_buy_amount,
                    "slippage": slippage,
                    "priorityFee": priority_fee,
                    "pool": "pump",
                }
            ),
        )
        print("Transaction Creation Response Status Code:", response.status_code)
        print("Transaction Creation Response Content:", response.content)

        if response.status_code != 200:
            print("Error generating transaction:", response.json())
            return

        # Debugging transaction content before signing
        try:
            tx_content = response.content
            print("Raw Transaction Content:", tx_content)
            tx_message = VersionedTransaction.from_bytes(tx_content).message
            print("Transaction Message:", tx_message)
        except Exception as e:
            print("Error parsing transaction content:", str(e))
            return

        print("Signing transaction...")
        tx = VersionedTransaction(
            VersionedTransaction.from_bytes(response.content).message,
            [mint_keypair, signer_keypair],
        )

        print("Signed Transaction:", tx)

        print("Sending transaction to blockchain...")
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)
        tx_payload = SendVersionedTransaction(tx, config)

        send_response = requests.post(
            url=rpc_endpoint,
            headers={"Content-Type": "application/json"},
            data=tx_payload.to_json(),
        )

        print("Send Transaction Response Status Code:", send_response.status_code)
        print("Send Transaction Response Content:", send_response.content)

        if send_response.status_code != 200:
            print("Failed to send transaction:", send_response.reason)
            return

        tx_signature = send_response.json().get("result")
        if tx_signature:
            print(f"Transaction successful! View it here: https://solscan.io/tx/{tx_signature}")
        else:
            print("Transaction failed: No signature returned.")

    except Exception as e:
        print("An error occurred:", str(e))


create_token_on_pumpfun(
    private_key="",
    token_name="DW Deployment Showcase",
    token_symbol="ORTUS",
    token_description="This token has been created automatically using the ORTUS spell by Degen Wizard AI.",
    token_twitter="https://x.com/wizard_terminal",
    token_telegram="https://t.me/degenwizard_portal",
    token_website="https://www.degenwizard.com/spells",
    image_path="",
    dev_buy_amount=0,
    rpc_endpoint="https://api.mainnet-beta.solana.com/",
)
