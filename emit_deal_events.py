from prefect.events import emit_event
import time


def emit_deal_events(deal_id: str = "1234"):
    print(f"Deal {deal_id} starting!")
    customer_id = "abcd"

    emit_event(
        event=f"cart.completed.{deal_id}",
        resource={"prefect.resource.id": f"customer.{customer_id}"},
    )

    time.sleep(5)

    emit_event(
        event=f"shipping_address.completed.{deal_id}",
        resource={"prefect.resource.id": f"customer.{customer_id}"},
    )

    time.sleep(5)

    # Stray Final Event

    customer_id = "efgh"
    emit_event(
        event=f"payment.completed.5678",
        resource={"prefect.resource.id": f"customer.efgh"},
    )

    time.sleep(5)

    # Correct Final Event

    emit_event(
        event=f"payment.completed.{deal_id}",
        resource={"prefect.resource.id": f"customer.{customer_id}"},
    )


if __name__ == "__main__":
    emit_deal_events()
