# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2023 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from mvt.android.modules.androidqf.dumpsys_packages import DumpsysPackages
from mvt.common.indicators import Indicators
from mvt.common.module import run_module

from ..utils import get_android_androidqf


class TestDumpsysPackagesModule:
    def test_parsing(self):
        data_path = get_android_androidqf()
        m = DumpsysPackages(target_path=data_path)
        run_module(m)
        assert len(m.results) == 2
        assert len(m.detected) == 0
        assert len(m.timeline) == 6
        assert (
            m.results[0]["package_name"]
            == "com.samsung.android.provider.filterprovider"
        )

    def test_detection_pkgname(self, indicator_file):
        data_path = get_android_androidqf()
        m = DumpsysPackages(target_path=data_path)
        ind = Indicators(log=logging.getLogger())
        ind.parse_stix2(indicator_file)
        ind.ioc_collections[0]["app_ids"].append("com.sec.android.app.DataCreate")
        m.indicators = ind
        run_module(m)
        assert len(m.results) == 2
        assert len(m.detected) == 1
        assert len(m.timeline) == 6
        assert m.detected[0]["package_name"] == "com.sec.android.app.DataCreate"
