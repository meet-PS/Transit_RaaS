import sys
import do_json
import constants
import os
from os import listdir
from os.path import isfile, join

def run_shell_script(my_script):
    #This can run a shell script only on the management VM
    print(my_script)
    return os.system(my_script)

def run_playbook(my_script):
    #This can run a playbook only on the management VM
    print(my_script)
    return os.system(my_script)

def get_vm_ip(hypervisor,vm_name,net_name):
    try:
        vm_name_arg = " vm_name="+vm_name
        ip_file_path_arg = " ip_path=../../"+constants.temp_file
        net_name_arg = " net_name=" + net_name
        hypervisor_arg = " hypervisor="+hypervisor
        extra_vars = constants.ansible_become_pass + vm_name_arg +  hypervisor_arg + ip_file_path_arg + net_name_arg

        rc = run_shell_script("ansible-playbook logic/misc/get_vm_ip.yml -i logic/inventory/hosts.yml -v --extra-vars '"+extra_vars+"'")
        if (rc != 0):
            raise

        return read_temp_file()
    except:
        print("IP fetch failed for machine: "+vm_name+" of network "+net_name)
        raise

def get_ns_ip(hypervisor,ns_name,ns_if):
    try:
        ns_name_arg=" ns_name="+ns_name
        ns_if_arg=" ns_if="+ns_if
        ip_file_path_arg = " ip_path=../../"+constants.temp_file
        hypervisor_arg = " hypervisor="+hypervisor
        extra_vars = constants.ansible_become_pass +  hypervisor_arg + ip_file_path_arg+ns_name_arg+ns_if_arg

        rc = run_shell_script("ansible-playbook logic/misc/get_ns_ip.yml -i logic/inventory/hosts.yml -v --extra-vars '"+extra_vars+"'")
        if (rc != 0):
            raise

        return read_temp_file()
    except:
        print("IP fetch failed for machine: "+ns_name+" of interface "+ns_interface)
        raise

def get_mgmt_nid():
    json_data = do_json.json_read(constants.mgmt_net_file)
    return json_data["network_id"]

def client_exists_vpc(vpc_name):
    return os.path.exists(constants.var_vpc + vpc_name + "/" + vpc_name + ".json")

def client_add_vpc(hypervisor, vpc_name):
    vpc_dir = constants.var_vpc + vpc_name + "/"
    file_path = vpc_dir + vpc_name + ".json"

    if not os.path.exists(vpc_dir):
        os.makedirs(vpc_dir)

    new_vpc_data = constants.new_vpc_data
    new_vpc_data["hypervisor_name"] = hypervisor
    new_vpc_data["vpc_name"] = vpc_name
    do_json.json_write(new_vpc_data, file_path)

    vpc_spines_dir = vpc_dir + constants.vpc_spines
    if not os.path.exists(vpc_spines_dir):
        os.makedirs(vpc_spines_dir)

    vpc_leafs_dir = vpc_dir + constants.vpc_leafs
    if not os.path.exists(vpc_leafs_dir):
        os.makedirs(vpc_leafs_dir)

    vpc_pcs_dir = vpc_dir + constants.vpc_pcs
    if not os.path.exists(vpc_pcs_dir):
        os.makedirs(vpc_pcs_dir)

def client_exists_spine(vpc_name, spine_name):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_spines + spine_name+ ".json"

    return os.path.exists(file_path)

def client_add_spine(hypervisor, vpc_name, spine_name, capacity):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_spines + spine_name + ".json"

    new_spine_data = constants.new_spine_data
    new_spine_data["hypervisor_name"] = hypervisor
    new_spine_data["vpc_name"] = vpc_name
    new_spine_data["spine_name"] = spine_name
    new_spine_data["capacity"] = capacity
    do_json.json_write(new_spine_data, file_path)

def client_exists_l1_transit(l1_transit_name):
    file_path = constants.l1_transits + l1_transit_name + ".json"
    return os.path.exists(file_path)

