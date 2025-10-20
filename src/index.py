from packages.App.App import App
import sys

from routes.Help import registerHelp
from routes.Translator import registerTranslator

registerHelp()
registerTranslator()
App.run(sys.argv[1:])
