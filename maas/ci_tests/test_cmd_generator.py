import os
import unittest
from unittest import TestCase

from starter.utils import get_dist_init_addr, get_dist_init_addr_origin


class TestDist(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.algo_app_name = "maas-muses-deepseek"
        cls.pod_name_rule = "{ALGO_APP_NAME}--{TWL_LABEL_group}-{ID}"
        os.environ["NNODES"] = "2"

    def test_rank0(self):
        os.environ["NODE_RANK"] = "0"
        os.environ["TWL_LABEL_group"] = "depskv32-rank0"
        os.environ["POD_NAME"] = self.pod_name_rule.format(
            ALGO_APP_NAME=self.algo_app_name,
            TWL_LABEL_group=os.environ["TWL_LABEL_group"],
            ID=0,
        )
        dist_init_addr = get_dist_init_addr()
        dist_init_addr_origin = get_dist_init_addr_origin()
        self.assertEqual(dist_init_addr, dist_init_addr_origin)
        print(f"{dist_init_addr=}")

    def test_rank1(self):
        os.environ["NODE_RANK"] = "1"
        os.environ["TWL_LABEL_group"] = "depskv32-rank1"
        os.environ["POD_NAME"] = self.pod_name_rule.format(
            ALGO_APP_NAME=self.algo_app_name,
            TWL_LABEL_group=os.environ["TWL_LABEL_group"],
            ID=0,
        )
        dist_init_addr = get_dist_init_addr()
        dist_init_addr_origin = get_dist_init_addr_origin()
        self.assertEqual(dist_init_addr, dist_init_addr_origin)
        print(f"{dist_init_addr=}")


if __name__ == "__main__":
    unittest.main()