def client_add_l1_transit(hypervisor, l1_transit_name, capacity):
    dir_path = constants.l1_transits;
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = dir_path + l1_transit_name + ".json"

    new_l1_transit_data = constants.new_l1_transit_data
    new_l1_transit_data["hypervisor_name"] = hypervisor
    new_l1_transit_data["l1_transit_name"] = l1_transit_name
    new_l1_transit_data["capacity"] = capacity
    do_json.json_write(new_l1_transit_data, file_path)

def client_exists_l2_transit(l2_transit_name):
    file_path = constants.l2_transits + l2_transit_name + ".json"
    return os.path.exists(file_path)

def client_add_l2_transit(hypervisor, l2_transit_name, capacity):
    dir_path = constants.l2_transits;
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = dir_path + l2_transit_name + ".json"

    new_l2_transit_data = constants.new_l2_transit_data
    new_l2_transit_data["hypervisor_name"] = hypervisor
    new_l2_transit_data["l2_transit_name"] = l2_transit_name
    new_l2_transit_data["capacity"] = capacity
    do_json.json_write(new_l2_transit_data, file_path)

def client_exists_leaf(vpc_name, leaf_name):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_leafs + leaf_name + ".json"

    return os.path.exists(file_path)

def get_all_spines(vpc_name):
    dir_path=constants.var_vpc + vpc_name + \
            constants.vpc_spines
    spines = [f.split('.')[0] for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return spines

def get_all_leafs(vpc_name):
    dir_path=constants.var_vpc + vpc_name + \
            constants.vpc_leafs
    leafs = [f.split('.')[0] for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return leafs


def client_add_leaf(hypervisor, vpc_name, leaf_name, network_id):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_leafs + leaf_name + ".json"
    new_leaf_data = constants.new_leaf_data
    new_leaf_data["hypervisor_name"] = hypervisor
    new_leaf_data["vpc_name"] = vpc_name
    new_leaf_data["leaf_name"] = leaf_name
    new_leaf_data["network_id"] = network_id
    do_json.json_write(new_leaf_data, file_path)

def client_exists_pc(vpc_name, pc_name):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_pcs + pc_name + ".json"

    print(file_path)

    return os.path.exists(file_path)

def client_add_pc(hypervisor_name,vpc_name, pc_name, capacity):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_pcs + pc_name + ".json"
    print(constants.new_pc_data)
    new_pc_data = constants.new_pc_data
    new_pc_data["hypervisor_name"] = hypervisor_name
    new_pc_data["vpc_name"] = vpc_name
    new_pc_data["pc_name"] = pc_name
    new_pc_data["capacity"] = capacity
    do_json.json_write(new_pc_data, file_path)

def write_spine_ip(vpc, spine, spine_ip):
    file_path = constants.var_vpc + vpc + \
            constants.vpc_spines + spine + ".json"

    spine_data = do_json.json_read(file_path)
    spine_data["ip"] = spine_ip
    do_json.json_write(spine_data, file_path)

def get_spine_ip(vpc, spine):
    file_path = constants.var_vpc + vpc + \
            constants.vpc_spines + spine + ".json"
    spine_data = do_json.json_read(file_path)
    spine_ip = spine_data["ip"]
    return spine_ip

def read_temp_file():
    with open(constants.temp_file) as f:
        data = f.read()

    return data
    
def get_new_veth_subnet(subnet_name):
    file_path = "var/reserved_subnets.json"
    subnet_data = do_json.json_read(file_path)
    return subnet_data[subnet_name]

def update_veth_subnet(subnet_name,new_subnet):
    file_path = "var/reserved_subnets.json"
    subnet_data = do_json.json_read(file_path)
    subnet_data[subnet_name]=new_subnet
    do_json.json_write(subnet_data, file_path)

def client_add_leaf_pc(vpc_name, pc_name, leaf_name):
    file_path = constants.var_vpc + vpc_name + \
            constants.vpc_pcs + pc_name + ".json"

    pc_data = do_json.json_read(file_path) 
    leafs = pc_data["leafs"]
    leafs.append(leaf_name)
    pc_data["leafs"] = leafs
    do_json.json_write(pc_data, file_path) 

