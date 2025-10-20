from middleware.Translator import translatorMiddleware
from packages.App.App import App
from controller.translator.Translator import translatorController

def registerTranslator() -> None:
    App.routes("--translator", translatorController, translatorMiddleware)