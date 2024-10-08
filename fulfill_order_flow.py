from prefect import flow
from prefect.events import DeploymentCompoundTrigger


@flow(log_prints=True)
def fulfill_order_flow(deal_id: str = "1234", customer_id: str = "abcd"):
    print(f"Fulfilling order {deal_id}!")


if __name__ == "__main__":
    fulfill_order_flow.serve(
        name="fulfill_order_flow",
        trigger=DeploymentCompoundTrigger(
            enabled=True,
            name="deal_compound_trigger",
            require="all",
            triggers=[
                {
                    "type": "event",
                    "match": {"prefect.resource.id": f"customer.*"},
                    "expect": [f"cart.completed.*"],
                },
                {
                    "type": "event",
                    "match": {"prefect.resource.id": f"customer.*"},
                    "expect": [f"shipping_address.completed.*"],
                },
                {
                    "type": "event",
                    "match": {"prefect.resource.id": f"customer.*"},
                    "expect": [f"payment.completed.*"],
                },
            ],
        ),
    )
