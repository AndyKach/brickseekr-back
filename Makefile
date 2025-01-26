run:
	cd src/ && uvicorn main:app --reload


run\:ngrok:
	ngrok http --url=accurately-apparent-cobra.ngrok-free.app 8000