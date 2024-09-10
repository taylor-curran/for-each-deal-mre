from prefect import flow
from prefect.events import DeploymentCompoundTrigger


@flow(log_prints=True)
def fulfill_order_flow(deal_id: str = "1234", customer_id: str = "abcd"):
    print(f"Fulfilling order {deal_id}!")


# Example Trigger

#   triggers=[
#             DeploymentCompoundTrigger(
#                 enabled=True,
#                 name="my-compound-trigger",
#                 require="all",
#                 triggers=[
#                     {
#                       "type": "event",
#                       "match": {"prefect.resource.id": "my.external.resource"},
#                       "expect": ["external.resource.pinged"],
#                     },
#                     {
#                       "type": "event",
#                       "match": {"prefect.resource.id": "my.external.resource"},
#                       "expect": ["external.resource.replied"],
#                     },
#                 ],
#                 parameters={
#                     "param_1": "{{ event }}",
#                 },
#             )
#         ],


# emit_event(
#     event=f"cart.completed.{deal_id}",
#     resource={"prefect.resource.id": f"customer.{customer_id}"},
# )
# time.sleep(5)
# emit_event(
#     event=f"shipping_address.completed.{deal_id}",
#     resource={"prefect.resource.id": f"customer.{customer_id}"},
# )
# time.sleep(5)
# emit_event(
#     event=f"payment.completed.{deal_id}",
#     resource={"prefect.resource.id": f"customer.{customer_id}"},
# )


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
