import json

region = 'us-east-1'

# for each instance type, compute how many would be required to meet cpu and memory requirements, and cost
def compute_equivalence_classes(instances, cpus, memory):
    costs = []
    for (inst_type, info) in instances.items():
        cpu_equiv = cpus / info['vCPU']
        mem_equiv = memory / info['memory'] 
        n = max(cpu_equiv, mem_equiv)
        cost = n*info['ondemand']
        costs.append((inst_type, cost, n))

    costs = sorted(costs, key=lambda x: x[1])
    for x in costs:
        print(x)
        
def main():
    instances_file = 'www/instances.json'
    instances_raw = None
    with open(instances_file, 'r') as f:
        instances_raw = f.read()

    instances = json.loads(instances_raw)

    criteria = ['memory',
                # 'network_performance',
                'vCPU']
    stripped_instances = {}
    for i in instances:
        instance_dict = {c:float(i[c]) for c in criteria}
        try:
            instance_dict['ondemand'] = float(i['pricing'][region]['linux']['ondemand'])
        except KeyError as e:
            # some instances not available in all regions
            continue

        stripped_instances[i['instance_type']] = instance_dict

    cpus = 64
    memory = 64
    compute_equivalence_classes(stripped_instances, cpus, memory)
        
if __name__=='__main__':
    main()
