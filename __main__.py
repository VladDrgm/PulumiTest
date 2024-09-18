import pulumi
from pulumi_azure_native import resources, storage, web

# Step 1: Retrieve Resource Group
resource_group = resources.get_resource_group("VladTest")

# Step 2: Create a Storage Account (required by the Functions App)
storage_account = storage.StorageAccount(
    "vdpulumisa",
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name="Standard_LRS"
    ),
    kind="StorageV2",
)



# Step 3: Create an App Service Plan (for the Functions App)
app_service_plan = web.AppServicePlan(
    "vd-pulumi-asp",
    resource_group_name=resource_group.name,
    sku=web.SkuDescriptionArgs(
        tier="Dynamic",  # The "Dynamic" SKU is used for consumption plans (pay-per-execution)
        name="Y1",
    ),
    kind="FunctionApp",
)

# Step 4: Create the Functions App
functions_app = web.WebApp(
    "vd-pulumi-fa",
    resource_group_name=resource_group.name,
    server_farm_id=app_service_plan.id,
    kind="FunctionApp",
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(
                name="AzureWebJobsStorage"
            ),
            web.NameValuePairArgs(
                name="FUNCTIONS_WORKER_RUNTIME",
                value="python",  # Set to "python" or another language if needed (e.g., "dotnet", "node", "java").
            ),
        ],
    ),
)

# Step 5: Export the URL of the Functions App
# pulumi.export("functionAppUrl", functions_app.default_host_name)
