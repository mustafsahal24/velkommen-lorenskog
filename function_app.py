import json 
import azure.functions as func

app = func.FunctionApp()


@app.route(route="welcome", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def welcome(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")

    if not name: 
        return func.HttpResponse(
            json.dumps({"error": "Mangler parameteren 'name'"}),
            status_code=400,
            mimetype="application/json",
        )

    body = {"message": f"Velkommen til Lorenskog, {name}!"}
    return func.HttpResponse(
        json.dumps(body),
        status_code=200,
        mimetype="application/json",
    )