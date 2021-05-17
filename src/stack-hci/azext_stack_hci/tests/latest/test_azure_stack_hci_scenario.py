# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

import os
from azure.cli.testsdk import ScenarioTest
from .. import try_manual, raise_if
from azure.cli.testsdk import ResourceGroupPreparer


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


@try_manual
def setup(test, rg):
    test.kwargs.update({
        'cluster_name': test.create_random_name('cli-cluster-', 20),
        'app_name': test.create_random_name(prefix='cli-app-', length=14)
    })

    app_id = test.cmd('ad app create --display-name {app_name}').get_output_in_json()['appId']
    tenant_id = test.cmd('account show').get_output_in_json()['tenantId']

    test.kwargs.update({
        'aad_client_id': app_id,
        'aad-tenant-id': tenant_id
    })


# EXAMPLE: /Clusters/put/GetClusters
@try_manual
def step__clusters_put_clusters(test, rg):
    test.cmd('az stack-hci cluster create '
             '--location "East US" '
             '--aad-client-id {aad_client_id} '
             '--aad-tenant-id {aad-tenant-id} '
             '--name "{cluster_name}" '
             '--resource-group "{rg}" '
             '--tags tag0="value0" ',
             checks=[
                 test.check('location', "eastus"),
                 test.check('name', '{cluster_name}'),
                 test.check('resourceGroup', '{rg}'),
                 test.check('tags', {'tag0': 'value0'})
             ])


# EXAMPLE: /Clusters/get/GetClusters
@try_manual
def step__clusters_get_clusters(test, rg):
    test.cmd('az stack-hci cluster show '
             '--name "{cluster_name}" '
             '--resource-group "{rg}"',
             checks=[
                 test.check('location', "eastus"),
                 test.check('name', '{cluster_name}'),
                 test.check('resourceGroup', '{rg}'),
                 test.check('tags', {'tag0': 'value0'})
             ])


# EXAMPLE: /Clusters/get/ListClusters
@try_manual
def step__clusters_list_clusters(test, rg, cluster_amount):
    test.cmd('az stack-hci cluster list '
             '--resource-group "{rg}"',
             checks=[test.check('length([])', cluster_amount)])

    test.cmd('az stack-hci cluster list ',
             checks=[test.check('length([])', cluster_amount)])


# EXAMPLE: /Clusters/patch/GetClusters
@try_manual
def step__clusters_patch_clusters(test, rg):
    test.cmd('az stack-hci cluster update '
             '--tags tag1="value1" tag2="value2" '
             '--name "{cluster_name}" '
             '--resource-group "{rg}"',
             checks=[test.check('tags', {'tag1': 'value1', 'tag2': 'value2'})])


# EXAMPLE: /Clusters/delete/GetClusters
@try_manual
def step__clusters_delete_clusters(test, rg):
    test.cmd('az stack-hci cluster delete '
             '--name "{cluster_name}" '
             '--resource-group "{rg}" -y',
             checks=[])


@try_manual
def cleanup(test, rg):
    test.cmd("ad app delete --id {aad_client_id} ")


@try_manual
def call_scenario(test, rg):
    setup(test, rg)
    step__clusters_put_clusters(test, rg)
    step__clusters_get_clusters(test, rg)
    step__clusters_list_clusters(test, rg, 1)
    step__clusters_patch_clusters(test, rg)
    step__clusters_delete_clusters(test, rg)
    step__clusters_list_clusters(test, rg, 0)
    cleanup(test, rg)


@try_manual
class AzureStackHCIClientScenarioTest(ScenarioTest):

    @ResourceGroupPreparer(name_prefix='cli_test_stack_hci_test-rg'[:7], key='rg', parameter_name='rg')
    def test_stack_hci(self, rg):

        call_scenario(self, rg)
        raise_if()
