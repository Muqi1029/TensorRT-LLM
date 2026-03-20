import os


def get_node_nums() -> int:
    return int(os.getenv("NNODES", 1))


def get_node_rank() -> int:
    return int(os.getenv("NODE_RANK", 0))


def cluster_endpoint() -> str:
    return os.getenv("CLUSTER", "yj-arsenal")


def get_dist_init_addr():
    # get dist init addr in the multi nodes setting
    node_nums = get_node_nums()
    if node_nums <= 1:
        raise ValueError(
            f"Dist init addr must be used in multi nodes settings, but found {node_nums=}"
        )

    # NODE_RANK
    node_rank = get_node_rank()

    # POD_NAME: <algorithm_app_name>--<twl_label_group>-<number> | example: maas-muses-deepseek--dpskv32-rank1-0
    master_addr = os.environ["POD_NAME"]

    # CLUSTER: yj-arsenal by default
    cluster = cluster_endpoint()

    # TWL_LABEL_group: <group_name> | example: dpskv32-rank1, whose master_twl_label_group is `dpskv32-rank0`
    twl_label_group = os.environ["TWL_LABEL_group"]

    if node_rank == 0:
        # master node
        master_twl_label_group = twl_label_group
    elif node_rank >= 1:
        # worker nodes
        twl_label_group_arr = list(twl_label_group)

        # check node rank
        if int(twl_label_group_arr[-1]) != node_rank:
            raise ValueError(
                "The last item of TWL_LABEL_group must be equal to NODE_RANK, "
                "but found {twl_label_group=}, NODE_RANK={node_rank}"
            )

        twl_label_group_arr[-1] = "0"
        master_twl_label_group = "".join(twl_label_group_arr)

    else:
        raise ValueError(
            f"node rank is supposed to greater or equal to 0, but found {node_rank=} by env NODE_RANK"
        )

    master_addr = master_addr.replace(twl_label_group, master_twl_label_group)

    # HARDCODE Here: get internal ip
    return master_addr + f".hl-{master_addr.rsplit('-', 1)[0]}.rcd-f1-prod.svc.{cluster}.local"


def get_dist_init_addr_origin():
    node_nums = get_node_nums()
    if node_nums > 1:
        node_rank = int(get_node_rank())
        master_addr = os.environ.get("POD_NAME")
        cluster = cluster_endpoint()
        twl_label_group = os.environ.get("TWL_LABEL_group")
        if node_rank >= 1:
            twl_label_group_items = twl_label_group.split("-")
            last_item = twl_label_group_items[-1]
            new_last_item = last_item.replace(str(node_rank), "0")
            twl_label_group_items[-1] = new_last_item
            new_twl_label_group = "-".join(twl_label_group_items)
            master_addr = master_addr.replace(twl_label_group, new_twl_label_group)
        master_addr = (
            master_addr + f".hl-{master_addr.rsplit('-', 1)[0]}.rcd-f1-prod.svc.{cluster}.local"
        )
    return master_addr
