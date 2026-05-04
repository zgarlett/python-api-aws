/// <reference path=".sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "python-backend",
      removal: input?.stage === "production" ? "retain" : "remove",
      protect: ["production"].includes(input?.stage),
      home: "aws",
    };
  },
  async run() {
    const api = new sst.aws.ApiGatewayV2("Api");

    api.route("GET /", {
      handler: "functions/api.get_root",
      runtime: "python3.12",
    });

    api.route("GET /items", {
      handler: "functions/api.get_items",
      runtime: "python3.12",
    });

    api.route("GET /items/{id}", {
      handler: "functions/api.get_item",
      runtime: "python3.12",
    });

    api.route("POST /items", {
      handler: "functions/api.create_item",
      runtime: "python3.12",
    });

    api.route("DELETE /items/{id}", {
      handler: "functions/api.delete_item",
      runtime: "python3.12",
    });

    return {
      api: api.url,
    };
  },
});
