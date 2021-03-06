import os
import sys
import do_json
import raas_utils
import hyp_utils
import constants
import ipaddress


"""@params:
    param1 = connection config name (required)
"""

if __name__=="__main__":
    if (len(sys.argv) < 2):
        raas_utils.log_service("Please give connection config file")
        exit(1)

    connection_config_file = sys.argv[1]
    connection_name = connection_config_file.split('/')[-1].split('.')[0]
    cid = hyp_utils.get_client_id()

    connection_data = do_json.json_read(connection_config_file)
    raas_utils.log_service(connection_data)
    vpc_name = connection_data["vpc_name"]
    pc_name = connection_data["pc_name"]
    leaf_name = connection_data["leaf_name"]

    if not raas_utils.client_exists_pc(vpc_name, pc_name):
        raas_utils.log_service("pc does not exists "+pc_name)
        exit(1)

    if not raas_utils.client_exists_leaf(vpc_name, leaf_name):
        raas_utils.log_service("leaf does not exist "+ leaf_name)
        exit(1)

    pc_hypervisor_name = connection_data["pc_hypervisor_name"]
    leaf_hypervisor_name = connection_data["leaf_hypervisor_name"]

    if (pc_hypervisor_name == leaf_hypervisor_name):
        raas_utils.log_service("pc and leaf exist in same hypervisor, direct connect")
        hypervisor = pc_hypervisor_name
        hypervisor_arg = "hypervisor="+hypervisor
        hypervisors_data = hyp_utils.get_hypervisors_data()
        hypervisor_ip = hyp_utils.get_hyp_ip(hypervisor)

        try:
            hyp_pc_name = hyp_utils.get_hyp_pc_name(hypervisor, vpc_name, pc_name)

            pc_name_ansible_arg = "c_name=" + hyp_pc_name

            hyp_leaf_name = hyp_utils.get_hyp_leaf_name(hypervisor, vpc_name, leaf_name)
            hyp_leaf_name_arg = "l_name=" + hyp_leaf_name

            l_br_name = hyp_leaf_name + "_br"
            l_br_name_arg = "l_br_name=" + l_br_name

            c_hyp_id = hyp_pc_name.split('_')[0]
            vpc_hyp_id = hyp_pc_name.split('_')[1]
            pc_hyp_id = hyp_pc_name.split('_')[2]

            leaf_hyp_id = hyp_leaf_name.split('_')[2]

            ve_l_pc_arg = "ve_l_pc=" + c_hyp_id + '_' + vpc_hyp_id + '_ve_' + leaf_hyp_id + ' ' + pc_hyp_id 
            ve_pc_l_arg = "ve_pc_l=" + c_hyp_id + '_' + vpc_hyp_id + '_ve_' + pc_hyp_id + ' ' + leaf_hyp_id 

            extra_vars = constants.ansible_become_pass + " " + \
                    pc_name_ansible_arg + " " + hypervisor_arg + \
                    " " + hyp_leaf_name_arg + " " + l_br_name_arg + " " + \
                    ve_l_pc_arg + " " + ve_pc_l_arg

            #raas_utils.log_service("here2")
            raas_utils.run_playbook("ansible-playbook logic/subnet/add_to_subnet.yml -i logic/inventory/hosts.yml -v --extra-vars '"+extra_vars+"'")
                
            raas_utils.client_add_leaf_pc(vpc_name, pc_name, leaf_name)

            #raise
            #raas_utils.add_mgmt_ns(hypervisor)
        except:
            raas_utils.log_service("connect pc failed")
            raise
            #raas_utils.log_service("ansible-playbook logic/vpc/delete_pc.yml -i logic/inventory/hosts.yml -v --extra-vars '"+extra_vars+"'")
    else:
        raas_utils.log_service("pc and leaf exist in different hypervisor, vxlan connect")
        exit(1)
