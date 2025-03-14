# Copyright (c) 2021 Microsoft Open Technologies, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#    THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
#    CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
#    LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
#    FOR A PARTICULAR PURPOSE, MERCHANTABILITY OR NON-INFRINGEMENT.
#
#    See the Apache Version 2.0 License for specific language governing
#    permissions and limitations under the License.
#
#    Microsoft would like to thank the following companies for their review and
#    assistance with these files: Intel Corporation, Mellanox Technologies Ltd,
#    Dell Products, L.P., Facebook, Inc., Marvell International Ltd.
#
#
import errno
import os
from os.path import exists
import json

from typing import TYPE_CHECKING
from typing import Dict, List

from data_module.port_config import PortConfig

DEFAULT_CONFIG_DB = "../resources/config_db.json"

class ConfigDBLoader():
    '''
    Read config from config_db.json.
    Load the data from a json file.
    '''

    def __init__(self, file_path: str = None):
        """
            Init the ConfigDBLoader.

            Args:
                file_path: config_db.json file path
        """


        self.file_path = self.__validate_file_path__(file_path)
        self.config_json = None
        self.port_config = None
        with open(self.file_path, mode='r') as f:
            self.config_json = json.load(f)
    
    
    def __validate_file_path__(self, file_path):
        """
        Validate if the file exists.
        Return:
            A validated file path
        """
        config_path = None
        if file_path:
            config_path = file_path
            print("Config_db.json path is {}".format(config_path))
        else:
            config_path = os.path.join(os.path.dirname(__file__),
                            DEFAULT_CONFIG_DB)
            print("Config_db.json uses default path {}".format(config_path))
        file_exists = exists(config_path)
        if not file_exists:
            raise FileNotFoundError("File not found:{}. Please refer to {} for how to set it.".format(
                config_path,
                "https://github.com/opencomputeproject/SAI/blob/master/ptf/docs/SAI-PTFv2Overview.md#run-test"
                 ))
        return config_path


    def get_port_config(self) -> List['PortConfig']:
        '''
        Method for get the configuration for port config.
        RETURN:
            dict: port config, key is the interface name
        '''
        
        port_conf = self.config_json.get('PORT')
        port_Configs = []
        for index, key in enumerate(port_conf):
            portConfig = PortConfig()
            portConfig.name = key
            portConfig.alias = port_conf[key]['alias']
            portConfig.index = int(port_conf[key]['index'])
            portConfig.lanes = [int(i) for i in port_conf[key]['lanes'].split(',')]
            portConfig.mtu = 0 if not 'mtu' in  port_conf[key] else int(port_conf[key]['mtu'])
            portConfig.pfc_asym = None \
                if not 'pfc_asym' in  port_conf[key] else port_conf[key]['pfc_asym']
            portConfig.speed = 0 \
                if not 'speed' in  port_conf[key] else int(port_conf[key]['speed'])
            portConfig.fec = None \
                if not 'fec' in  port_conf[key] else port_conf[key]['fec']
            portConfig.tpid = None if not 'tpid' in  port_conf[key] else port_conf[key]['tpid']
            port_Configs.append(portConfig)

        self.port_config = port_Configs
        return port_Configs
