from controller.Help import helpController
from middleware.Help import helpMiddleware
from packages.App.App import App

def registerHelp() -> None:
    App.routes("help", helpController, helpMiddleware)