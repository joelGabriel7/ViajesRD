from fastapi import APIRouter, Request
import paypalrestsdk

app = APIRouter(prefix="/payment", tags=["Payment"])


CLIENT_ID = 'Aerha-chYWLU3W8BnWBJIEnEL4fO9XdCddYFGngtCkjTxW9Dzk7eUZb03d_El-D4uEHEagcw5KSp7Ddj'
SECRET_KEY = 'EB_Ej5IJfEq73aNN3XSAygUMYByMZ8e9OdiFhg5f4t7KQtSjHeGhqLrPIHftpmljm3q2FFY6qanCFRQE'

import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": CLIENT_ID,
  "client_secret": SECRET_KEY })

# Resto de tu código...

@app.get("/paypal/execute")
async def execute_payment(request: Request):
    payment_id = request.query_params.get('paymentId')
    payer_id = request.query_params.get('PayerID')

    # Encuentra el pago correspondiente
    payment = paypalrestsdk.Payment.find(payment_id)

    # Ejecuta el pago
    if payment.execute({"payer_id": payer_id}):
        print("Payment executed successfully")
        # Aquí puedes agregar la lógica para actualizar tu base de datos
    else:
        print(payment.error)

    return {"message": "Payment executed"}