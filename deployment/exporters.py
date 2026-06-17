import joblib, json, os
class DeploymentExporter:
    def export(self, model, schema: dict, config: dict, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        joblib.dump(model, os.path.join(output_dir, "model.joblib"))
        with open(os.path.join(output_dir, "schema.json"), "w") as f:
            json.dump(schema, f, indent=2)
        with open(os.path.join(output_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
        with open(os.path.join(output_dir, "requirements.txt"), "w") as f:
            f.write("scikit-learn\npandas\nnumpy\njoblib\n")
        print(f"Package saved → {output_dir}")
