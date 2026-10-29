"""Inngangen til Azure Functions-appen. Registrerer alle endepunktene."""

import azure.functions as func

from welcome.routes import bp

app = func.FunctionApp()
app.register_functions(bp)