from kubernetes import client, config
from prettytable import PrettyTable
import argparse

def parse_argument():
	parser = argparse.ArgumentParser()
	parser.add_argument("--namespace", help="namespace of deployments")
	return parser.parse_args()

def print_deployment_list(namespace):
	config.load_kube_config()
	apis_api = client.AppsV1Api()
	resp = apis_api.list_namespaced_deployment(namespace=namespace)
	
	deployment_status_table = PrettyTable(['Deployment Name', 'Image', 'Last Update Time'])

	for item in resp.items:
		total_update = len(item.status.conditions)
		total_container = len(item.spec.template.spec.containers)	
		deployment_status_table.add_row([item.metadata.name, item.spec.template.spec.containers[total_container-1].image, item.status.conditions[total_update-1].last_update_time])
	print(deployment_status_table)


if __name__ == "__main__":
	args = parse_argument()
	if args.namespace:
		namespace=args.namespace
	else:
		namespace="default"
	
	print_deployment_list(namespace)
