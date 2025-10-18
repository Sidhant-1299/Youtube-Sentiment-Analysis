from mlflow.tracking import MlflowClient
import mlflow

TRACKING_URI = "http://3.19.222.199:5000/"
mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient()
# run_id = client.get_model_version_by_name("yt_chrome_plugin_model", "3").run_id
# artifacts = client.list_artifacts(run_id, path="")
# print(artifacts)

# for model in client.search_registered_models():
#     print(f"MODEL NAME: {model.name}")

model_name = "yt_chrome_plugin_model"
model_version = "3"
model_uri = f"models:/{model_name}/{model_version}"

reg_model = client.get_registered_model(model_name)
run_id = reg_model.latest_versions[0].run_id

print(run_id)

artifacts = client.list_artifacts(run_id, path="")
print(artifacts)

